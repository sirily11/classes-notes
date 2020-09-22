import mss
import tkinter as tk
from PIL import Image
import pytesseract
import mss.tools
from screenshot_ocr.gui import Application




if __name__ == '__main__':
    root = tk.Tk()
    root.minsize(300, 400)
    app = Application(master=root)
    app.mainloop()
