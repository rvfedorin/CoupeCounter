import tkinter
from PIL import Image, ImageTk
import os

# my models
import settings


class ChangeMixin:
    def __init__(self, need_entry=True, *args, **kwargs):
        self.parts = None
        self.mat_dict = None
        self.canvas = None
        self.ldsp = None
        self.mirror = None
        self.mat_indicator = None
        self.insertion_list = None
        self.need_entry = need_entry

    def change_material(self, event, change_side):
        for i in self.parts.keys():
            if i == change_side:
                # меняем местами, т.к. во второй части противоположное значение
                new_mat = (self.mat_dict[change_side][2], self.mat_dict[change_side][3],
                           self.mat_dict[change_side][0], self.mat_dict[change_side][1])

                self.mat_dict[change_side] = new_mat
                self.canvas.itemconfig(self.parts[i][0], image=new_mat[0])
                self.canvas.itemconfig(self.parts[i][1], text=new_mat[1])

    def mat_random(self, num_part):  # чередование материала части
        if self.mat_indicator:
            self.mat_indicator -= 1
            # запоминаем материал каждой двери и противоположность
            self.mat_dict[num_part] = (self.ldsp, 'ЛДСП', self.mirror, 'Зеркало')
        else:
            self.mat_indicator += 1
            self.mat_dict[num_part] = (self.mirror, 'Зеркало', self.ldsp, 'ЛДСП')

    def create_binds(self):
        for part, mat_txt in self.parts.items():
            self.canvas.tag_bind(mat_txt[0], '<Button-1>',
                                 lambda event, part=part: self.change_material(event, part))
            self.canvas.tag_bind(mat_txt[1], '<Button-1>',
                                 lambda event, part=part: self.change_material(event, part))

    def make_form(self, copy=False):
        pass

    def make_only_view(self):
        self.need_entry = False
        self.make_form(copy=True)


