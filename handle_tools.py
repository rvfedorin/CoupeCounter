import tkinter
from PIL import Image, ImageTk
import os

# my models
import tools
import settings


class DoorHandle(tkinter.Frame):
    def __init__(self, system_instance, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pack()
        self.main_instance = system_instance
        self.files_img = []

        #  open files with images handle
        try:
            for file in os.listdir(f'{settings.handles}/{self.main_instance.sys_door.system_doors_name}'):
                if file.endswith('.png'):
                    self.files_img.append(file)
        except:
            print('not found handle')

        #  open file with colors
        try:
            with open(f'{settings.handles}/{self.main_instance.sys_door.system_doors_name}/colors.txt', 'rb') as file:
                self.colors = [col.decode()[:-1] for col in file]
        except:
            print('not found colors')

        self.pack(fill='x')
        self.label = tkinter.Label(self, text="2. Выберите профиль вертикальной ручки: ", bg='#1ad924', width=50)
        self.label.pack()
        self.row_frame = []
        self.fields = [
            f'Профиль {self.main_instance.sys_door.system_doors_name}: ',
            f'Цвет профиля {self.main_instance.sys_door.system_doors_name}: ',
        ]
        self.type_handle = tkinter.StringVar()
        self.type_handle.set(self.files_img[0][:-4])  # default value
        self.color_handle = tkinter.StringVar()
        self.color_handle.set(self.colors[0])  # default value
        self.need_tape = tkinter.IntVar()
        self.make_widget()

    def make_widget(self):
        row = tkinter.Frame(self, relief='ridge', bd=1)
        row.pack(side='top', fill='x')
        #  Изабражение профиля
        self.image = Image.open(
            os.path.join(
                f'{settings.handles}/{self.main_instance.sys_door.system_doors_name}', f'{self.type_handle.get()}.png'))
        self.image = self.image.resize((120, 60), Image.ANTIALIAS)
        self.prof_img = ImageTk.PhotoImage(self.image, row)
        self.label = tkinter.Label(row, image=self.prof_img)
        self.label.pack()
        self.row_frame.append(row)

        #  Профиль
        row = tkinter.Frame(self, relief='ridge', bd=1)
        row.pack(side='top', fill='x')
        types_prof = []
        for f_name in self.files_img:
            types_prof.append(f_name[:-4])

        option = tools.MyOptionMenu(
            row,
            self.type_handle,
            *types_prof,
            command=lambda new_img=self.type_handle.get(): self.change_img_prof(new_img))

        mes = tkinter.Message(row, text=self.fields[0], width=150)
        mes.pack(side='left')
        option.pack(side='right')
        self.row_frame.append(row)

        #  Цвет профиля
        row = tkinter.Frame(self, relief='ridge', bd=1)
        row.pack(side='top', fill='x')
        option = tools.MyOptionMenu(row, self.color_handle, *self.colors)
        mes = tkinter.Message(row, text=self.fields[1], width=200)
        mes.pack(side='left')
        option.pack(side='right')
        self.row_frame.append(row)

        self.row_frame.append(row)

    def change_img_prof(self, new_img):
        self.type_handle.set(new_img)
        for fr in self.row_frame:
            fr.destroy()
        self.make_widget()