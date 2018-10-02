import tkinter
import os
from PIL import Image, ImageTk

import settings
from handle_tools import DoorHandle


class SystemDoorsChange(tkinter.Toplevel):
    def __init__(self, main_frame, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title('Выбор системы.')
        self.main_frame = main_frame
        self._buttons = []
        self.btn_frames = []
        self.photos = []
        self.make_widget()

    def make_widget(self):
        _line = 4
        btn_frame = tkinter.Frame(self, bg='green')
        btn_frame.pack()
        for system_door in self.main_frame.sys_door.all_system_doors:
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
        #  Перерисовываем и менякм систему
        self.main_frame.sys_door.system_doors_img = new_system_doors
        self.main_frame.sys_door.refresh()

        #  Перерисовываем блок профиля вертикальной ручки
        self.main_frame.door_handle.destroy()
        self.main_frame.door_handle = DoorHandle(self.main_frame, self.main_frame)  # как фрейм и как объект

        #  Перересовывакм блок профиля вертикальной ручки
        self.main_frame.form_material.forget()
        self.main_frame.form_material.pack()

        #  Перерисовываем кнопки
        self.main_frame.button_change_system.forget()
        self.main_frame.button_change_form.forget()
        self.main_frame.button_calculation.forget()
        self.main_frame.button_change_system.pack(side='left', pady=4, padx=10)
        self.main_frame.button_change_form.pack(side='right', pady=4, padx=4)
        self.main_frame.button_calculation.pack(side='right', pady=4, padx=4)


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
        self.system_doors_name = self.system_doors_img[:-3]  # take name system as default ([:-3] - extension cut)
        self.make_widget()
        self.pack(side='top', fill='x')

    def make_widget(self):
        self.system_doors_name = self.system_doors_img[:-3]
        self.image = Image.open(os.path.join(settings.system_doors_path_img, self.system_doors_img))
        self.photo = ImageTk.PhotoImage(self.image)
        self.label = tkinter.Label(self, image=self.photo)
        self.label.pack()

    def refresh(self):
        self.label.destroy()
        self.make_widget()
