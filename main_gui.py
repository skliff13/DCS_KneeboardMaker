import os
import json
import warnings
import numpy as np
from PIL import ImageTk, Image as PIL_Image, ImageDraw, ImageFont, ImageColor
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

        w = 800
        h = 600
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
        x = event.x + self.x_scrollbar.get()[0] * self.img.shape[1]
        y = event.y + self.y_scrollbar.get()[0] * self.img.shape[0]
        x = int(x * self.display_scale)
        y = int(y * self.display_scale)
        s = f'XY = ({x}, {y})'
        self.status_bar.set_status(s)

    def left_click(self, event):
        x = event.x + self.x_scrollbar.get()[0] * self.img.shape[1]
        y = event.y + self.y_scrollbar.get()[0] * self.img.shape[0]
        x = int(x * self.display_scale)
        y = int(y * self.display_scale)

        msg = 'Please enter comma-separated landmark properties in format:\n'
        msg += '\nLandmarkName,CODE,radius,color\n\n'
        msg += 'e.g.\nCarpiquet,CQ,58,cyan\nEvreux,ER,46,yellow\n'
        title = 'Adding landmark'

        landmark_string = self.request_landmark_string(title, msg)

        if not landmark_string:
            return

        landmark_string += f',{x},{y}'
        val = self.info_bar.landmarks.get()
        landmarks = list(eval(val)) if val else list()
        landmarks.append(landmark_string)
        self.info_bar.landmarks.set(landmarks)
        self.update_preview()

    def add_connection(self, _=None):
        msg = 'Please enter two comma-separated landmark codes:\n'
        msg += '\nCODE1,CODE2\n\n'
        msg += 'e.g.\nCQ,ER\n'
        title = 'Adding connection'

        connection_string = self.request_connection_string(title, msg)

        if not connection_string:
            return

        val = self.info_bar.connections.get()
        connections = list(eval(val)) if val else list()
        connections.append(connection_string)
        self.info_bar.connections.set(connections)
        self.update_preview()

    def request_landmark_string(self, title, msg, initial_value='A,a,50,yellow'):
        landmark_string = None
        while True:
            try:
                landmark_string = askstring(title, msg, initialvalue=initial_value, parent=self)
            except:
                pass

            if not landmark_string:
                break

            check_message = self.validate_landmark_string(landmark_string)
            if check_message:
                initial_value = landmark_string
                landmark_string = None
                messagebox.showwarning('Wrong landmark string', check_message)
            else:
                break

        return landmark_string

    def request_connection_string(self, title, msg, initial_value='L1,L2'):
        connection_string = None
        while True:
            try:
                connection_string = askstring(title, msg, initialvalue=initial_value)
            except:
                pass

            if not connection_string:
                break

            check_message = self.validate_connection_string(connection_string)
            if check_message:
                initial_value = connection_string
                connection_string = None
                messagebox.showwarning('Wrong connection string', check_message)
            else:
                break

        return connection_string

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
            msg = f'"{parts[2]}" is not a valid positive integer\n\n'
            msg += 'Third value must be positive integer'
            return msg

        try:
            ImageColor.getrgb(parts[3])
        except:
            msg = f'"{parts[3]}" is not a valid color string\n\n'
            msg += 'Fourth value must be a valid color name (e.g. "red", "blue", "cyan", "yellow", "magenta", ...)'
            return msg

        return None

    @staticmethod
    def validate_connection_string(s):
        parts = s.split(',')

        if len(parts) != 2:
            return 'There mut be 2 comma-separated values'

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

    def save_info(self, _=None):
        info_path = os.path.splitext(self.file_path)[0] + '_info.json'

        info = {'landmarks': [s for s in self.info_bar.listbox_landmarks.get(0, last=END)],
                'connections': [s for s in self.info_bar.listbox_connections.get(0, last=END)]}

        with open(info_path, 'wt') as f:
            json.dump(info, f, indent=2)

        self.status_bar.set_status('Image info saved')

    def open_image(self, _=None):
        formats = '*.jpg *.png *.bmp *.jpeg *.JPG *.JPEG *.PNG *.BMP'
        file_types = (('Image files', formats), ('All Files', '*.*'))
        file_path = askopenfilename(initialdir='test_data/', filetypes=file_types, title='Choose a file.')

        if not file_path:
            return

        try:
            img = io.imread(file_path)

            self.file_path = file_path
            self.img = img
            self.status_bar.set_status('Image loaded')
        except Exception as e:
            self.status_bar.set_status('Image load failed')
            msg = f'Failed to read image from "{file_path}":\n\n{str(e)}'
            messagebox.showwarning('Failed to read image', msg)

        info_path = os.path.splitext(file_path)[0] + '_info.json'
        if not os.path.isfile(info_path):
            self.info_bar.update_info()
            self.update_preview()
            return

        try:
            with open(info_path,'rt') as f:
                info = json.load(f)

            landmarks = info['landmarks']
            self.info_bar.landmarks.set(landmarks)

            connections = info['connections']
            self.info_bar.connections.set(connections)

            self.info_bar.update_info()
            self.update_preview()
        except Exception as e:
            self.status_bar.set_status('Image info load failed')
            msg = f'Failed to read image info from "{file_path}":\n\n{str(e)}'
            messagebox.showwarning('Failed to read image info', msg)

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

        sz = sts.landmarkFontSize
        font = ImageFont.truetype('font/Ubuntu-B.ttf', size=sz)
        lw = sts.connectionWidth

        for s in self.info_bar.listbox_landmarks.get(0, last=END):
            parts = tuple(s.split(','))
            _, code, r, color, x, y = parts
            r, x, y = tuple(map(int, (r, x, y)))

            for d in range(int(lw)):
                r1 = r + d
                draw.ellipse((x - r1, y - r1, x + r1, y + r1), outline=color)
                draw.text((x - sz // 4 * 3, y - sz // 2), code, font=font)


if __name__ == '__main__':
    MainWindow()
