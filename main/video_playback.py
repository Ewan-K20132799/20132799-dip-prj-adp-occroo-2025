#imports utilized
from pathlib import Path
import cv2

VID_PATH = Path("../resources/oop.mp4")

class VideoPlayer:
    capture: cv2.VideoCapture

    def __init__(self,
                 video: Path | str):
        self.video_path = Path(video)
        self.capture = cv2.VideoCapture(str(video))
        if not self.capture.isOpened():
            raise ValueError(f"Cannot open {video}")

    def video_playback(self):
        cap = self.capture

        while True:
            ret, frame = cap.read()

            if not ret:
                print(f"Unable to find frame in {self.video_path}, or video has ended.") # prints when there is no ret value for frame
                break
            cv2.imshow('CodingVideo', frame) # Displays video frame

            key = cv2.waitKey(30)

            if key == ord(' '): # Pauses and resumes video when pressed
                cv2.waitKey(-1)

            if key & 0xFF == ord('q'):  # Exits video using keybind
                break
        cap.release()
        cv2.destroyAllWindows() # removes video window from screen


class VideoReader:
   def __init__(self,
                vid_t = trans):
        self.vid_t = vid_t

   def video_reader(self):
      return self.vid_t

def test():
    video = VideoPlayer(video=VID_PATH)
    video.video_playback()


if __name__ == "__main__":
    test()


