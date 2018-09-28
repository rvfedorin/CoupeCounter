import tkinter
from PIL import Image, ImageTk

import settings


class AddQuest:
    def __init__(self, frame, command):
        self.image = Image.open(f'{settings.data}/quest.png')
        self.image = self.image.resize((15, 15), Image.ANTIALIAS)
        self.photo = ImageTk.PhotoImage(self.image)
        self.button = tkinter.Button(
            frame,
            relief='groove',
            image=self.photo,
            command=lambda _name='quest_tape': command(_name))


