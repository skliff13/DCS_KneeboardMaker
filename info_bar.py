import os
from tkinter import *


class InfoBar:
    def __init__(self, root):
        self.root = root
        self.frame = Frame(root, bd=1, relief=GROOVE)
        self.frame.pack(side=LEFT, fill=BOTH)
        self.scale_kilometers_per_pixel = DoubleVar(value=0.06425)

        self.__add_label('Image info', anchor=N)
        self.img_file_label = self.__add_label('Image file: <not loaded>')
        self.img_resolution_label = self.__add_label('Image resolution: ')
        self.__add_label('')
        self.__add_label('Display settings', anchor=N)
        self.scale_label = self.__add_label('Scale (+/-): ')

        self.draw_landmarks = IntVar(value=1)
        self.draw_connections = IntVar(value=1)
        self.cb_frame = Frame(self.frame, bd=4)
        self.cb_landmarks = Checkbutton(self.cb_frame, text='Draw landmarks', variable=self.draw_landmarks,
                                        command=root.update_preview)
        self.cb_landmarks.pack(side=LEFT)
        self.cb_connections = Checkbutton(self.cb_frame, text='Draw connections', variable=self.draw_connections,
                                          command=root.update_preview)
        self.cb_connections.pack(side=LEFT)
        self.cb_frame.pack(side=TOP)

        self.__add_label('')
        self.__add_label('Landmarks', anchor=N)
        landmarks_frame = Frame(self.frame)
        scrollbar_landmarks = Scrollbar(landmarks_frame, orient=VERTICAL)
        scrollbar_landmarks.pack(side=RIGHT, fill=Y)
        self.landmarks = StringVar()
        self.listbox_landmarks = Listbox(landmarks_frame, listvariable=self.landmarks)
        self.listbox_landmarks.bind('<Double-Button-1>', self.lb_landmarks_double_click)
        self.listbox_landmarks.pack(side=TOP, fill=BOTH, expand=True)
        self.listbox_landmarks.config(yscrollcommand=scrollbar_landmarks.set)
        scrollbar_landmarks.config(command=self.listbox_landmarks.yview)
        landmarks_frame.pack(side=TOP, fill=BOTH, expand=True)

        connections_frame = Frame(self.frame)
        self.__add_label('Connections', anchor=N)
        scrollbar_connections = Scrollbar(connections_frame, orient=VERTICAL)
        scrollbar_connections.pack(side=RIGHT, fill=Y)
        self.connections = StringVar()
        self.listbox_connections = Listbox(connections_frame, listvariable=self.connections)
        self.listbox_connections.bind('<Double-Button-1>', self.lb_connections_double_click)
        self.listbox_connections.pack(side=TOP, fill=BOTH, expand=True)
        self.listbox_connections.config(yscrollcommand=scrollbar_connections.set)
        scrollbar_connections.config(command=self.listbox_connections.yview)
        connections_frame.pack(side=TOP, fill=BOTH, expand=True)

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

    def lb_landmarks_double_click(self, _=None):
        item_idx = self.listbox_landmarks.curselection()[0]
        landmark = self.listbox_landmarks.get(item_idx)

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

    def lb_connections_double_click(self, _=None):
        item_idx = self.listbox_connections.curselection()[0]
        connection = self.listbox_connections.get(item_idx)

        msg = 'Please enter two comma-separated landmark codes:\n'
        msg += '\nCODE1,CODE2\n\n'
        msg += 'e.g.\nCQ,ER\n'
        title = 'Editing connection'

        connection_string = self.root.request_connection_string(title, msg, initial_value=connection)

        if not connection_string:
            return

        connections = list(eval(self.connections.get()))
        connections[item_idx] = connection_string
        self.connections.set(connections)
        self.root.update_preview()
