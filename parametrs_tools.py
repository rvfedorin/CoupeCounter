import tkinter

# my models
from quest_tools import HelpOpening, HelpTape
import tools


class ParametersDoorOpening(tkinter.Frame):
            def __init__(self, main_frame, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.pack(fill='x')
                self.label = tkinter.Label(self,
                                           text="1. Введите параметры проёма и дверей-купе: ",
                                           bg='#1ad924',
                                           width=70)
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
                self.amount_doors.set(2)  # default value
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
                option = tools.MyOptionMenu(row, self.amount_doors, *list_num, command=main_frame.change_form)
                mes = tkinter.Message(row, text=self.fields[2], width=150)
                mes.pack(side='left')
                option.pack(side='right')
                self.row_frame.append(row)

                #  'Количество мест перекрытия:'
                row = tkinter.Frame(self, relief='ridge', bd=1)
                row.pack(side='top', fill='x')
                list_num = [1, 2, 3, 4, 5, 6, 7]
                option = tools.MyOptionMenu(row, self.amount_opening, *list_num)
                mes = tkinter.Message(row, text=self.fields[3], width=200)
                self.opening_quest = tools.AddQuest(row, HelpOpening)
                mes.pack(side='left')
                self.opening_quest.button.pack(side='left')
                option.pack(side='right')
                self.row_frame.append(row)

                #  'Буферная лента ("шлегель"):'
                row = tkinter.Frame(self)
                row.pack(side='top', fill='x')
                check1 = tkinter.Checkbutton(row, variable=self.need_tape, onvalue=1, offvalue=0)
                mes = tkinter.Message(row, text=self.fields[4], width=200)
                self.tape_quest = tools.AddQuest(row, HelpTape)
                mes.pack(side='left')
                self.tape_quest.button.pack(side='left')
                check1.pack(side="right", pady=2)

                self.row_frame.append(row)