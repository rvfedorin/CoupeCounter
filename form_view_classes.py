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

        self.mat_dict = {'left': (self.mirror, 'Зеркало'), 'right': (self.ldsp, 'ЛДСП')}

        self.parts = {
            'left': (self.canvas.create_image(86.5, 130, image=self.mat_dict['left'][0]),
                     self.canvas.create_text(86.5, 130, text=self.mat_dict['left'][1])),

            'right': (self.canvas.create_image(153.5, 130, image=self.mat_dict['right'][0]),
                      self.canvas.create_text(153.5, 130, text=self.mat_dict['right'][1]))
        }

        for part, mat_txt in self.parts.items():
            self.canvas.tag_bind(mat_txt[0], '<Button-1>',
                                 lambda event, part=part: self.change_material(event, part))
            self.canvas.tag_bind(mat_txt[1], '<Button-1>',
                                 lambda event, part=part: self.change_material(event, part))

    def change_material(self, event, change_side):

        for i in self.parts.keys():
            if i == change_side:
                if self.mat_dict[change_side][0] == self.ldsp:
                    new_mat = (self.mirror, 'Зеркало')
                else:
                    new_mat = (self.ldsp, 'ЛДСП')

                self.mat_dict[change_side] = new_mat
                self.canvas.itemconfig(self.parts[i][0], image=new_mat[0])
                self.canvas.itemconfig(self.parts[i][1], text=new_mat[1])


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

        self.mat_dict = {
            'left_top': (self.mirror, 'Зеркало'),
            'right_top': (self.ldsp, 'ЛДСП'),
            'left_bottom': (self.ldsp, 'ЛДСП'),
            'right_bottom': (self.mirror, 'Зеркало'),
        }

        self.parts = {
            'left_top': (self.canvas.create_image(86.5, 77, image=self.mat_dict['left_top'][0]),
                         self.canvas.create_text(86.5, 77, text=self.mat_dict['left_top'][1])),

            'right_top': (self.canvas.create_image(153.5, 77, image=self.mat_dict['right_top'][0]),
                          self.canvas.create_text(153.5, 77, text=self.mat_dict['right_top'][1])),

            'left_bottom': (self.canvas.create_image(86.5, 184, image=self.mat_dict['left_bottom'][0]),
                            self.canvas.create_text(86.5, 184, text=self.mat_dict['left_bottom'][1])),

            'right_bottom': (self.canvas.create_image(153.5, 184, image=self.mat_dict['right_bottom'][0]),
                             self.canvas.create_text(153.5, 184, text=self.mat_dict['right_bottom'][1])),
        }

        for part, mat_txt in self.parts.items():
            self.canvas.tag_bind(mat_txt[0], '<Button-1>',
                                 lambda event, part=part: self.change_material(event, part))
            self.canvas.tag_bind(mat_txt[1], '<Button-1>',
                                 lambda event, part=part: self.change_material(event, part))

    def change_material(self, event, change_side):
        for i in self.parts.keys():
            if i == change_side:
                if self.mat_dict[change_side][0] == self.ldsp:
                    new_mat = (self.mirror, 'Зеркало')
                else:
                    new_mat = (self.ldsp, 'ЛДСП')

                self.mat_dict[change_side] = new_mat
                self.canvas.itemconfig(self.parts[i][0], image=new_mat[0])
                self.canvas.itemconfig(self.parts[i][1], text=new_mat[1])


class TreeSection:
    pass


class FormFourSection:
    pass


class OneBottomInsert:
    pass


class OneMiddleInsert:
    pass


class TreeInsert:
    pass


class TreeMiddleInsert:
    pass


class TwoInsert:
    pass


class TwoMiddleInsert:
    pass