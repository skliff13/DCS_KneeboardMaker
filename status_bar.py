from tkinter import *
from tkinter import messagebox


class StatusBar:
    def __init__(self, root):
        self.label = Label(root, text='Initialization...', bd=1, relief=SUNKEN, anchor=W)
        self.label.pack(side=BOTTOM, fill=X)
        self.root = root

    def set_status(self, string):
        self.label.config(text=string)
        self.root.update()
