import os
import json
import warnings
import numpy as np
from PIL import ImageTk, Image as PIL_Image, ImageColor
from skimage import io
from skimage.transform import resize
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from tkinter.simpledialog import askstring, askfloat

from drawing import draw_landmarks, draw_connections, draw_slides
from main_menu import MainMenu
from status_bar import StatusBar
from info_bar import InfoBar
from display_settings import DisplaySettings


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
        self.preview_canvas.bind('<Button-3>', self.right_click)
        self.preview_canvas.bind('<MouseWheel>', self.mouse_wheel)
        self.preview_canvas.bind('<Button-4>', self.mouse_wheel)
        self.preview_canvas.bind('<Button-5>', self.mouse_wheel)
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

    def mouse_wheel(self, event):
        if event.num == 5 or event.delta == -120:
            self.zoom_out()
        if event.num == 4 or event.delta == 120:
            self.zoom_in()

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
        landmarks.sort()
        self.info_bar.landmarks.set(landmarks)
        self.update_preview()

    def right_click(self, event):
        x = event.x + self.x_scrollbar.get()[0] * self.img.shape[1]
        y = event.y + self.y_scrollbar.get()[0] * self.img.shape[0]
        x = int(x * self.display_scale)
        y = int(y * self.display_scale)

        sh = self.info_bar.slide_height.get()
        sw = int(sh / 1.5)
        left = max(1, min(x - sw // 2, self.img.shape[1] - sw - 1))
        top = max(1, min(y - sh // 2, self.img.shape[0] - sh - 1))

        center_xy = (left + sw // 2, top + sh // 2)
        self.info_bar.slide_centers.append(center_xy)
        self.update_preview()

    def pop_slide_center(self, _=None):
        if self.info_bar.slide_centers:
            self.info_bar.slide_centers.pop()
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
        connections.sort()
        self.info_bar.connections.set(connections)
        self.update_preview()

    def request_landmark_string(self, title, msg, initial_value='Name,CODE,50,yellow'):
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
                'connections': [s for s in self.info_bar.listbox_connections.get(0, last=END)],
                'scale_kilometers_per_pixel': self.info_bar.scale_kilometers_per_pixel.get(),
                'slide_height': self.info_bar.slide_height.get(),
                'slide_centers': self.info_bar.slide_centers,
                'draw': {'landmarks': self.info_bar.draw_landmarks.get(),
                         'connections': self.info_bar.draw_connections.get(),
                         'angles': self.info_bar.draw_angles.get(),
                         'distances': self.info_bar.draw_distances.get()}
                }

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

            self.info_bar.landmarks.set(info['landmarks'])
            self.info_bar.connections.set(info['connections'])
            self.info_bar.scale_kilometers_per_pixel.set(info['scale_kilometers_per_pixel'])
            self.info_bar.slide_height.set(info['slide_height'])
            self.info_bar.slide_centers = info['slide_centers']
            self.info_bar.draw_landmarks.set(info['draw']['landmarks'])
            self.info_bar.draw_connections.set(info['draw']['connections'])
            self.info_bar.draw_angles.set(info['draw']['angles'])
            self.info_bar.draw_distances.set(info['draw']['distances'])

            self.info_bar.sld_slide_size.config(from_=self.img.shape[0] // 4, to=self.img.shape[0] - 2)

            self.info_bar.update_info()
            self.update_preview()
        except Exception as e:
            self.status_bar.set_status('Image info load failed')
            msg = f'Failed to read image info from "{file_path}":\n\n{str(e)}'
            messagebox.showwarning('Failed to read image info', msg)

    def update_preview(self, _=None):
        preview = PIL_Image.fromarray(self.img)

        if self.info_bar.draw_landmarks.get():
            draw_landmarks(self, preview)

        if self.info_bar.draw_connections.get():
            draw_connections(self, preview)

        draw_slides(self, preview)

        size = (preview.size[0] // self.display_scale, preview.size[1] // self.display_scale)
        preview.thumbnail(size)
        preview = ImageTk.PhotoImage(preview)

        self.preview_canvas.create_image(0, 0, image=preview, anchor=NW)
        self.preview_canvas.config(scrollregion=(0, 0, size[0], size[1]))
        self.preview = preview

    def set_image_scale(self, _=None):
        value = askfloat('Enter image scale', 'Enter image pixel size in kilometers',
                         initialvalue=self.info_bar.scale_kilometers_per_pixel.get())

        if value:
            self.info_bar.scale_kilometers_per_pixel.set(value)
            self.update_preview()

    def export_slides(self, _=None):
        self.status_bar.set_status('Exporting ...')
        preview = PIL_Image.fromarray(self.img)

        if self.info_bar.draw_landmarks.get():
            draw_landmarks(self, preview)

        if self.info_bar.draw_connections.get():
            draw_connections(self, preview)

        sts = DisplaySettings()
        us = sts.export_upsize
        order = sts.export_interpolation_order

        out_dir = os.path.splitext(self.file_path)[0] + '_slides'
        os.makedirs(out_dir, exist_ok=True)
        img = np.array(preview)
        for i, xy in enumerate(self.info_bar.slide_centers):
            sh = self.info_bar.slide_height.get()
            sw = int(sh / 1.5)
            left = max(1, min(xy[0] - sw // 2, self.img.shape[1] - sw - 1))
            top = max(1, min(xy[1] - sh // 2, self.img.shape[0] - sh - 1))

            slide = img[top:top + sh, left:left + sw]
            slide = resize(slide, (slide.shape[0] * us, slide.shape[1] * us), order=order)
            slide = (slide * 255).astype(np.uint8)
            slide_path = os.path.join(out_dir, 'slide_%02i.jpg' % i)
            io.imsave(slide_path, slide)

        draw_slides(self, preview)
        preview = np.array(preview)
        preview = resize(preview, (preview.shape[0] * us, preview.shape[1] * us), order=order)
        preview = (preview * 255).astype(np.uint8)
        preview_path = os.path.join(out_dir, 'preview.jpg')
        io.imsave(preview_path, preview)

        msg = f'The slides have been exported to "{out_dir}"'
        messagebox.showinfo('Export finished', msg)


if __name__ == '__main__':
    MainWindow()
