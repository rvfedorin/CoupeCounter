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
        self.insertion = self.forms_template[self.form].count(0)
        self.section = self.forms_template[self.form].count(1)
        self.doors = int(self.main_frame.param_door.amount_doors.get())  # количество дверей
        self.prof = self.main_frame.door_handle.type_handle.get()
        self.color = self.main_frame.door_handle.color_handle.get()
        self.system = self.main_frame.sys_door.system_doors_name
        self.bolt = self.main_frame.form_material.type_bolt.get()
        self.door_height = int(self.main_frame.param_door.height_var.get())
        self.door_width = int(self.main_frame.param_door.width_var.get()) / 2

        #  Заголовок
        self.title_txt = f'Профиль {self.prof}, ' \
                         f'{self.color}, ' \
                         f'{self.system}'

        self.text = TextDecor(self, wrap='word', height=1, width=len(self.title_txt))
        self.text.insert('end', self.title_txt)
        self.text.tag_add('title', 1.0, '1.end')
        self.text.tag_config('title', font='Arial 10 bold', justify='center')

        #  Система (изображение), профиль (изображение), параметры
        self.sys_img = self.main_frame.sys_door.image
        self.sys_img = self.sys_img.resize((120, 60), Image.ANTIALIAS)
        self.sys_img = ImageTk.PhotoImage(self.sys_img)
        self.canvas.create_image(80, 78, image=self.sys_img)

        self.prof_img = self.main_frame.door_handle.prof_img
        self.canvas.create_image(200, 78, image=self.prof_img)

        self.param_txt = f"""
Высота проёма: {self.door_height}
Ширина проёма: {self.main_frame.param_door.width_var.get()}
Количество дверей: {self.doors}
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

        self.data_form = _to_create[0](self, self.doors, _to_create[1], need_entry=False)
        self.main_frame.form_material.form_class.copy(self.data_form)
        self.data_form.make_only_view()
        self.canvas.create_window(270, y + self.data_form.y_size/2 + 10, window=self.data_form.canvas)

        self.create_out()

        # кнопака выход
        self.button_exit = tkinter.Button(self, text='Выход', command=self.destroy)
        self.button_exit.pack(padx=10, pady=10, side='right')

    def create_table(self, rows: tuple, y=140):  # таблица для канваса
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

    def create_out(self):  # Созднание вывода в html
        table = self.create_template_tabel()
        body = f"""
<body>
<center>
<div id="sheet">
﻿<strong>Профиль {self.prof}, {self.color}, {self.system}</strong><br><br>
<div class="showLogoPar">
  <div class="showLogoWww">
    <img src="pic/sysknop/Absolut.png"  />
    <img src="pic/profcut/Absolut/Laguna.png" />
  <p class="clr"></p>
  </div>
  <div class="showPar">
    <span>Высота проёма: {self.main_frame.param_door.height_var.get()}</span><br />
    <span>Ширина проёма: {self.main_frame.param_door.width_var.get()}</span><br />
    <span>Количество дверей: {self.doors}</span><br />
    <span>Мест перекрытия: {self.main_frame.param_door.amount_opening.get()}</span><br />
  </div>
</div>
  <table id='counttable' cellspacing=0 cellpading=5>
    <tr> 
      <td class='rightborder'>Размер двери: </td>
      <td class='bb'><strong><i>2460 x 218мм. НУЖНА ФОРМУЛА</i></strong></td>
    </tr>
    <tr>
      <td class='rightborder'>Размер плиты 10мм: </td>
      <td class='bb'><strong>1199 x 179мм. - 7шт. НУЖНА ФОРМУЛА</strong></td>
    </tr>
    <tr>
      <td class='rightborder'>Размер зеркала (стекла) 4мм: </td>
      <td class='bb'><strong>1197 x 177мм. - 7шт. НУЖНА ФОРМУЛА</strong></td>
    </tr>
    <tr>
      <td  class='rightborder'>Длина вертикального профиля: </td>
      <td><strong>2460мм. НУЖНА ФОРМУЛА</strong></td>
    </tr>
    <tr>
      <td class='rightborder'>Длина горизонтального и межсекционного профиля: </td>
      <td><strong>164мм. НУЖНА ФОРМУЛА</strong></td>
    </tr>
    <tr>
      <td  class='rightborder'>Межсекционный профиль: </td>
      <td><strong>{self.bolt}</strong></td>
    </tr>
    <tr>
      <td class='rightborder'>Длина силиконового уплотнителя для зеркала:</td>
      <td><strong>19м.</strong></td>
    </tr>
  </table>
  """
        body += """
  <br>Размеры с учётом &laquo;шлегеля&raquo;, 34м<br><br>
  <table id="jvdoor" width="250" height="417">
  """
        for row in table:
            body += '\n<tr>'
            for col in row:
                body += f'{col}\n'
            body += '\n</tr>'

        body += '\n</table>'

        print(body)

    def create_template_tabel(self):
        num_part = 1
        table = []
        rows = []
        doors = self.doors
        mat_ldsp = f'{settings.mater_img}/g.jpg'
        mat_mirror = f'{settings.mater_img}/w.png'

        insertion_var_list = self.main_frame.form_material.form_class.insertion_list

        if self.insertion:
            sum_ins = 0
            for ins in insertion_var_list:
                sum_ins += ins[0].get()
            height_sec = (self.door_height - sum_ins) / (10 + self.section)  # высота секции
        else:
            height_sec = ''

        while doors:
            insertion = 0
            for i in self.forms_template[self.form]:
                mat = self.data_form.mat_dict[num_part][1]

                if mat == 'Зеркало':
                    if i == 0:
                        height = insertion_var_list[insertion]/10
                        _app = f'<td background="{mat_mirror}" width="36" height="{height}"><center><span>Зеркало:<br>1197 x 177</span></td>'
                    else:
                        _app = f'<td background="{mat_mirror}" width="36" height="{height_sec}"><center><span>Зеркало:<br>1197 x 177</span></td>'
                else:
                    if i == 0:
                        height = insertion_var_list[insertion]/10
                        _app = f'<td background="{mat_ldsp}" width="36" height="{height}><center><span>ЛДСП:<br>1199 x 179</span></td>'
                    else:
                        _app = f'<td background="{mat_ldsp}" width="36" height="{height_sec}"><center><span>ЛДСП:<br>1199 x 179</span></td>'

                insertion += 1
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