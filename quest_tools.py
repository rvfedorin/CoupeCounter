from tkinter.scrolledtext import ScrolledText
from PIL import Image, ImageTk
import os
import tkinter

# my models
import settings


class HelpTape(tkinter.Toplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Что такое буферная лента в конструкции дверей-купе.")
        self.text = tkinter.Text(self, wrap='word', height=40, width=100)
        self.text_p1 = """
        Что такое буферная лента в конструкции дверей-купе?

 Что такое "шлегель", о котором всё время упоминается при расчётах дверей-купе?
 Двери в шкаф-купе делаются из алюминиевого профиля, а алюминий довольно твёрдый материал. 
 Так вот, чтобы двери не стучали по стенкам, на торец двери клеится так называемая "буферная лента".
 Буферной лентой называется лента с ворсом (высота ворса - 6мм и 10мм). 
 Буферная лента с ворсом 6 мм предназначена для смягчения удара двери-купе о стенку шкафа при закрывании. 
 Буферная лента с ворсом 10мм клеится не на торец двери, а на заднюю сторону профиля, 
 и цель её перекрыть щель между дверями в местах перекрытия, чтобы защитить шкаф от пыли. 
 Эту ленту ещё называют "пыльником".
        """
        self.text_p2 = """
 А что на счёт "шлегеля", спросите вы? 
 Шлегель - это название фирмы, которая занимается изготовлением различных уплотнителей для окон и дверей, 
 в том числе и изготовлением той самой буферной ленты для раздвижных дверей (то есть для дверей-купе). 

 История похожа на ту, когда скотчем начали называть клейкую ленту, которую производила фирма под названием "Скотч". 
 Так и здесь - Шлегель стал синонимом торцевой буферной ленты. 
 Сказать шлегель проще, чем говорит "буферная лента", и ещё уточнять: на торец или для защиты от пыли. 
 А так всё просто: "Дайте мне 6 метров "шлегеля" и 3 метра "пыльника". И всё понятно!
        """
        self.text.insert(1.0, self.text_p1)
        self.text.tag_add('title', 2.0, '2.end')
        self.text.tag_config('title', font=('bold',))
        self.image = Image.open(os.path.join(settings.help_img, 'tape_schem.png'))
        self.photo = ImageTk.PhotoImage(self.image)
        self.img = tkinter.Label(self, relief='flat', bd=0, image=self.photo)
        self.text.window_create(tkinter.INSERT, window=self.img)
        self.text.insert('end', self.text_p2)
        self.text.pack(fill='x')


class HelpOpening(tkinter.Toplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Что такое места перекрытия в конструкции дверей-купе?.")
        self.text = ScrolledText(self, wrap='word', height=40, width=120)
        self.text_p1 = """
    Что такое места перекрытия в конструкции дверей-купе?
    
 Двери-купе перемещаются относительно друг друга по соседним полозьям, 
 и чтобы внешне фасад шкафа-купе смотрелся нормально, край передней двери перекрывает край соседней двери 
 на ширину профиля. Это и называется "местом перекрытия".
 Если в проём встраиваются две двери, между дверями создаётся одно место перекрытия. 
 Если встраиваются три двери, получается два места перекрытия. 
 Если встраиваются четыре двери, мест перекрытий может быть и три, а может быть и два. 
 Пять дверей - четыре места перекрытия. На рисунке внизу всё показано наглядно.
 Чаще всего мест перекрытий бывает на один меньше, чем дверей, но бывают и исключения, как на примере четырёх дверей. 
 Поэтому нужно быть внимательным при заполнении формы параметров дверей-купе
               """

        self.text.insert(1.0, self.text_p1)
        self.text.tag_add('title', 2.0, '2.end')
        self.text.tag_config('title', font=('bold',))
        self.image = Image.open(os.path.join(settings.help_img, 'opening_schem.png'))
        self.photo = ImageTk.PhotoImage(self.image)
        self.img = tkinter.Label(self, relief='flat', bd=0, image=self.photo)
        self.text.window_create(tkinter.INSERT, window=self.img)
        self.text.insert('end', ' ')
        self.text.pack(fill='x', side='left')