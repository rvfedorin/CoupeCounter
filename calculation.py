import tkinter
import os
from PIL import Image, ImageTk
import tkinter.messagebox as mbox

import settings


class TextDecor(tkinter.Text):
    def __init__(self, *args, **kwargs):
        super().__init__(bg='gray95', relief='flat', font='Arial 9', *args, **kwargs)


class Calculation(tkinter.Toplevel):
    def __init__(self, main_frame, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title('Расчёт.')
        self.main_frame = main_frame
        self.canvas = tkinter.Canvas(self, width=500, height=500)
        self.canvas.pack()

        #  Заголовок
        self.title_txt = f'Профиль {self.main_frame.door_handle.type_handle.get()}, ' \
                         f'{self.main_frame.door_handle.color_handle.get()}, ' \
                         f'{self.main_frame.sys_door.system_doors_name}'
        self.text = TextDecor(self, wrap='word', height=1, width=len(self.title_txt))
        self.text.insert('end', self.title_txt)
        self.text.tag_add('title', 1.0, '1.end')
        self.text.tag_config('title', font='Arial 10 bold', justify='center')
        self.canvas.create_window(250, 20, window=self.text)

        #  Система (изображение), профиль (изображение), параметры
        self.sys_img = self.main_frame.sys_door.image
        self.sys_img = self.sys_img.resize((120, 60), Image.ANTIALIAS)
        self.sys_img = ImageTk.PhotoImage(self.sys_img)
        self.canvas.create_image(80, 78, image=self.sys_img)

        self.prof_img = self.main_frame.door_handle.prof_img
        self.canvas.create_image(200, 78, image=self.prof_img)

        self.param_txt = f"""
Высота проёма: {self.main_frame.param_door.height_var.get()}
Ширина проёма: {self.main_frame.param_door.width_var.get()}
Количество дверей: {self.main_frame.param_door.amount_doors.get()}
Мест перекрытия: {self.main_frame.param_door.amount_opening.get()}
        """
        self.param_text = TextDecor(self, wrap='word', height=5, width=40)
        self.param_text.insert('end', self.param_txt)
        self.canvas.create_window(450, 70, window=self.param_text)

        #  Таблица расчёта
        self.canvas.create_line(20, 120, 480, 120, dash=(4, 2))
        self.data = (
            ('Размер двери:', 'требуется формула'),
            ('Размер плиты 10мм:', 'требуется формула'),
            ('Размер зеркала (стекла) 4мм:', 'требуется формула'),
            ('Длина вертикального профиля:', 'требуется формула'),
            ('Длина горизонтального профиля (верх и низ):', 'требуется формула'),
            ('Длина силиконового уплотнителя для зеркала:', 'требуется формула'),
        )
        y = self.create_table(self.data)

        # шегель, если есть
        shag = self.main_frame.param_door.need_tape.get()

        if shag:
            self.shagel_txt = 'Размеры с учётом «шлегеля», 25м'
            self.shagel_text = TextDecor(self, wrap='word', height=1, width=40)
            self.shagel_text.insert('end', self.shagel_txt)
            self.canvas.create_window(300, y+10, window=self.shagel_text)

            y += 10

        #  Изображение дверей
        _to_create = self.main_frame.form_material.to_create
        doors = self.main_frame.form_material.doors
        self.data_form = _to_create[0](self, doors, _to_create[1], need_entry=False)
        self.main_frame.form_material.form_class.copy(self.data_form)
        self.data_form.make_only_view()
        self.canvas.create_window(270, y + self.data_form.y_size/2 + 10, window=self.data_form.canvas)

        # кнопака выход
        self.button_exit = tkinter.Button(self, text='Выход', command=self.destroy)
        self.button_exit.pack(padx=10, pady=10, side='right')


    def create_table(self, rows: tuple, y=140):
        for row in rows:
            text_name = TextDecor(self, wrap='word', height=1, width=len(row[0]))
            text_name.insert('end', row[0])

            text_value = TextDecor(self, wrap='word', height=1, width=len(row[1]))
            text_value.insert('end', row[1])

            self.canvas.create_window(20 + len(row[0])*3.5, y, window=text_name)
            self.canvas.create_window(350 + len(row[1])*3.5, y, window=text_value)
            self.canvas.create_line(20, y+15, 480, y+15)
            y += 25
        self.canvas.create_line(330, 130, 330, y-10)
        return y

