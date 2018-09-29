import tkinter


class FormAndMaterial(tkinter.Frame):
    def __init__(self, main_frame, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.main_frame = main_frame