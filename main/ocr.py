# imports
from pathlib import Path
from PIL import Image
import pytesseract
from preliminary.library_basics import CodingVideo

VID_PATH = Path("../resources/oop.mp4")
OUT_PATH = Path("../resources/")


def init_lib_base():
    return (CodingVideo.get_frame_rgb_array,
            CodingVideo.save_as_image,
            CodingVideo.get_given_time,
            CodingVideo.get_frame_number_at_time)


class OCR:

    def __init__(self,
                 video: Path | str):
        self.video = CodingVideo(video=str(video))
        if not self.video.capture.isOpened():
            raise ValueError(f"Cannot open {video}")

    def gen_image(self, frame_num:int):
        return CodingVideo.get_frame_rgb_array(self.video, frame_number=frame_num)

    def save_img(self, sec_num:int):
        CodingVideo.get_frame_number_at_time(self.video, seconds=sec_num)
        return CodingVideo.save_as_image(self.video, seconds=sec_num)

    def gen_ocr(self, sec_num:int):
        return CodingVideo.get_given_time(self.video, seconds=sec_num)

    def save_ocr_as_txt(self, sec_num):
        frame = CodingVideo.save_as_image(self.video, seconds=sec_num)
        arr_image = Image.fromarray(frame)
        text_ext = pytesseract.image_to_string(arr_image)

        output_file = OUT_PATH / 'output.txt'
        with open(output_file, 'w') as text_file:
            text_file.write("__Transcript__\n")
            text_file.write(text_ext)
        return f"Successful {output_file}"

    def load_ocr_txt(self):
        pass

def test():
    Video = OCR(video=VID_PATH)

    generate_img = Video.gen_image(frame_num=20)
    save_img = Video.save_img(sec_num=20)
    generate_ocr = Video.gen_ocr(sec_num=20)
    save_ocr_text = Video.save_ocr_as_txt(sec_num=20)

    print("--Results--")
    print(f"{generate_img}")
    print(f"{save_img}")
    print(f"{generate_ocr}")
    print(f"{save_ocr_text}")
if __name__ == "__main__":
    test()