import tkinter
from PIL import Image, ImageTk
import os

# my models
from form_view_classes import *
import tools


class FormsChange(tkinter.Toplevel):
    def __init__(self, main_frame, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title('Выбор системы.')
        self.main_frame = main_frame
        self._buttons = []
        self.btn_frames = []
        self.photos = []
        self.all_forms = None
        self.name_list = {
            'FormNoSection.png': 'Без секций',
            'FormTwoSection.png': 'Две секции',
            'treesection.png': 'Три секции',
            'FormFourSection.png': 'Четыре секции',
            'onebottominsert.png': 'Одна вставка нижняя',
            'onemiddleinsert.png': 'Одна вставкм средняя',
            'treeinsert.png': 'Три вставки',
            'treemiddleinsert.png': 'Три среднии вставки',
            'twoinsert.png': 'Две вставки',
            'twomiddleinsert.png': 'Две средние вставки',
        }
        self.make_widget()

    def make_widget(self):
        _line = 4
        btn_frame = tkinter.Frame(self)
        self.geometry('+20+20')
        btn_frame.pack()
        try:  # open dir with images forms and save all png to variable
            self.all_forms = [f for f in os.listdir(settings.form_img) if f.endswith('.png')]
        except:
            print('error open form')
        for new_form in self.all_forms:
            if _line == 0:
                btn_frame = tkinter.Frame(self)
                btn_frame.pack()
                self.btn_frames.append(btn_frame)
                _line = 4
            row_but = tkinter.Frame(btn_frame, pady=10)
            row_but.pack(side='left')
            image = Image.open(os.path.join(settings.form_img, new_form))
            image = image.resize((150, 240), Image.ANTIALIAS)
            photo = ImageTk.PhotoImage(image)
            _b = tkinter.Button(
                row_but,
                image=photo,
                text=new_form,
                relief='flat',
                command=lambda _name=new_form: self.change(_name))

            _b.pack(side='top')
            _lab = tkinter.Label(row_but, text=self.name_list[new_form], font='Helvetica 10')
            _lab.pack(side='top')
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
        self.section = None
        self.form = 'FormNoSection.png'
        self.form_class = None
        self.form_list = {
            'FormNoSection.png': FormNoSection,
            'FormTwoSection.png': FormTwoSection,
            'treesection.png': TreeSection,
            'FormFourSection.png': FormFourSection,
            'onebottominsert.png': OneBottomInsert,
            'onemiddleinsert.png': OneMiddleInsert,
            'treeinsert.png': TreeInsert,
            'treemiddleinsert.png': TreeMiddleInsert,
            'twoinsert.png': TwoInsert,
            'twomiddleinsert.png': TwoMiddleInsert,
        }
        self.var_bolt = {'С болтом': 'with_bolt.png', 'Без болта': 'notbolt.png'}
        self.type_bolt = tkinter.StringVar()
        self.type_bolt.set('С болтом')  # default value
        self.bolt_frames = []

        self.make_widget()

    def make_widget(self):
        if self.section:
            self.create_bolt_section()

        self.label_mat = tkinter.Label(self,
                                   text=f"{4 if self.section else 3}. Выбрерите наполнение для дверей: ",
                                   bg='#1ad924', width=50)
        self.label_mat.pack()

        self.form_class = self.form_list[self.form](self)
        self.canvas = self.form_class.canvas
        self.text = self.canvas.create_text(100, 10, text=f"{self.form}")
        self.canvas.pack()

    def create_bolt_section(self):
        row = tkinter.Frame(self, relief='ridge', bd=1)
        row.pack(side='top', fill='x')
        self.bolt_frames.append(row)
        self.label = tkinter.Label(row,
                                   text=f"3. Выберите профиль вертикальной ручки: ",
                                   bg='#1ad924', width=50)
        self.label.pack()

        self.option = tools.MyOptionMenu(
            row,
            self.type_bolt,
            *self.var_bolt,
            command=lambda new_img=self.type_bolt.get(): self.change_img_bolt(new_img))

        self.option.pack(side='right')
        self.mes = tkinter.Message(row, text='Межсекционный профиль: ', width=250)
        self.mes.pack(side='left')

        row = tkinter.Frame(self, relief='ridge', bd=1)
        row.pack(side='top', fill='x')
        self.image = Image.open(
            os.path.join(settings.bolt, f'{self.var_bolt[self.type_bolt.get()]}'))
        self.image = self.image.resize((120, 60), Image.ANTIALIAS)
        self.bolt_img = ImageTk.PhotoImage(self.image, row)
        self.bolt = tkinter.Label(row, image=self.bolt_img)
        self.bolt.pack(side='bottom')
        self.bolt_frames.append(row)

    def refresh(self, new_form):
        if self.form != 'FormNoSection.png':
            for fr in self.bolt_frames:
                fr.destroy()
        if new_form != 'FormNoSection.png':
            self.section = True
        else:
            self.section = None

        self.canvas.destroy()
        self.label_mat.destroy()
        self.form = new_form
        self.make_widget()

    def change_img_bolt(self, new_img):
        self.type_bolt.set(new_img)
        for fr in self.bolt_frames:
            fr.destroy()
        self.create_bolt_section()

        self.canvas.forget()
        self.label_mat.forget()
        self.label_mat.pack()
        self.canvas.pack()



