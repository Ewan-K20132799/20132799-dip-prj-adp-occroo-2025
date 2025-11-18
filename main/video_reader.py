#imports utilized
from pathlib import Path
import cv2


VID_PATH = Path("./resources/oop.mp4")

class VideoReader:
    capture: cv2.VideoCapture

    def __init__(self,
                 video: Path | str):
        self.capture = cv2.VideoCapture(str(video))
        if not self.capture.isOpened():
            raise ValueError(f"Cannot open {video}")

    def video_playback(self):
        cap = self.capture

        while True:
            ret, frame = cap.read()

            if not ret:
                break

            cv2.imshow('CodingVideo', frame) # Displays video frame

            if cv2.waitKey(25) & 0xFF == ord('q'):  # Exits video using keybind
                break

        cap.release()
        cv2.destroyAllWindows() # removes video window from screen

    # def video_reader(self):


def test():
    video = VideoReader(video=VID_PATH)

    display = video.video_playback()

    return display

if __name__ == "__main__":
    print(cv2.getBuildInformation())
