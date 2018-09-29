import tkinter
from PIL import Image, ImageTk
import os

# my models
from form_view_classes import *


class FormsChange(tkinter.Toplevel):
    def __init__(self, main_frame, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title('Выбор системы.')
        self.main_frame = main_frame
        self._buttons = []
        self.btn_frames = []
        self.photos = []
        self.all_forms = None
        self.make_widget()

    def make_widget(self):
        _line = 4
        btn_frame = tkinter.Frame(self, bg='green')
        btn_frame.pack()
        try:  # open dir with images forms and save all png to variable
            self.all_forms = [f for f in os.listdir(settings.form_img) if f.endswith('.png')]
        except:
            print('error open form')
        for new_form in self.all_forms:
            if _line == 0:
                btn_frame = tkinter.Frame(self, bg='green')
                btn_frame.pack()
                self.btn_frames.append(btn_frame)
                _line = 4
            image = Image.open(os.path.join(settings.form_img, new_form))
            image = image.resize((150, 240), Image.ANTIALIAS)
            photo = ImageTk.PhotoImage(image)
            _b = tkinter.Button(
                btn_frame,
                image=photo,
                text=new_form,
                command=lambda _name=new_form: self.change(_name))

            _b.pack(side='left')
            _line -= 1
            self.photos.append(photo)
            self._buttons.append(_b)

    def change(self, new_form):
        self.main_frame.form_material.refresh(new_form)
        self.destroy()


class FormAndMaterial(tkinter.Frame):
    def __init__(self, main_frame, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pack()
        self.main_frame = main_frame
        self.button_chage = None
        self.label = None
        self.canvas = None
        self.num = 3
        self.section = None
        self.form = 'FormNoSection.png'
        self.form_class = None
        self.form_list = {
            'FormNoSection.png': FormNoSection,
            'FormTwoSection.png': FormTwoSection,
        }

        self.make_widget()

    def make_widget(self):
        if self.section:
            self.label = tkinter.Label(self,
                                       text=f"3. Выберите профиль вертикальной ручки: ",
                                       bg='#1ad924', width=50)
            self.label.pack()
        self.num = 4 if self.section else 3

        self.label_mat = tkinter.Label(self,
                                   text=f"{self.num}. Выбрерите наполнение для дверей: ",
                                   bg='#1ad924', width=50)
        self.label_mat.pack()

        self.form_class = self.form_list[self.form](self)
        self.canvas = self.form_class.canvas
        self.text = self.canvas.create_text(100, 10, text=f"{self.form}")
        self.canvas.pack()

    def refresh(self, new_form):
        if self.form != 'FormNoSection.png':
            self.label.destroy()
        if new_form != 'FormNoSection.png':
            self.section = True
        else:
            self.section = None

        self.canvas.destroy()
        self.label_mat.destroy()
        self.form = new_form
        self.make_widget()

