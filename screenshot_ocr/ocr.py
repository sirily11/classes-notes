import mss
from PIL import Image
import pytesseract
import mss.tools

class ScreenshotOCT:
    def __init__(self, screen=1, lang='eng'):
        """
        :param screen: which display you want to use
        :param lang: language of the image
        """
        self.screen = screen
        self.lang = lang

    def take_screenshot(self) -> str:
        """
        Take a screenshot and return a string which represents the image
        :return:
        """
        with mss.mss() as sct:
            # Grab the data
            mon = sct.monitors[self.screen]
            sct_img = sct.grab(mon)
            img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
            return self.__ocr__(img)

    def __ocr__(self, image):
        return pytesseract.image_to_string(image, lang=self.lang)
