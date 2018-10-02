import tkinter
import os
from PIL import Image, ImageTk
import tkinter.messagebox as mbox

import settings


class Calculation(tkinter.Toplevel):
    def __init__(self, main_frame, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def make_widget(self):
        pass

