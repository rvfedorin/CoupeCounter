import tkinter
from PIL import Image, ImageTk
import os

# my models
import settings


class FormNoSection:
    def __init__(self, master_frame):
        try:
            self.img_ldsp = Image.open(os.path.join(settings.mater_img, 'wfon.jpg'))
            self.img_ldsp = self.img_ldsp.resize((60, 207), Image.ANTIALIAS)
        except:
            print('Image ldsp not found')

        try:
            self.img_mirror = Image.open(os.path.join(settings.mater_img, 'gfon.jpg'))
            self.img_mirror = self.img_mirror.resize((60, 207), Image.ANTIALIAS)
        except:
            print('Image mirror not found')

        self.ldsp = ImageTk.PhotoImage(self.img_ldsp)
        self.mirror = ImageTk.PhotoImage(self.img_mirror)
        self.canvas = tkinter.Canvas(master_frame, width=250, height=250)
        self.door = self.canvas.create_rectangle(50, 20, 190, 240)
        self.part_left = self.canvas.create_rectangle(56, 26, 117, 234)
        self.part_right = self.canvas.create_rectangle(123, 26, 184, 234)
        self.part_left_mat = self.canvas.create_image(86.5, 130, image=self.mirror)
        self.part_right_mat = self.canvas.create_image(153.5, 130, image=self.ldsp)


class FormTwoSection:
    def __init__(self, master_frame):
        try:
            self.img_ldsp = Image.open(os.path.join(settings.mater_img, 'wfon.jpg'))
            self.img_ldsp = self.img_ldsp.resize((60, 100), Image.ANTIALIAS)
        except:
            print('Image ldsp not found')

        try:
            self.img_mirror = Image.open(os.path.join(settings.mater_img, 'gfon.jpg'))
            self.img_mirror = self.img_mirror.resize((60, 100), Image.ANTIALIAS)
        except:
            print('Image mirror not found')

        self.ldsp = ImageTk.PhotoImage(self.img_ldsp)
        self.mirror = ImageTk.PhotoImage(self.img_mirror)
        self.canvas = tkinter.Canvas(master_frame, width=250, height=250)
        self.door = self.canvas.create_rectangle(50, 20, 190, 240)

        self.part_left_top = self.canvas.create_rectangle(56, 26, 117, 127)
        self.part_right_top = self.canvas.create_rectangle(123, 26, 184, 127)
        self.part_left_bottom = self.canvas.create_rectangle(56, 133, 117, 234)
        self.part_right_bottom = self.canvas.create_rectangle(123, 133, 184, 234)

        self.part_left_top_mat = self.canvas.create_image(86.5, 77, image=self.mirror)
        self.part_right_top_mat = self.canvas.create_image(153.5, 77, image=self.ldsp)
        self.part_left_bottom_mat = self.canvas.create_image(86.5, 184, image=self.ldsp)
        self.part_right_bottom_mat = self.canvas.create_image(153.5, 184, image=self.mirror)
