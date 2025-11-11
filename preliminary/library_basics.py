# imports - add all required imports here
from pathlib import Path
from PIL import Image
import cv2
import numpy as np
import pytesseract

VID_PATH = Path("/home/ellie_marigold/Source/Repos/20132799-dip-prj-adp-occroo-2025/resources/oop.mp4")
OUT_PATH = Path("/home/ellie_marigold/Source/Repos/20132799-dip-prj-adp-occroo-2025/resources/")

class CodingVideo:
    capture: cv2.VideoCapture


    def __init__(self,
                 video: Path | str):
        self.capture = cv2.VideoCapture(video) # You complete me!
        if not self.capture.isOpened():
            raise ValueError(f"Cannot open {video}")

        self.fps = self.capture.get(cv2.CAP_PROP_FPS) #frames per second
        self.frame_count = self.capture.get(cv2.CAP_PROP_FRAME_COUNT)  #total frames
        self.duration = self.frame_count/self.fps #duration of clip


    def __str__(self) -> str:
        """Displays key metadata from the video

        Specifically, the following information is shown:
            FPS - Number of frames per second rounded to two decimal points
            FRAME COUNT - The total number of frames in the video
            DURATION (minutes) - Calculated total duration of the video given FPS and FRAME COUNT

        Reference
        ----------
        https://docs.opencv.org/3.4/d4/d15/group__videoio__flags__base.html#gaeb8dd9c89c10a5c63c139bf7c4f5704d
        """

        info_string = ('Current video has following properties:' +
                       f'{self.fps}' + 'fps' +
                       f'{self.frame_count}' + 'frame count' +
                       f'{self.duration}' + 'duration')
        return info_string

    def get_frame_number_at_time(self, seconds: int) -> int:

        """Given a time in seconds, returns the value of the nearest frame"""
        return int(self.fps * seconds)


    def get_frame_rgb_array(self, frame_number: int,
                            output_path: Path | str = 'output.png') -> np.ndarray:
        """Returns a numpy N-dimensional array (ndarray)

        The array represents the RGB values of each pixel in a given frame

        Note: cv2 defaults to BGR format, so this function converts the color space to RGB

        Reference
        ---------
        # TODO: Find a tutorial on OpenCV that demonstrates color space conversion

        """
        self.capture.set(cv2.CAP_PROP_POS_FRAMES, frame_number - 1)
        ok, frame =  self.capture.read()
        if not ok or frame is None:
            raise ValueError("Invalid frame in target")

        rgb_frame_array = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(rgb_frame_array)
        image.save(output_path)
        return rgb_frame_array


    def get_image_as_bytes(self, seconds: int) -> bytes:
        self.capture.set(cv2.CAP_PROP_POS_FRAMES, self.get_frame_number_at_time(seconds))
        ok, frame = self.capture.read()
        if seconds < 0 or seconds > self.duration:
            raise ValueError(f"Invalid time:{seconds}s. Video duration is only {self.duration:.2f}s.")
        if not ok or frame is None:
            raise ValueError("Invalid frame in target location")
        ok, buf = cv2.imencode(".png", frame)
        if not ok:
          raise ValueError("Failed to encode frame")
        return buf.tobytes()

    def save_as_image(self, seconds: int,
                      output_path: Path | str = 'output.png',
                      ) -> np.ndarray:
      """Saves the given frame as a png image

      # TODO: Requires a third-party library to convert ndarray to png
      # Lib is Pillow (PIL)
      # TODO: Identify the library and add a reference to its documentation
      # Ref: https://pillow.readthedocs.io/en/stable/?badge=latest


      """
      output_path = OUT_PATH / output_path
      frame_number = self.get_frame_number_at_time(seconds)
      frame_array = self.get_frame_rgb_array(frame_number)

      if isinstance(output_path, Path):

            frame = self.get_frame_number_at_time(seconds)
            self.capture.set(cv2.CAP_PROP_POS_FRAMES, frame-1)
            image = Image.fromarray(frame_array)
            image.save(output_path)
            ok, frame = self.capture.read()
            if not ok:
                raise ValueError("Unable to read frame from file.")
            else:
                return frame_array
      else:
            raise ValueError("Unable to read file.")

    def get_given_time(self, seconds: int) -> str:
        frame_number = self.get_frame_number_at_time(seconds)
        self.capture.set(cv2.CAP_PROP_POS_FRAMES, frame_number - 1)
        ok, frame = self.capture.read()
        if not ok or frame is None:
            raise ValueError("Invalid frame in target")

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(rgb_frame)
        img_to_str = pytesseract.image_to_string(rgb_frame)

        if type(image) is str:
            ok, frame = self.capture.read()
            if not ok or frame is None:
                raise ValueError("Invalid frame in target location") or ValueError("No frame in target location.")
            else:
                if not ok:
                    raise ValueError("Failed to encode frame")
        return img_to_str

def test():
    """Try out your class here"""
    Video = CodingVideo(video=VID_PATH)

    string = Video.__str__()
    frame_n = Video.get_frame_number_at_time(10)
    array = Video.get_frame_rgb_array(10)
    i_bytes = Video.get_image_as_bytes(10)
    save = Video.save_as_image(10)
    given = Video.get_given_time(10)

    print("--Results__")
    print(f"{string}")
    print(f"\nFrame at # Seconds: {frame_n}")
    print(f"Frame array shape: {array.shape}")
    print(f"Image bytes length: {len(i_bytes)}")
    print(f"Saved image array shape: {save.shape}")
    print(f"\n--Text at #s--")
    print(f"{given}")

    return string, frame_n, array, i_bytes, save, given

if __name__ == '__main__':
    test()
