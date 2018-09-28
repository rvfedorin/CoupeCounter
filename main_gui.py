# ver 1.0.0
# created by Roman Fedorin

import tkinter
import os
from PIL import Image, ImageTk

#  my modules ======================
import settings


class SystemDoorsChange(tkinter.Toplevel):
    def __init__(self, sys_doors_inst, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title('Выбор системы.')
        self.sys_doors_inst = sys_doors_inst
        self._buttons = []
        self.btn_frames = []
        self.photos = []
        self.make_widget()

    def make_widget(self):
        _line = 4
        btn_frame = tkinter.Frame(self, bg='green')
        btn_frame.pack()
        for system_door in self.sys_doors_inst.all_system_doors:
            if _line == 0:
                btn_frame = tkinter.Frame(self, bg='green')
                btn_frame.pack()
                self.btn_frames.append(btn_frame)
                _line = 4
            image = Image.open(os.path.join(settings.system_doors_path_img, system_door))
            photo = ImageTk.PhotoImage(image)
            _b = tkinter.Button(
                btn_frame,
                image=photo,
                text=system_door,
                command=lambda _name=system_door: self.change(_name))

            _b.pack(side='left')
            _line -= 1
            self.photos.append(photo)
            self._buttons.append(_b)

    def change(self, new_system_doors):
        self.sys_doors_inst.system_doors_img = new_system_doors
        self.sys_doors_inst.refresh()
        self.destroy()


class SystemDoors(tkinter.Frame):

    def __init__(self, *args, **kwargs):
        super(SystemDoors, self).__init__(*args, **kwargs)
        self.image = None
        self.photo = None
        self.label = None
        self.button_chage = None

        try:  # open dir with images system and save all png to variable
            self.all_system_doors = [f for f in os.listdir(settings.system_doors_path_img) if f.endswith('.png')]
        except:
            print('error open ')

        self.system_doors_img = self.all_system_doors[0]  # take one from all as default
        self.system_doors_name = self.all_system_doors[0][:-3]  # take name system as default ([:-3] - extension cut)
        self.make_widget()
        self.pack(side='top', fill='x')

    def make_widget(self):
        self.image = Image.open(os.path.join(settings.system_doors_path_img, self.system_doors_img))
        self.photo = ImageTk.PhotoImage(self.image)
        self.label = tkinter.Label(self, image=self.photo)
        self.label.pack()
        self.button_chage = tkinter.Button(self,
                                           text="Выбрать систему",
                                           command=lambda: SystemDoorsChange(self))
        self.button_chage.pack(pady=4)

    def refresh(self):
        self.label.destroy()
        self.button_chage.destroy()
        self.make_widget()


class ParametersDoorOpening(tkinter.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pack(fill='x')
        self.label = tkinter.Label(self, text="1. Введите параметры проёма и дверей-купе: ", bg='#1ad924', width=50)
        self.label.pack()
        self.row_frame = []
        self.fields = [
            'Высота проёма:',
            'Ширина проёма:',
            'Количество дверей:',
            'Количество мест перекрытия:',
            'Буферная лента ("шлегель"):'
        ]
        self.amount_doors = tkinter.StringVar()
        self.amount_doors.set(1)  # default value
        self.amount_opening = tkinter.StringVar()
        self.amount_opening.set(1)  # default value
        self.need_tape = tkinter.IntVar()

        #  'Высота проёма:'
        row = tkinter.Frame(self, relief='ridge', bd=1)
        row.pack(side='top', fill='x')
        self.height = tkinter.Entry(row)
        self.height.insert(0, '2500')
        mes = tkinter.Message(row, text=self.fields[0], width=100)
        mes.pack(side='left')
        self.height.pack(side="right", pady=2)
        self.row_frame.append(row)

        #  'Ширина проёма:'
        row = tkinter.Frame(self, relief='ridge', bd=1)
        row.pack(side='top', fill='x')
        self.width = tkinter.Entry(row)
        self.width.insert(0, '1500')
        mes = tkinter.Message(row, text=self.fields[1], width=100)
        mes.pack(side='left')
        self.width.pack(side="right", pady=2)
        self.row_frame.append(row)

        #  'Количество дверей:'
        row = tkinter.Frame(self, relief='ridge', bd=1)
        row.pack(side='top', fill='x')
        list_num = [1, 2, 3, 4, 5, 6, 7, 8]
        option = tkinter.OptionMenu(row, self.amount_doors, *list_num)
        mes = tkinter.Message(row, text=self.fields[2], width=150)
        mes.pack(side='left')
        option.pack(side='right')
        self.row_frame.append(row)

        #  'Количество мест перекрытия:'
        row = tkinter.Frame(self, relief='ridge', bd=1)
        row.pack(side='top', fill='x')
        list_num = [1, 2, 3, 4, 5, 6, 7]
        option = tkinter.OptionMenu(row, self.amount_opening, *list_num)
        mes = tkinter.Message(row, text=self.fields[3], width=200)
        mes.pack(side='left')
        option.pack(side='right')
        self.row_frame.append(row)

        #  'Буферная лента ("шлегель"):'
        row = tkinter.Frame(self)
        row.pack(side='top', fill='x')
        check1 = tkinter.Checkbutton(row, variable=self.need_tape, onvalue=1, offvalue=0)
        mes = tkinter.Message(row, text=self.fields[4], width=200)
        self.image = Image.open(f'{settings.data}/quest.png')
        self.image = self.image.resize((15, 15), Image.ANTIALIAS)
        self.photo = ImageTk.PhotoImage(self.image)
        button_quest = tkinter.Button(
            row,
            relief='groove',
            image=self.photo,
            command=lambda _name='quest_tape': print(_name))

        mes.pack(side='left')
        button_quest.pack(side='left')
        check1.pack(side="right", pady=2)

        self.row_frame.append(row)


class DoorHandle(tkinter.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class MainFrame(tkinter.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pack(fill='x')
        self.sys_door = SystemDoors(self)
        self.param_door = ParametersDoorOpening(self)
        self.door_handle = DoorHandle(self)


if __name__ == '__main__':
    # import sys

    root = tkinter.Tk()
    root.title('Расчет дверей купе.')
    # root.iconbitmap('data/firm.ico')
    root.minsize(width=250, height=265)
    root.resizable(width=False, height=False)

    #  START Layout
    MainFrame(root)
    # END Layout
    root.mainloop()
