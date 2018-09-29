# ver 1.0.0
# created by Roman Fedorin
import tkinter

#  my modules ======================
from systems_tools import SystemDoors, SystemDoorsChange
from parametrs_tools import ParametersDoorOpening
from handle_tools import DoorHandle
from form_material import FormAndMaterial, FormsChange


class MainFrame(tkinter.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pack(fill='x')
        self.sys_door = SystemDoors(self)
        self.param_door = ParametersDoorOpening(self)
        self.door_handle = DoorHandle(self, self)
        self.form_material = FormAndMaterial(self, self)

        self.button_change_system = tkinter.Button(self,
                                                   text="Выбрать систему",
                                                   command=lambda: SystemDoorsChange(self))
        self.button_change_form = tkinter.Button(self,
                                            text="Выбрать конфигурацию дверей.",
                                            command=lambda: FormsChange(self))

        self.button_change_system.pack(side='left', pady=4)
        self.button_change_form.pack(side='right', pady=4)


if __name__ == '__main__':
    # import sys

    root = tkinter.Tk()
    root.title('Расчет дверей купе.')
    root.geometry('+10+10')
    # root.iconbitmap('data/firm.ico')
    root.minsize(width=250, height=265)
    root.resizable(width=False, height=False)

    #  START Layout
    MainFrame(root)
    # END Layout
    root.mainloop()
