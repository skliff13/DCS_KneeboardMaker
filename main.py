
import os
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.lines as lines
from skimage import io
from PIL import Image

from configuration import Configuration
from display_settings import DisplaySettings


class KneeboardMaker:
    def __init__(self):
        self.cfg = Configuration()
        self.sts = DisplaySettings()

        self.generate_all()

    def generate_all(self):
        sts: DisplaySettings = self.sts
        cfg: Configuration = self.cfg

        landmarks_table = pd.read_csv(cfg.path_to_landmarks)
        connections_table = pd.read_csv(cfg.path_to_connections)

        print('Reading map from "%s"' % cfg.path_to_map)
        im = io.imread(cfg.path_to_map)
        if im.shape[2] > 3:
            im = im[:, :, 0:3]
        im = sts.imageBrightnessAndContrast[0] + im.astype(float) * sts.imageBrightnessAndContrast[1]
        im[im < 0] = 0
        im[im > 255] = 255
        im = im.astype(np.uint8)

        fig = plt.figure(frameon=False)
        fig.set_size_inches(im.shape[1] / 300., im.shape[0] / 300.)
        ax = plt.Axes(fig, [0., 0., 1, 1])
        ax.set_axis_off()
        fig.add_axes(ax)

        ax.imshow(im)

        if self.cfg.draw_landmarks:
            self.draw_landmarks(ax, landmarks_table)
        if self.cfg.draw_connections:
            self.draw_connections(ax, connections_table, landmarks_table)

        if not os.path.isdir(cfg.output_dir):
            os.mkdir(cfg.output_dir)
        plt.savefig(os.path.join(cfg.output_dir, 'map_large.jpg'), dpi=sts.outputDPI)

        self.cut_for_kneeboard()

    def get_connection_info(self, row, landmarks_table):
        row = row[1]
        mrk1 = landmarks_table.loc[landmarks_table['ShortName'] == row.NM1]
        mrk2 = landmarks_table.loc[landmarks_table['ShortName'] == row.NM2]
        r1 = int(mrk1['R'])
        r2 = int(mrk2['R'])
        x01 = int(mrk1['X'])
        y01 = int(mrk1['Y'])
        x02 = int(mrk2['X'])
        y02 = int(mrk2['Y'])

        return r1, r2, x01, x02, y01, y02

    def draw_connections(self, ax, connections_table, landmarks_table):
        print('Putting connections')

        for row in connections_table.iterrows():
            r1, r2, x01, x02, y01, y02 = self.get_connection_info(row, landmarks_table)

            d0, x1, x2, y1, y2 = self.draw_conn_line(ax, r1, r2, x01, x02, y01, y02)

            self.draw_connection_center(ax, d0, x01, x02, y01, y02)

            self.draw_connection_angle(ax, d0, x1, x2, y1, y2)
            self.draw_connection_angle(ax, d0, x2, x1, y2, y1)

    def draw_connection_angle(self, ax, d0, x1, x2, y1, y2):
        sts: DisplaySettings = self.sts

        font = {'size': sts.distanceFontSize}
        color = sts.connectionColor
        w = sts.angleRectangleWidth
        h = sts.angleRectangleHeight
        degrees_in_radian = 57.295

        x1a = x1 + (x2 - x1) * w / 2 / d0
        y1a = y1 + (y2 - y1) * w / 2 / d0

        rectangle = plt.Rectangle((x1a - w // 2, y1a - h // 2), w, h, color=color)
        ax.add_artist(rectangle)

        angle = round(degrees_in_radian * math.atan2(x2 - x1, -(y2 - y1)))
        if angle < 0:
            angle = 360 + angle

        angle_text = '%i$^\circ$' % angle
        plt.text(x1a, y1a, angle_text, horizontalalignment='center', verticalalignment='center', fontdict=font)

    def draw_connection_center(self, ax, d0, x01, x02, y01, y02):
        sts: DisplaySettings = self.sts
        cfg: Configuration = self.cfg

        font = {'size': sts.distanceFontSize}
        clr = sts.connectionColor
        w = sts.distanceRectangleWidth
        h = sts.distanceRectangleHeight

        kilometers_per_nautical_mile = 1.852
        distance_km = round(d0 * cfg.scaleKilometersPerPixel)
        distance_nm = round(distance_km / kilometers_per_nautical_mile)

        if distance_km > sts.minConnCenterDistKm:
            center_x = (x01 + x02) / 2.
            center_y = (y01 + y02) / 2.
            rectangle = plt.Rectangle((center_x - w // 2, center_y - h // 2), w, h, color=clr)
            ax.add_artist(rectangle)

            dist_text = '%i km\n%i nm' % (distance_km, distance_nm)
            plt.text(center_x, center_y, dist_text, horizontalalignment='center', verticalalignment='center',
                     fontdict=font)

    def draw_conn_line(self, ax, r1, r2, x01, x02, y01, y02):
        sts: DisplaySettings = self.sts

        clr = sts.connectionColor
        dl = sts.connectionMargin
        lw = sts.connectionWidth

        d0 = ((x01 - x02) ** 2 + (y01 - y02) ** 2) ** 0.5
        x1 = x01 + (x02 - x01) * (r1 * sts.radiusMultiplier + dl) / d0
        y1 = y01 + (y02 - y01) * (r1 * sts.radiusMultiplier + dl) / d0
        x2 = x02 + (x01 - x02) * (r2 * sts.radiusMultiplier + dl) / d0
        y2 = y02 + (y01 - y02) * (r2 * sts.radiusMultiplier + dl) / d0
        line = lines.Line2D([x1, x2], [y1, y2], color=clr, linewidth=lw)
        ax.add_line(line)

        return d0, x1, x2, y1, y2

    def draw_landmarks(self, ax, landmarks_table):
        sts: DisplaySettings = self.sts

        font = {'size': sts.landmarkFontSize}
        lw = sts.connectionWidth

        print('Putting landmarks')
        for row in landmarks_table.iterrows():
            row = row[1]
            c = plt.Circle((row.X, row.Y), row.R * sts.radiusMultiplier, edgecolor=row.Color, facecolor='none',
                           linewidth=lw)
            ax.add_artist(c)
            plt.text(row.X, row.Y, row.ShortName, horizontalalignment='center', verticalalignment='center',
                     fontdict=font)

    def cut_for_kneeboard(self):
        cfg: Configuration = self.cfg

        big = io.imread(os.path.join(cfg.output_dir, 'map_large.jpg'))
        big = big[:, :, 0:3]

        im = Image.fromarray(big)
        h = round(big.shape[0] * 1024. / big.shape[1])
        im.thumbnail((1024, h), Image.ANTIALIAS)
        im.save(os.path.join(cfg.output_dir, 'map_preview.png'))

        print('Saving kneeboard pages')
        for i in range(len(cfg.slide_topleft_XYs)):
            x = cfg.slide_topleft_XYs[i][0]
            y = cfg.slide_topleft_XYs[i][1]
            small = big[y:y + cfg.slide_extraction_size[1], x:x + cfg.slide_extraction_size[0], :]

            im = Image.fromarray(small)
            im.thumbnail(cfg.slide_output_size, Image.ANTIALIAS)
            output_map_filename = 'kneeboard_%i_of_%i.png' % (i + 1, len(cfg.slide_topleft_XYs))
            im.save(os.path.join(cfg.output_dir, output_map_filename))


if __name__ == '__main__':
    KneeboardMaker()
