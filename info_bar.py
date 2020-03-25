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
        self.__add_label('')
        self.__add_label('Landmarks', anchor=N)

        scrollbar = Scrollbar(self.frame, orient=VERTICAL)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.landmarks = StringVar()
        self.listbox = Listbox(self.frame, listvariable=self.landmarks)
        self.listbox.bind('<Double-Button-1>', self.listbox_double_click)
        self.listbox.pack(side=TOP, fill=BOTH, expand=True)
        self.listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox.yview)

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

    def listbox_double_click(self, _=None):
        item_idx = self.listbox.curselection()[0]
        landmark = self.listbox.get(item_idx)

        parts = landmark.split(',')
        xy = parts[4:]
        landmark = ','.join(parts[:4])

        msg = 'Please enter comma-separated landmark properties in format:\n'
        msg += '\nLandmarkName,CODE,radius,color\n\n'
        msg += 'e.g.\nCarpiquet,CQ,58,cyan\nEvreux,ER,46,yellow\n'
        title = 'Editing landmark'

        landmark_string = self.root.request_landmark_string(title, msg, initial_value=landmark)

        if not landmark_string:
            return

        landmarks = list(eval(self.landmarks.get()))
        landmarks[item_idx] = landmark_string + ',' + ','.join(xy)
        self.landmarks.set(landmarks)
        self.root.update_preview()
