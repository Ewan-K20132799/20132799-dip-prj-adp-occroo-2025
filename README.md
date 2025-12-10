# Overview

This project was designed for people who experience difficulties relating to their vision who want to maybe copy some
code or take notes easier from a video and was made as a means to allow those who are hard of sight to fulfill those needs.

The core dependencies of this project include:
- uvloop
- opencv (cv2)
- numpy
- pillow (PIL)
- pytesseract
- fastapi
- starlette
- jinja
- httpcore
- node js (npm (for bluebird))

These utilities are used to help create functions such as video playback, OCR generation, OCR saving and loading videos.

# deploying and activating the project
1. git clone this repository to your repos file (you can copy the link or sha prefix after typing git clone into the terminal)
2. open the project in your chosen IDE (PyCharm preferred)
3. before creating the .venv file, enter the project file in your repos by typing cd ~/Source/Repos/"current_name_of_repo"
4. in the terminal create a .venv and install all dependencies mentioned above using a bash/zsh terminal
5. activate the .venv file by typing source .venv/lib or bin (depends on if you are using windows or MacOS/Linux)/activate
6. activate FastAPI with your bash/zsh terminal command fastapi dev main.py

# project functions
keybinds:
- space = play/pause (will have to use this for initial video activation)
- m = mute/unmute

gui interaction:
- all gui interactive items are centered in the screen
- video gui:
  - the video gui includes (from left to right):
    - a rewind button 
    - pause/play button
    - fast forward button
    - interactive video playback line
    - mute/unmute button
    - volume control
  - There are three buttons below the vido gui including (from left to right):
    - The generate OCR button (generates OCR (will do this in the background))
      - the save OCR button (This currently saves it to resources and is named based on the frame that
      the use has paused on in the video)
      - The load video function (This takes the user to their files directory to select a video that will be added to 
       the resources directory)

Tesseract binaries are required (if the user is on Linux and doesn't have tesseract binaries preinstalled, then the link is https://github.com/tesseract-ocr/tesseract
copy the link above and run makepkg -Si).

Reference for button CSS: https://uiverse.io/cssbuttons-io/weak-firefox-5 