class FormSection(ChangeMixin):
    def __init__(self, master_frame, num_doors=2, sec=1, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.num_doors = num_doors
        self.opening_h = int(master_frame.main_frame.param_door.height_var.get())
        self.opening_w = int(master_frame.main_frame.param_door.width_var.get())
        self.x_size = int(self.opening_w / 28)
        self.y_size = int(self.opening_h / 14)
        self.padd = 4
        self.sec = sec
        self.mat_dict = {}
        self.parts = {}
        self.frame = master_frame
        self.mat_indicator = 0
        self.make_form()

    def make_form(self, copy=False):
        try:
            self.img_ldsp = Image.open(os.path.join(settings.mater_img, 'wfon.jpg'))
            self.img_mirror = Image.open(os.path.join(settings.mater_img, 'gfon.jpg'))
            y_size = int((self.y_size - self.padd*(self.sec-1)) / self.sec)
            self.img_ldsp = self.img_ldsp.resize((self.x_size-2, y_size - 2), Image.ANTIALIAS)
            self.img_mirror = self.img_mirror.resize((self.x_size - 1, y_size - 1), Image.ANTIALIAS)
        except:
            print('Image ldsp or mirror not found')

        self.ldsp = ImageTk.PhotoImage(self.img_ldsp)
        self.mirror = ImageTk.PhotoImage(self.img_mirror)
        cx = self.x_size * self.num_doors + self.num_doors*self.padd + self.padd * 3
        cy = self.y_size + self.padd * 5
        self.canvas = tkinter.Canvas(self.frame, width=cx, height=cy)

        x1 = 10
        y1 = 10
        x2 = x1 + self.x_size
        y2 = y1 + self.y_size - self.padd

        self.door = self.canvas.create_rectangle(x1-self.padd, y1-self.padd,
                                                 x1+(self.x_size+self.padd)*self.num_doors,
                                                 y1 + self.y_size + self.padd)

        door_count = self.num_doors
        num_part = 1
        while door_count:  # все дверу нумеруем
            sec_count = self.sec
            while sec_count:
                y2 = y1 + (self.y_size - self.padd*(self.sec-1)) / self.sec
                self.canvas.create_rectangle(x1, y1, x2, y2)  # рисуем двери

                if not copy:
                    self.mat_random(num_part)  # чередование материала части

                x = x1 + 1 + self.img_ldsp.size[0] / 2
                y = y1 + 1 + self.img_ldsp.size[1] / 2
                self.parts[num_part] = (
                    self.canvas.create_image(x, y, image=self.mat_dict[num_part][0]),
                    self.canvas.create_text(x, y, text=self.mat_dict[num_part][1])
                )
                y1 = y2 + self.padd
                sec_count -= 1
                num_part += 1
            x1 = x1 + self.padd + self.img_ldsp.size[0] + self.padd / 2
            x2 = x1 + self.padd + self.img_ldsp.size[0] - self.padd / 2
            y1 = 10
            door_count -= 1
            if self.need_entry:
                self.create_binds()  # создать привязки смены материала, определён в ChangeMixin

    def copy(self, object):
        object.num_doors = self.num_doors
        object.num_doors = self.num_doors
        object.opening_h = self.opening_h
        object.opening_w = self.opening_w
        object.x_size = self.x_size
        object.y_size = self.y_size
        object.padd = self.padd
        object.sec = self.sec
        object.mat_dict = self.mat_dict.copy()
        object.parts = self.parts.copy()
        object.mat_indicator = self.mat_indicator


class WithInsert(ChangeMixin):
    def __init__(self, master_frame, num_doors=2, insertion=2, insertion_list=None, **kwargs):
        super().__init__(**kwargs)
        self.frame = master_frame
        self.num_doors = num_doors
        self.opening_h = int(self.frame.main_frame.param_door.height_var.get())  # высота проёма
        self.opening_w = int(self.frame.main_frame.param_door.width_var.get())  # ширина проёма
        self.delim = 14  # масштаб
        self.x_size = int(self.opening_w / (self.delim*2))
        self.y_size = int(self.opening_h / self.delim)
        self.padd = 4  # отступ от частей двери
        self.insertion_photo_dict = {}
        if insertion_list:
            self.insertion_list = insertion_list[:]
        else:
            self.insertion_list = []  # содержит переменные с размером вставок.
        self.insertion_img_list = []
        self.type = insertion
        self.insertion_forms = {
            1: [1, 0],  # секция (1) вставка (0) Одна вставка нижняя
            2: [0, 1, 0],  # вставка секция вставка Две вставки
            3: [0, 1, 0, 1, 0],  # вставка секция вставка Три вставки
            21: [1, 0, 1],  # Одна средняя вставка
            22: [1, 0, 1, 0, 1],  # Две средние вставки
            23: [1, 0, 1, 0, 1, 0, 1],  # Три среднии вставка
        }

        self.insertion = self.insertion_forms[self.type].count(0)  # количество вставок
        self.section = self.insertion_forms[self.type].count(1)  # количество секций

        _insertion = self.insertion
        if len(self.insertion_list) == 0:
            while _insertion:
                insertion_size = [tkinter.IntVar(), 'None']
                insertion_size[0].set(200)
                self.insertion_list.append(insertion_size)
                _insertion -= 1

        self.mat_dict = {}
        self.parts = {}
        self.mat_indicator = 0
        self.make_form()

    def make_form(self, copy=False):
            sum_ins = 0
            for ins in self.insertion_list:
                sum_ins += ins[0].get() / self.delim + self.padd

            try:
                self.img_ldsp = Image.open(os.path.join(settings.mater_img, 'wfon.jpg'))
                self.img_mirror = Image.open(os.path.join(settings.mater_img, 'gfon.jpg'))

                if self.type > 22:
                    y_size = int((self.y_size - sum_ins) / self.section - self.padd)
                elif self.type > 21:
                    y_size = int((self.y_size - sum_ins) / self.section - self.padd)
                elif self.type > 20:
                    y_size = int((self.y_size - sum_ins) / self.section) - self.padd
                elif self.type > 1:
                    y_size = int((self.y_size - sum_ins) / (self.insertion - 1))
                else:
                    y_size = int((self.y_size - sum_ins)) - self.padd

                self.img_ldsp = self.img_ldsp.resize((self.x_size-1, y_size-1), Image.ANTIALIAS)
                self.img_mirror = self.img_mirror.resize((self.x_size-1, y_size-1), Image.ANTIALIAS)

                for ins in self.insertion_list:
                    self.insertion_img_list.append(
                        [self.img_ldsp.resize((self.x_size-1, int((ins[0].get()/self.delim))-1), Image.ANTIALIAS),
                         self.img_mirror.resize((self.x_size-1, int((ins[0].get() / self.delim))-1), Image.ANTIALIAS)
                         ])
            except:
                print('Image ldsp or mirror error')

            self.ldsp = ImageTk.PhotoImage(self.img_ldsp)
            self.mirror = ImageTk.PhotoImage(self.img_mirror)
            cx = self.x_size * self.num_doors + self.num_doors*self.padd + self.padd * 3 + 60
            cy = self.y_size + self.padd * 5 + self.padd * (self.insertion - 2)
            self.canvas = tkinter.Canvas(self.frame, width=cx, height=cy)

            x1 = 10
            y1 = 10
            x2 = x1 + self.x_size
            y2 = y1 + self.y_size - self.padd

            self.door_width = x1+(self.x_size+self.padd)*self.num_doors + (1 * self.num_doors)

            sum_ins = 0
            for ins in self.insertion_list:
                sum_ins += ins[0].get() / self.delim

            if self.type > 20:
                door_height = y1 + sum_ins + self.img_ldsp.size[1]*self.section + self.padd * len(
                    self.insertion_forms[self.type]) + self.padd
            else:
                door_height = y1 + sum_ins + self.img_ldsp.size[1] * self.section + self.padd * len(
                    self.insertion_forms[self.type])

            self.door = self.canvas.create_rectangle(x1-self.padd,
                                                     y1-self.padd,
                                                     self.door_width,
                                                     door_height)
            door_count = self.num_doors
            num_part = 1
            first_door = True
            while door_count:  # все дверу нумеруем
                insertion_count = self.insertion
                for i, type_parts in enumerate(self.insertion_forms[self.type]):
                    if type_parts == 0:  # если это вставка
                        _index = insertion_count-1
                        _photo_ldsp = ImageTk.PhotoImage(self.insertion_img_list[_index][0])
                        _photo_mirror = ImageTk.PhotoImage(self.insertion_img_list[_index][1])
                        self.insertion_photo_dict[num_part] = (_photo_ldsp, _photo_mirror)
                        #  начало блока вставки
                        _variable = self.insertion_list[_index][0].get()  # высота вставки
                        y2 = y1 + int(_variable / self.delim)
                        self.canvas.create_rectangle(x1, y1, x2, y2)  # рисуем двери

                        if not copy:  # если это не копия
                            # запоминаем материал каждой двери и противоположный
                            self.mat_dict[num_part] = (self.insertion_photo_dict[num_part][0], 'ЛДСП',
                                                       self.insertion_photo_dict[num_part][1], 'Зеркало')

                        x = x1 + 0.5 + self.insertion_img_list[_index][0].size[0] / 2
                        y = y1 + 0.5 + self.insertion_img_list[_index][0].size[1] / 2
                        self.parts[num_part] = (
                            self.canvas.create_image(x, y, image=self.insertion_photo_dict[num_part][0]),
                            self.canvas.create_text(x, y, text='ЛДСП')
                        )
                        if len(self.insertion_forms[self.type]) - 1 != i:
                            y1 = y2 + self.padd

                        insertion_count -= 1
                        num_part += 1
                        #  конец блока вставки
                        if first_door and self.need_entry:  # если это первая дверь
                            _var = self.insertion_list[_index]
                            ent = tkinter.Entry(textvariable=_var[0])
                            ent.bind('<FocusOut>', lambda event, v=_var: self.change_size_insertion(event, v))
                            ent.bind('<Return>', lambda event, v=_var: self.change_size_insertion(event, v))
                            self.insertion_list[_index][1] = ent
                            self.canvas.create_window((x + self.door_width, y), width=50, window=ent)

                    else:  # Если это секция
                        #  начало блока секции
                        y2 = y1 + self.img_ldsp.size[1] + 1
                        self.canvas.create_rectangle(x1, y1, x2, y2)  # рисуем двери

                        if not copy:
                            self.mat_dict[num_part] = (self.mirror, 'Зеркало', self.ldsp, 'ЛДСП')

                        x = x1 + 0.5 + self.img_ldsp.size[0] / 2
                        y = y1 + 0.5 + self.img_ldsp.size[1] / 2
                        self.parts[num_part] = (
                            self.canvas.create_image(x, y, image=self.mat_dict[num_part][0]),
                            self.canvas.create_text(x, y, text=self.mat_dict[num_part][1])
                        )
                        if len(self.insertion_forms[self.type]) - 1 != i:
                            y1 = y2 + self.padd
                        num_part += 1
                        #  конец блока секции

                x1 = x1 + self.padd + self.img_ldsp.size[0] + self.padd / 2
                x2 = x1 + self.padd + self.img_ldsp.size[0] - self.padd / 2
                y1 = 10
                door_count -= 1
                first_door = False

                if self.need_entry:
                    self.create_binds()  # создать привязки смены материала, определён в ChangeMixin

    def change_size_insertion(self, event, var):
        var[1].destroy()
        sum_ins = 0
        for ins in self.insertion_list:
            sum_ins += ins[0].get() / self.delim + self.padd
        if sum_ins*self.delim > self.opening_h or var[0].get() < 50:
            var[0].set(300)
        self.insertion_img_list = []
        self.parts = {}
        self.canvas.destroy()
        self.make_form()
        self.frame.canvas = self.canvas
        self.frame.canvas.pack()

    def copy(self, object):
        object.num_doors = self.num_doors
        object.opening_h = self.opening_h
        object.opening_w = self.opening_w
        object.delim = self.delim
        object.x_size = self.x_size
        object.y_size = self.y_size
        object.padd = self.padd
        object.type = self.type
        object.insertion = self.insertion
        object.section = self.section
        object.insertion_list = self.insertion_list[:]
        object.mat_dict = self.mat_dict.copy()
        object.mat_indicator = self.mat_indicator
        object.door_width = self.door_width
        object.img_ldsp = self.img_ldsp
        object.img_mirror = self.img_ldsp
        # object.ldsp = self.ldsp
        # object.mirror = self.mirror
        object.insertion_photo_dict = self.insertion_photo_dict.copy()


