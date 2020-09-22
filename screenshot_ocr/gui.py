import tkinter as tk
from tkinter import StringVar, OptionMenu, Button, Text
from .ocr import ScreenshotOCT
from threading import Thread

import mss


class Application(tk.Frame):
    text: Text
    language_options: OptionMenu
    language_selection: StringVar
    button: Button
    options: OptionMenu
    selection: StringVar

    def __init__(self, master=None):
        super().__init__(master)
        self.has_start = False
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        scc = mss.mss()
        choices = [f"Display {i}" for i, m in enumerate(scc.monitors)]
        languages = ['eng']

        frame1 = tk.Frame(self)
        frame1.pack(fill=tk.X)

        tk.Label(frame1, text="Display Selection").pack(side=tk.LEFT, padx=10)
        self.selection = tk.StringVar(self)
        self.selection.set(choices[0])
        self.options = tk.OptionMenu(frame1, self.selection, *choices)
        self.options.pack(fill=tk.X, expand=True)

        frame2 = tk.Frame(self)
        frame2.pack(fill=tk.X)

        tk.Label(frame2, text="Language Selection").pack(side=tk.LEFT, padx=10)
        self.language_selection = tk.StringVar(self)
        self.language_selection.set(languages[0])
        self.language_options = tk.OptionMenu(frame2, self.language_selection, *languages)
        self.language_options.pack(fill=tk.X)

        frame3 = tk.Frame(self)
        frame3.pack(fill=tk.X)

        tk.Label(frame3, text="Output").pack(side=tk.LEFT, padx=10)
        self.text = tk.Text(frame3)
        self.text.pack(fill=tk.BOTH, padx=10)

        self.button = tk.Button()
        self.button["text"] = "Screenshot"
        self.button["command"] = self.screenshot
        self.button.pack(side="bottom", fill=tk.X, pady=10)

    def screenshot(self):
        display_str = self.selection.get().replace("Display ", "")
        language = self.language_selection.get()
        if not self.has_start:
            t = Thread(target=self.__convert, args=(display_str, language))
            t.start()
            self.has_start = True

    def __convert(self, display, language):
        self.__set_text("Start working")
        ocr = ScreenshotOCT(screen=int(display), lang=language)
        try:
            result = ocr.take_screenshot()
            self.__set_text(result)
        except Exception as e:
            self.__set_text(str(e))
        self.has_start = False

    def __set_text(self, text):
        self.text.delete(1.0, tk.END)
        self.text.insert(tk.END, text)
