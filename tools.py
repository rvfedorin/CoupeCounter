import tkinter
from PIL import Image, ImageTk
import os

# my models
import settings


class MyOptionMenu(tkinter.OptionMenu):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.image = Image.open(os.path.join(settings.data, 'one_down.png'))
        self.photo = ImageTk.PhotoImage(self.image)
        self.config(indicatoron=0, compound='right', image=self.photo)


class AddQuest:
    def __init__(self, frame, command):
        self.image = Image.open(f'{settings.data}/quest.png')
        self.image = self.image.resize((15, 15), Image.ANTIALIAS)
        self.photo = ImageTk.PhotoImage(self.image)
        self.button = tkinter.Button(
            frame,
            relief='groove',
            image=self.photo,
            command=command)


