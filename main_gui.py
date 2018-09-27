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
        self.pack(side='top')

    def make_widget(self):
        self.image = Image.open(os.path.join(settings.system_doors_path_img, self.system_doors_img))
        self.photo = ImageTk.PhotoImage(self.image)
        self.label = tkinter.Label(self, image=self.photo)
        self.label.pack()
        self.button_chage = tkinter.Button(self, text="Выбрать систему", command=lambda: SystemDoorsChange(self))
        self.button_chage.pack()

    def refresh(self):
        self.label.destroy()
        self.button_chage.destroy()
        self.make_widget()


if __name__ == '__main__':
    import sys

    root = tkinter.Tk()
    root.title('Расчет дверей купе.')
    # root.iconbitmap('data/firm.ico')
    root.minsize(width=300, height=265)
    root.resizable(width=False, height=False)

    #  START Layout
    SystemDoors()
    # END Layout
    root.mainloop()
