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
        self.param_door = ParametersDoorOpening(self, self)
        self.door_handle = DoorHandle(self, self)
        self.form_material = FormAndMaterial(self, self)

        self.button_change_system = tkinter.Button(self,
                                                   text="Выбрать систему",
                                                   command=lambda: SystemDoorsChange(self))
        self.button_change_form = tkinter.Button(self,
                                            text="Выбрать конфигурацию дверей.",
                                            command=lambda: FormsChange(self),
                                                 )

        self.button_change_system.pack(side='left', pady=4, padx=4)
        self.button_change_form.pack(side='right', pady=4, padx=4)

    def change_form(self, event):
        form_list = self.form_material.form_list[self.form_material.form]  # '1FormNoSection.png': (FormSection, 0),
        form = form_list[0]
        sec = form_list[1]
        doors = int(self.param_door.amount_doors.get())
        self.form_material.canvas.destroy()
        insertions = self.form_material.form_class.insertion_list
        self.form_material.form_class = form(self.form_material, doors, sec, insertions)
        self.form_material.canvas = self.form_material.form_class.canvas
        self.form_material.canvas.pack()

    def change_size_open(self, event):
        form_list = self.form_material.form_list[self.form_material.form]  # '1FormNoSection.png': (FormSection, 0),
        form = form_list[0]
        sec = form_list[1]
        doors = int(self.param_door.amount_doors.get())

        if int(self.param_door.width_var.get()) > 5000 or int(self.param_door.width_var.get()) < 1500:
            self.param_door.width_var.set('1500')
        if int(self.param_door.height_var.get()) > 5000 or int(self.param_door.height_var.get()) < 1000:
            self.param_door.height_var.set('2500')

        self.form_material.canvas.destroy()
        self.form_material.form_class = form(self.form_material, doors, sec)
        self.form_material.canvas = self.form_material.form_class.canvas
        self.form_material.canvas.pack()


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
