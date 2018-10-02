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
        self.mat_indicator = None

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


class FormSection(ChangeMixin):
    def __init__(self, master_frame, num_doors=2, sec=1):
        super().__init__()
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

            self.create_binds()  # создать привязки смены материала, определён в ChangeMixin


class WithInsert(ChangeMixin):
    def __init__(self, master_frame, num_doors=2, insertion=2):
        super().__init__()
        self.frame = master_frame
        self.num_doors = num_doors
        self.opening_h = int(self.frame.main_frame.param_door.height_var.get())
        self.opening_w = int(self.frame.main_frame.param_door.width_var.get())
        self.delim = 14
        self.x_size = int(self.opening_w / (self.delim*2))
        self.y_size = int(self.opening_h / self.delim)
        self.padd = 4
        self.insertion = insertion
        self.insertion_list = []
        self.insertion_img_list = []

        _insertion = self.insertion
        while _insertion:
            insertion_size = [tkinter.IntVar(), 'None']
            insertion_size[0].set(500)
            self.insertion_list.append(insertion_size)
            _insertion -= 1

        self.mat_dict = {}
        self.parts = {}
        self.mat_indicator = 0
        self.make_form()

    def make_form(self):
            sum_ins = 0
            for ins in self.insertion_list:
                sum_ins += ins[0].get() / self.delim + self.padd

            try:
                self.img_ldsp = Image.open(os.path.join(settings.mater_img, 'wfon.jpg'))
                self.img_mirror = Image.open(os.path.join(settings.mater_img, 'gfon.jpg'))
                y_size = int((self.y_size - sum_ins)/(self.insertion - 1))
                self.img_ldsp = self.img_ldsp.resize((self.x_size-2, y_size - 2), Image.ANTIALIAS)
                self.img_mirror = self.img_mirror.resize((self.x_size - 1, y_size - 1), Image.ANTIALIAS)

                for ins in self.insertion_list:
                    self.insertion_img_list.append(
                        [self.img_ldsp.resize((self.x_size-2, int((ins[0].get()/self.delim)) - 2), Image.ANTIALIAS),
                         self.img_mirror.resize((self.x_size - 2, int((ins[0].get() / self.delim)) - 2), Image.ANTIALIAS)
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

            self.door_width = x1+(self.x_size+self.padd)*self.num_doors
            self.door = self.canvas.create_rectangle(x1-self.padd,
                                                     y1-self.padd,
                                                     self.door_width,
                                                     y1 + self.y_size + self.padd + self.padd*(self.insertion-2))

            door_count = self.num_doors
            num_part = 1
            first_door = True
            while door_count:  # все дверу нумеруем
                insertion_count = self.insertion
                while insertion_count:
                    if insertion_count == 1:  # если это последняя вставка, то после неё секция не ставится
                        _index = insertion_count-1
                        _photo_ldsp = ImageTk.PhotoImage(self.insertion_img_list[_index][0])
                        _photo_mirror = ImageTk.PhotoImage(self.insertion_img_list[_index][1])
                        #  начало блока вставки
                        _variable = self.insertion_list[_index][0].get()
                        y2 = y1 + int(_variable / self.delim)
                        self.canvas.create_rectangle(x1, y1, x2, y2)  # рисуем двери

                        # запоминаем материал каждой двери и противоположный
                        self.mat_dict[num_part] = (_photo_ldsp, 'ЛДСП', _photo_mirror, 'Зеркало')

                        x = x1 + 1 + self.img_ldsp.size[0] / 2
                        y = y1 + 1 + self.insertion_img_list[_index][0].size[1] / 2
                        self.parts[num_part] = (
                            self.canvas.create_image(x, y, image=_photo_ldsp),
                            self.canvas.create_text(x, y, text='ЛДСП')
                        )
                        y1 = y2 + self.padd
                        insertion_count -= 1
                        num_part += 1
                        #  конец блока вставки
                        if first_door:  # если это первая дверь
                            _var = self.insertion_list[_index]
                            ent = tkinter.Entry(textvariable=_var[0])
                            ent.bind('<FocusOut>', lambda event, v=_var: self.change_size_insertion(event, v))
                            ent.bind('<Return>', lambda event, v=_var: self.change_size_insertion(event, v))
                            self.insertion_list[_index][1] = ent
                            self.canvas.create_window((x + self.door_width, y), width=50, window=ent)

                    else:  # Если вставка не последняя, то после неё вставляем секцию
                        #  начало блока вставки
                        _index = insertion_count - 1
                        _photo_ldsp = ImageTk.PhotoImage(self.insertion_img_list[_index][0])
                        _photo_mirror = ImageTk.PhotoImage(self.insertion_img_list[_index][1])
                        #  начало блока вставки
                        _variable = self.insertion_list[_index][0]
                        y2 = y1 + int(_variable.get() / self.delim)
                        self.canvas.create_rectangle(x1, y1, x2, y2)  # рисуем вставку

                        self.mat_dict[num_part] = (_photo_ldsp, 'ЛДСП', _photo_mirror, 'Зеркало')

                        x = x1 + 1 + self.img_ldsp.size[0] / 2
                        y = y1 + 1 + self.insertion_img_list[_index][0].size[1] / 2
                        self.parts[num_part] = (
                            self.canvas.create_image(x, y, image=_photo_ldsp),
                            self.canvas.create_text(x, y, text='ЛДСП')
                        )
                        y1 = y2 + self.padd
                        insertion_count -= 1
                        num_part += 1
                        #  конец блока вставки

                        if first_door:  # если это первая дверь
                            _var = self.insertion_list[_index]
                            ent = tkinter.Entry(textvariable=_var[0])
                            ent.bind('<FocusOut>', lambda event, v=_var: self.change_size_insertion(event, v))
                            ent.bind('<Return>', lambda event, v=_var: self.change_size_insertion(event, v))
                            self.insertion_list[_index][1] = ent
                            self.canvas.create_window((x + self.door_width, y), width=50, window=ent)

                        #  начало блока секции
                        y2 = y1 + self.img_ldsp.size[1] + 3
                        self.canvas.create_rectangle(x1, y1, x2, y2)  # рисуем двери

                        self.mat_dict[num_part] = (self.mirror, 'Зеркало', self.ldsp, 'ЛДСП')

                        x = x1 + 1 + self.img_ldsp.size[0] / 2
                        y = y1 + 1 + self.img_ldsp.size[1] / 2
                        self.parts[num_part] = (
                            self.canvas.create_image(x, y, image=self.mat_dict[num_part][0]),
                            self.canvas.create_text(x, y, text=self.mat_dict[num_part][1])
                        )
                        y1 = y2 + self.padd
                        num_part += 1
                        #  конец блока секции

                x1 = x1 + self.padd + self.img_ldsp.size[0] + self.padd / 2
                x2 = x1 + self.padd + self.img_ldsp.size[0] - self.padd / 2
                y1 = 10
                door_count -= 1
                first_door = False

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


class WithMiddleInsert:
    def __init__(self, master_frame, num_doors=2, insertion=0):
        super().__init__()