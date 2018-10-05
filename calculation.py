import tkinter
import os
from PIL import Image, ImageTk
from template_tools import CreateHtmlTemplate

import settings


class TextDecor(tkinter.Text):
    def __init__(self, *args, **kwargs):
        super().__init__(bg='gray95', relief='flat', font='Arial 9', *args, **kwargs)


class Calculation:
    def __init__(self, main_frame, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.main_frame = main_frame
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
        self.color = self.main_frame.door_handle.color_handle.get()[:-1]
        self.system = self.main_frame.sys_door.system_doors_name
        self.bolt = self.main_frame.form_material.type_bolt.get()
        self.opening_width = int(self.main_frame.param_door.width_var.get())
        self.door_height = int(self.main_frame.param_door.height_var.get())
        self.door_width = self.opening_width / 2
        self.overlaps = self.main_frame.param_door.amount_opening.get()
        self.pic_system = os.path.join(settings.system_doors_path_img, f'{self.system}.png')
        self.pic_profile = os.path.join(f'{settings.handles}/{self.system}', f'{self.prof}.png')

        self.create_out()

    def create_out(self):  # Созднание вывода в html
        table = self.create_template_tabel()
        body = CreateHtmlTemplate()
        body.bolt = self.bolt
        body.prof = self.prof
        body.color = self.color
        body.system = self.system
        body.door_height = self.door_height
        body.opening_width = self.opening_width
        body.overlaps = self.overlaps
        body.doors = self.doors
        body.pic_system = self.pic_system
        body.pic_profile = self.pic_profile

        temp = '<table id="jvdoor" width="250" height="417"><tbody>'
        for row in table:
            temp += '\n<tr>'
            for col in row:
                temp += f'{col}\n'
            temp += '\n</tr>'
        temp += '\n</tbody></table>'

        body.table_doors_view = temp
        body.create_body()
        body('</body>')
        body.save()
        body.open_calc()

    def create_template_tabel(self):
        num_part = 1
        table = []
        rows = []
        doors = self.doors

        insertion_var_list = self.main_frame.form_material.form_class.insertion_list

        if self.insertion:
            sum_ins = 0
            for ins in insertion_var_list:
                sum_ins += ins[0].get()
            height_sec = (self.door_height - sum_ins) / self.section / 10  # высота секции
        else:
            height_sec = self.door_height / self.section / 10

        while doors:
            insertion = 0
            for i in self.forms_template[self.form]:
                mat = self.main_frame.form_material.form_class.mat_dict[num_part][1]
                if mat == 'Зеркало':
                    if i == 0:
                        height = insertion_var_list[insertion][0].get()/10
                        insertion += 1
                        _app = f"""<td class="gfon" height="{int(height)}">
                        <center><span>Зеркало:<br>{int(height*10)} x 177</span></td>"""
                    else:
                        _app = f"""<td class="gfon" height="{int(height_sec)}">
                        <center><span>Зеркало:<br>{int(height_sec*10)} x 177</span></td>"""
                else:
                    if i == 0:
                        height = insertion_var_list[insertion][0].get()/10
                        insertion += 1
                        _app = f"""<td class="wfon" height="{int(height)}">
                        <center><span>ЛДСП:<br>{int(height*10)} x 179</span></td>"""
                    else:
                        _app = f"""<td class="wfon" height="{int(height_sec)}">
                        <center><span>ЛДСП:<br>{int(height_sec*10)} x 179</span></td>"""

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
