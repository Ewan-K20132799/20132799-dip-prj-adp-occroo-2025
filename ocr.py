# imports
from pathlib import Path
from PIL import Image
import pytesseract
from preliminary.library_basics import CodingVideo
import os

def init_lib_base():
    return (CodingVideo.get_frame_rgb_array,
            CodingVideo.save_as_image,
            CodingVideo.get_given_time,
            CodingVideo.get_frame_number_at_time)


class OCR:

    def __init__(self,
                 video: Path | str, out_dir: Path = None):
        video = Path(video)

        if out_dir is None:
            out_dir = video.parent

        self.video_path = video
        self.out_path = Path(out_dir)
        self.out_path.mkdir(parents=True, exist_ok=True)

        print("Loading video:", video.resolve())
        print("Exists:", video.exists())

        self.video = CodingVideo(video=str(video))

        if not self.video.capture.isOpened():
            raise ValueError(f"Cannot open video: {video}")

    def gen_image(self, sec_num:int):
        frame_num = CodingVideo.get_frame_number_at_time(self.video, seconds=sec_num)
        return CodingVideo.get_frame_rgb_array(self.video, frame_number=frame_num)

    def save_img(self, sec_num:int):
        CodingVideo.get_frame_number_at_time(self.video, seconds=sec_num)
        return CodingVideo.save_as_image(self.video, seconds=sec_num)

    def gen_ocr(self, sec_num:int):
        return CodingVideo.get_given_time(self.video, seconds=sec_num)


    def save_ocr_as_txt(self, sec_num: int, filename: str = None):
        frame_num = CodingVideo.get_frame_number_at_time(self.video, seconds=sec_num)

        frame = CodingVideo.get_frame_rgb_array(self.video, frame_number=frame_num)
        pil_image = Image.fromarray(frame)

        text_ext = pytesseract.image_to_string(pil_image)

        self.out_path.mkdir(parents=True, exist_ok=True)

        if filename:
            output_file = self.out_path / f"ocr_{frame_num}.txt"
        else:
            output_file = self.out_path / filename

        with open(output_file, "w", encoding="utf-8") as f:
            f.write("__Transcript__\n")
            f.write(f"Frame Number: {frame_num}\n")
            f.write(f"Timestamp (s): {sec_num}\n\n")
            f.write(text_ext)

        return output_file

def test():

    vid = OCR(video=Path(video))

    generate_img = vid.gen_image(sec_num=20)
    save_img = vid.save_img(sec_num=20)
    generate_ocr = vid.gen_ocr(sec_num=20)
    save_ocr_text = vid.save_ocr_as_txt(sec_num=20)

    print("--Results--")
    print(f"{generate_img}")
    print(f"{save_img}")
    print(f"{generate_ocr}")
    print(f"{save_ocr_text}")
if __name__ == "__main__":
    test()