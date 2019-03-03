import os
import json
import time
import warnings
import numpy as np
import matplotlib.pyplot as plt
import PIL
from PIL import ImageTk
from skimage import io
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename

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

        self.file_path = ''
        self.display_scale = 4
        self.min_display_scale = 1
        self.max_display_scale = 8

        w = 640
        h = 480
        self.img = np.ones((h, w, 3), dtype=np.uint8) * 127
        empty_preview = PIL.Image.fromarray(self.img)
        empty_preview = ImageTk.PhotoImage(empty_preview)
        preview_canvas = Canvas(self, width=w, height=h, bd=2, relief=SUNKEN, bg='gray',
                                xscrollcommand=x_scrollbar.set, yscrollcommand=y_scrollbar.set,
                                scrollregion=(0, 0, w, h))
        preview_canvas.create_image(0, 0, image=empty_preview, anchor=NW)
        preview_canvas.pack(side=TOP, expand=True, fill=BOTH)
        self.preview_canvas = preview_canvas
        self.preview = empty_preview

        x_scrollbar.config(command=preview_canvas.xview)
        y_scrollbar.config(command=preview_canvas.yview)

        warnings.filterwarnings('ignore')

        self.mainloop()

    def zoom_in(self, event=None):
        if self.display_scale > self.min_display_scale:
            self.display_scale //= 2
            self.update_preview()
            self.info_bar.update_info()

    def zoom_out(self, event=None):
        if self.display_scale < self.max_display_scale:
            self.display_scale *= 2
            self.update_preview()
            self.info_bar.update_info()

    def open_image(self, event=None):
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
        preview = PIL.Image.fromarray(self.img)
        size = (preview.size[0] // self.display_scale, preview.size[1] // self.display_scale)
        preview.thumbnail(size)
        preview = ImageTk.PhotoImage(preview)

        self.preview_canvas.create_image(0, 0, image=preview, anchor=NW)
        self.preview_canvas.config(scrollregion=(0, 0, size[0], size[1]))
        self.preview = preview


if __name__ == '__main__':
    MainWindow()
