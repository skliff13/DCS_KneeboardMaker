import os
from tkinter import *


class InfoBar:
    def __init__(self, root):
        self.root = root
        self.frame = Frame(root, bd=1, relief=GROOVE)
        self.frame.pack(side=LEFT, fill=BOTH)

        self.__add_label('Image info', anchor=N)
        self.img_file_label = self.__add_label('Image file: <not loaded>')
        self.img_resolution_label = self.__add_label('Image resolution: ')
        self.__add_label('')
        self.__add_label('Display settings', anchor=N)
        self.scale_label = self.__add_label('Scale (+/-): ')

    def __add_label(self, text, anchor=NW):
        label = Label(self.frame, width=40, text=text, anchor=anchor, justify=LEFT, bd=4)
        if anchor != NW:
            label.config(font='Helvetica 12 bold')
        label.pack(side=TOP)
        return label

    def update_info(self):
        file_path = self.root.file_path
        text = 'Image file: ' + os.path.split(file_path)[-1]
        self.img_file_label.config(text=text)

        img = self.root.img
        text = 'Image resolution: %i x %i' % (img.shape[1], img.shape[0])
        self.img_resolution_label.config(text=text)

        text = 'Scale (+/-): 1/' + str(self.root.display_scale)
        self.scale_label.config(text=text)
