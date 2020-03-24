import warnings
import numpy as np
from PIL import ImageTk, Image as PIL_Image, ImageDraw, ImageFont
from skimage import io
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from tkinter.simpledialog import askstring

from display_settings import DisplaySettings
from main_menu import MainMenu
from status_bar import StatusBar
from info_bar import InfoBar


class MainWindow(Tk):
    def __init__(self):
        Tk.__init__(self)

        self.app_version = '0.1'
        self.title('DCS Kneeboard Maker ' + self.app_version)

        self.main_menu = MainMenu(self)
        self.status_bar = StatusBar(self)
        self.status_bar.set_status('Ready')
        self.info_bar = InfoBar(self)

        x_scrollbar = Scrollbar(self, orient=HORIZONTAL)
        x_scrollbar.pack(side=BOTTOM, fill=X)
        y_scrollbar = Scrollbar(self, orient=VERTICAL)
        y_scrollbar.pack(side=RIGHT, fill=Y)
        self.x_scrollbar = x_scrollbar
        self.y_scrollbar = y_scrollbar

        self.file_path = ''
        self.display_scale = 4
        self.min_display_scale = 1
        self.max_display_scale = 8

        w = 640
        h = 480
        self.img = np.ones((h, w, 3), dtype=np.uint8) * 127
        empty_preview = PIL_Image.fromarray(self.img)
        empty_preview = ImageTk.PhotoImage(empty_preview)
        preview_canvas = Canvas(self, width=w, height=h, bd=2, relief=SUNKEN, bg='gray',
                                xscrollcommand=x_scrollbar.set, yscrollcommand=y_scrollbar.set,
                                scrollregion=(0, 0, w, h))
        preview_canvas.create_image(0, 0, image=empty_preview, anchor=NW)
        preview_canvas.pack(side=TOP, expand=True, fill=BOTH)
        self.preview_canvas = preview_canvas
        self.preview_canvas.bind('<Motion>', self.mouse_move)
        self.preview_canvas.bind('<Button-1>', self.left_click)
        self.preview = empty_preview

        x_scrollbar.config(command=preview_canvas.xview)
        y_scrollbar.config(command=preview_canvas.yview)

        warnings.filterwarnings('ignore')

        self.mainloop()

    def mouse_move(self, event):
        x = (event.x + self.x_scrollbar.get()[0] * self.img.shape[1]) * self.display_scale
        y = (event.y + self.y_scrollbar.get()[0] * self.img.shape[0]) * self.display_scale
        s = f'XY = ({x}, {y})'
        self.status_bar.set_status(s)

    def left_click(self, event):
        x = event.x * self.display_scale
        y = event.y * self.display_scale

        msg = 'Please enter comma-separated landmark properties in format:\n'
        msg += '\nLandmarkName,CODE,radius,color\n\n'
        msg += 'e.g.\nCarpiquet,CQ,58,cyan\nEvreux,ER,46,yellow\n'

        while True:
            landmark_string = askstring('Adding landmark', msg)

            if not landmark_string:
                return

            check_message = self.validate_landmark_string(landmark_string)
            if check_message:
                messagebox.showwarning('Wrong landmark string', check_message)
            else:
                break

        landmark_string += f',{x},{y}'
        self.info_bar.listbox.insert(END, landmark_string)

    @staticmethod
    def validate_landmark_string(s):
        parts = s.split(',')

        if len(parts) != 4:
            return 'There mut be 4 comma-separated values'

        try:
            i = int(parts[2])
            if i < 1:
                raise Exception('.')
        except:
            return 'Third value must be positive integer'

        # TODO check last value to be valid color identifier
        return None

    def zoom_in(self, _=None):
        if self.display_scale > self.min_display_scale:
            self.display_scale //= 2
            self.update_preview()
            self.info_bar.update_info()

    def zoom_out(self, _=None):
        if self.display_scale < self.max_display_scale:
            self.display_scale *= 2
            self.update_preview()
            self.info_bar.update_info()

    def open_image(self, _=None):
        formats = '*.jpg *.png *.bmp *.jpeg *.JPG *.JPEG *.PNG *.BMP'
        file_path = askopenfilename(initialdir='test_data/',
                                    filetypes=(('Image files', formats), ('All Files', '*.*')),
                                    title='Choose a file.')

        if not file_path:
            return

        try:
            img = io.imread(file_path)

            self.file_path = file_path
            self.img = img
            self.status_bar.set_status('Image loaded')

            self.info_bar.update_info()
            self.update_preview()
        except Exception as e:
            self.status_bar.set_status('Image load failed')
            messagebox.showwarning('Failed to read image',
                                   'Failed to read image from "%s":\n\n%s' % (file_path, str(e)))

    def update_preview(self):
        preview = PIL_Image.fromarray(self.img)

        self.draw_landmarks(preview)

        size = (preview.size[0] // self.display_scale, preview.size[1] // self.display_scale)
        preview.thumbnail(size)
        preview = ImageTk.PhotoImage(preview)

        self.preview_canvas.create_image(0, 0, image=preview, anchor=NW)
        self.preview_canvas.config(scrollregion=(0, 0, size[0], size[1]))
        self.preview = preview

    def draw_landmarks(self, preview):
        sts: DisplaySettings = DisplaySettings()

        draw = ImageDraw.Draw(preview)

        # font = {'size': sts.landmarkFontSize}
        sz = 50
        font = ImageFont.truetype('/usr/share/fonts/truetype/ubuntu/Ubuntu-B.ttf', size=sz)
        lw = sts.connectionWidth

        for s in self.info_bar.listbox.get(0, last=END):
            parts = tuple(s.split(','))
            _, code, r, color, x, y = parts
            r, x, y = tuple(map(int, (r, x, y)))

            draw.ellipse((x - r, y - r, x + r, y + r), outline=color)
            draw.text((x - sz // 4 * 3, y - sz // 2), code, font=font)

        #     c = plt.Circle((row.X, row.Y), row.R * sts.radiusMultiplier, edgecolor=row.Color, facecolor='none',
        #                    linewidth=lw)
        #     ax.add_artist(c)
        #     plt.text(row.X, row.Y, row.ShortName, horizontalalignment='center', verticalalignment='center',
        #              fontdict=font)


if __name__ == '__main__':
    MainWindow()
