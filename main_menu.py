from tkinter import *
from tkinter import messagebox


class MainMenu:
    def __init__(self, root):
        self.root = root
        self.menu = Menu(root)
        root.config(menu=self.menu)

        submenu = Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label='File', menu=submenu)
        submenu.add_command(label='Open image (Ctrl+O)', command=self.root.open_image)
        self.root.bind_all("<Control-o>", self.root.open_image)
        submenu.add_separator()
        submenu.add_command(label='Exit', command=root.destroy)

        submenu = Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label='Edit', menu=submenu)
        submenu.add_command(label='Zoom in (+)', command=self.root.zoom_in)
        self.root.bind_all('<plus>', self.root.zoom_in)
        self.root.bind_all('<equal>', self.root.zoom_in)
        self.root.bind_all('<KP_Add>', self.root.zoom_in)
        submenu.add_command(label='Zoom out (-)', command=self.root.zoom_out)
        self.root.bind_all('<minus>', self.root.zoom_out)
        self.root.bind_all('<KP_Subtract>', self.root.zoom_out)

        submenu = Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label='Help', menu=submenu)
        submenu.add_command(label='About', command=self.about)
        self.root.bind_all("<F1>", self.about)

    def about(self, event=None):
        txt = ''
        txt += 'DCS Kneeboard Maker ' + self.root.app_version + '\n\n'
        txt += 'Developed by skliff13\n'
        txt += 'https://github.com/skliff13\n'
        txt += 'Contact e-mail: vitali.liauchuk@gmail.com\n'
        messagebox.showinfo('About', txt)