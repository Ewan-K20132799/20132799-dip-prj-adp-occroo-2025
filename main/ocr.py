# imports
from fileinput import close
from pathlib import Path
import cv2
from PIL import Image
import pytesseract
from preliminary.library_basics import CodingVideo

VID_PATH = Path("../resources/oop.mp4")
OUT_PATH = Path("./resources/")


def init_lib_base():
    return CodingVideo.get_frame_rgb_array, CodingVideo.save_as_image, CodingVideo.get_given_time


class OCR:
    capture: cv2.VideoCapture

    def __init__(self,
                 video: Path | str):
        self.capture = cv2.VideoCapture(str(video))
        if not self.capture.isOpened():
            raise ValueError(f"Cannot open {video}")

    def gen_image(self):
        return CodingVideo.get_frame_rgb_array(self.capture)

    def gen_ocr(self):
        return CodingVideo.get_given_time(self.capture)

    def save_ocr_as_txt(self):

        while CodingVideo.save_as_image(self.capture) & CodingVideo.get_given_time(self.capture):
            txt_image = Image.open(OUT_PATH / " .png")

            text_ext = pytesseract.image_to_string(txt_image)

            with open('output.txt', 'w') as text_file:
                text_file.write("__Transcript__")
                text_file.write(text_ext)
            text_file.close()
        return

    def save_ocr_as_img(self):
        pass

    def load_ocr_txt(self):
        pass

def test():
    generate_img = OCR.gen_image()
    generate_ocr = OCR.gen_ocr()
    save_ocr_text = OCR.save_ocr_as_txt()

    print("--Results__")

if __name__ == "__main__":
    test()