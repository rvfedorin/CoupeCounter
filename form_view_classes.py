import tkinter
from PIL import Image, ImageTk
import os

# my models
import settings


class ChangeMixin:
    def __init__(self):
        self.parts = None
        self.mat_dict = None
        self.canvas = None
        self.ldsp = None
        self.mirror = None

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


class FormSection(ChangeMixin):
    def __init__(self, master_frame, num_doors=2, sec=0):
        super().__init__()
        self.num_doors = num_doors
        self.x_size = 51
        self.y_size = 208
        self.padd = 4
        self.sec = sec
        self.mat_dict = {}
        self.parts = {}
        self.frame = master_frame

        try:
            self.img_ldsp = Image.open(os.path.join(settings.mater_img, 'wfon.jpg'))
            if self.sec:
                y_size = int((self.y_size - self.padd*(self.sec-1)) / self.sec)
                self.img_ldsp = self.img_ldsp.resize((self.x_size-1, y_size - 2), Image.ANTIALIAS)
            else:
                self.img_ldsp = self.img_ldsp.resize((self.x_size - 1, self.y_size - 2), Image.ANTIALIAS)
        except:
            print('Image ldsp not found')

        try:
            self.img_mirror = Image.open(os.path.join(settings.mater_img, 'gfon.jpg'))
            if self.sec:
                y_size = int((self.y_size - self.padd*(self.sec-1)) / self.sec)
                self.img_mirror = self.img_mirror.resize((self.x_size-1, y_size - 1), Image.ANTIALIAS)
            else:
                self.img_mirror = self.img_mirror.resize((self.x_size - 1, self.y_size - 2), Image.ANTIALIAS)
        except:
            print('Image mirror not found')

        self.ldsp = ImageTk.PhotoImage(self.img_ldsp)
        self.mirror = ImageTk.PhotoImage(self.img_mirror)
        self.canvas = tkinter.Canvas(self.frame, width=480, height=250)

        x1 = 20 * (9 - self.num_doors) + self.padd * (8 - self.num_doors) * 2
        y1 = 26
        x2 = x1 + self.x_size
        y2 = y1 + self.y_size - self.padd

        self.door = self.canvas.create_rectangle(x1-self.padd, y1-self.padd,
                                                 x1+(self.x_size+self.padd)*self.num_doors,
                                                 y1 + self.y_size + self.padd)

        door_count = self.num_doors
        num_part = 1
        mat_random = 0
        while door_count:  # все дверу нумеруем
            sec_count = self.sec
            if self.sec:  # если дверь разбита на секции
                while sec_count:
                    y2 = y1 + (self.y_size - self.padd*(self.sec-1)) / self.sec
                    self.canvas.create_rectangle(x1, y1, x2, y2)  # рисуем двери

                    if mat_random:  # чередуем материал частей
                        mat_random += 1
                        self.mat_dict[num_part] = (self.ldsp, 'ЛДСП')  # запоминаем материал каждой двери
                    else:
                        mat_random -= 1
                        self.mat_dict[num_part] = (self.mirror, 'Зеркало')

                    x = x1 + 1 + self.x_size/4 + self.padd * 2 + self.padd
                    y = y1 + 1 + self.img_ldsp.size[1] / 2
                    self.parts[num_part] = (
                        self.canvas.create_image(x, y, image=self.mat_dict[num_part][0]),
                        self.canvas.create_text(x, y, text=self.mat_dict[num_part][1])
                    )
                    y1 = y2 + self.padd
                    sec_count -= 1
                    num_part += 1
                x1 = x1 + self.padd + self.x_size
                x2 = x1 + self.x_size
                y1 = 26
                door_count -= 1

            else:  # если секций нет
                if mat_random:  # чередуем материал частей
                    mat_random += 1
                    self.mat_dict[num_part] = (self.ldsp, 'ЛДСП')  # запоминаем материал каждой двери
                else:
                    mat_random -= 1
                    self.mat_dict[num_part] = (self.mirror, 'Зеркало')
                self.canvas.create_rectangle(x1, y1, x2, y2 + self.padd - 1)  # рисуем двери
                x1 = x1 + self.padd + self.x_size
                x2 = x1 + self.x_size

                x = x1 - self.padd - self.x_size / 2
                y = y1 + self.y_size / 2
                self.parts[num_part] = (
                    self.canvas.create_image(x, y, image=self.mat_dict[num_part][0]),
                    self.canvas.create_text(x, y, text=self.mat_dict[num_part][1])
                )
                door_count -= 1
                num_part += 1

            for part, mat_txt in self.parts.items():
                self.canvas.tag_bind(mat_txt[0], '<Button-1>',
                                     lambda event, part=part: self.change_material(event, part))
                self.canvas.tag_bind(mat_txt[1], '<Button-1>',
                                     lambda event, part=part: self.change_material(event, part))


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