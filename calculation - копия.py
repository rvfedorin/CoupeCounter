import tkinter
import os
from PIL import Image, ImageTk, ImageFont, ImageDraw
import tkinter.messagebox as mbox
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm

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
        self.context_for_template = {}
        self.doc = DocxTemplate("template.docx")
        self.forms_template = {  # 1 - секция, 0 - вставка
                            '1FormNoSection.png': [1],
                            '2FormTwoSection.png': [1, 1],
                            '3treesection.png': [1, 1, 1],
                            '4FormFourSection.png': [1, 1, 1, 1],
                            '5twoinsert.png': [0, 1, 0],
                            '6treeinsert.png': [0, 1, 0, 1, 0],
                            '7onemiddleinsert.png': [1, 0, 1],
                            '8twomiddleinsert.png': [1, 0, 1, 0, 1],
                            '9treemiddleinsert.png': [1, 0, 1, 0, 1, 0, 1],
                            '91onebottominsert.png': [1, 0],
                            }
        self.form = self.main_frame.form_material.form  # наприме 1FormNoSection.png
        self.doors = int(self.main_frame.param_door.amount_doors.get())  # количество дверей

        #  Заголовок
        self.title_txt = f'Профиль {self.main_frame.door_handle.type_handle.get()}, ' \
                         f'{self.main_frame.door_handle.color_handle.get()}, ' \
                         f'{self.main_frame.sys_door.system_doors_name}'

        self.context_for_template['profil'] = self.main_frame.door_handle.type_handle.get()
        self.context_for_template['color'] = self.main_frame.door_handle.color_handle.get()
        self.context_for_template['system'] = self.main_frame.sys_door.system_doors_name

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

        img = os.path.join(f'{settings.system_doors_path_img}', self.main_frame.sys_door.system_doors_img)
        self.context_for_template['img_system'] = InlineImage(self.doc, img, width=Mm(40))

        self.prof_img = self.main_frame.door_handle.prof_img
        self.canvas.create_image(200, 78, image=self.prof_img)

        img = os.path.join(f'{settings.handles}/{self.main_frame.sys_door.system_doors_name}',
                           f'{self.main_frame.door_handle.type_handle.get()}.png')
        self.context_for_template['img_handle'] = InlineImage(self.doc, img, width=Mm(40))

        self.param_txt = f"""
Высота проёма: {self.main_frame.param_door.height_var.get()}
Ширина проёма: {self.main_frame.param_door.width_var.get()}
Количество дверей: {self.doors}
Мест перекрытия: {self.main_frame.param_door.amount_opening.get()}
        """
        self.context_for_template['height'] = self.main_frame.param_door.height_var.get()
        self.context_for_template['width'] = self.main_frame.param_door.width_var.get()
        self.context_for_template['doors'] = self.main_frame.param_door.amount_doors.get()
        self.context_for_template['overlaps'] = self.main_frame.param_door.amount_opening.get()

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
        self.context_for_template['formul'] = 'требуется формула'
        y = self.create_table(self.data)

        # шегель, если есть
        shag = self.main_frame.param_door.need_tape.get()

        if shag:
            self.shagel_txt = 'Размеры с учётом «шлегеля», 25м'
            self.shagel_text = TextDecor(self, wrap='word', height=1, width=40)
            self.shagel_text.insert('end', self.shagel_txt)
            self.canvas.create_window(300, y+10, window=self.shagel_text)

            self.context_for_template['shagelshagel'] = self.shagel_txt

            y += 10

        #  Изображение дверей
        _to_create = self.main_frame.form_material.to_create

        self.data_form = _to_create[0](self, self.doors, _to_create[1], need_entry=False)
        self.main_frame.form_material.form_class.copy(self.data_form)
        self.data_form.make_only_view()
        self.canvas.create_window(270, y + self.data_form.y_size/2 + 10, window=self.data_form.canvas)

        self.context_for_template['table'] = self.create_template_img_tabel()

        self.doc.render(self.context_for_template)
        self.doc.save("generated.docx")

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

    def create_template_img_tabel(self):
        num_part = 1
        table = []
        rows = []
        doors = self.doors
        img_ldsp = Image.open('system_doors/img_material/w.png').resize((
            self.data_form.img_ldsp.size[0],
            self.data_form.img_ldsp.size[1]), Image.ANTIALIAS)
        img_mirror = Image.open('system_doors/img_material/g.jpg').resize((
            self.data_form.img_mirror.size[0],
            self.data_form.img_mirror.size[1]), Image.ANTIALIAS)

        # self.data_form.mat_dict[num_part]  # (phot_ldsp, 'ЛДСП', phot_mirror, 'Зеркало')
        while doors:
            for i in self.forms_template[self.form]:
                mat = self.data_form.mat_dict[num_part][1]

                if mat == 'Зеркало':
                    if i == 0:
                        self.create_text_in_img('system_doors/img_material/g.jpg', mat, num_part)
                        _app = InlineImage(self.doc, f"temp/{num_part}.png")
                    else:
                        self.create_text_in_img(img_mirror, mat, num_part, notopened=False)
                        _app = InlineImage(self.doc, f"temp/{num_part}.png")
                else:
                    if i == 0:
                        self.create_text_in_img('system_doors/img_material/w.png', mat, num_part)
                        _app = InlineImage(self.doc, f"temp/{num_part}.png")
                    else:
                        self.create_text_in_img(img_ldsp, mat, num_part, notopened=False)
                        _app = InlineImage(self.doc, f"temp/{num_part}.png")

                rows.append(_app)

                num_part += 1

            doors -= 1
            table.append(rows)
            rows = []

        return self.reverse_list(table)

    def reverse_list(self, list):
        temp = []
        result = []
        len_c = len(list[0])
        count = 0
        while len_c:
            for i in list:

                temp.append(i[count])
            result.append(temp)
            temp = []
            count += 1
            len_c -= 1

        return result

    def create_text_in_img(self, image, text, num_part, notopened=True):
        if notopened:
            image = Image.open(image)
        else:
            image = image
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype("data/arial.ttf", 10)
        draw.text((10, 10), text, font=font, fill=(0, 0, 0))
        image.save(f"temp/{num_part}.png")


