# Imports
import video_playback as play
import ocr as trans
from preliminary import simple_api
from fastapi.responses import HTMLResponse
from fastapi import FastAPI, HTTPException, Response

class VideoReader:
   def __init__(self,
                vid_t = trans,
                vid_p = play):
        self.vid_t = vid_t
        self.vid_p = vid_p

   def video_reader(self):
      return self.vid_t

   def video_playback(self):
      return self.vid_p

class API:
    def __init__(self, api=simple_api):
        self.api = api

    def api_util(self):
        return self.api

app = FastAPI()

@app.get('/')
def app_slash():
    return HTTPException(status_code=404,
                          detail="Unable to access site.")
@app.get('/index.html', response_class=HTMLResponse)
def main_app():
    return (VideoReader(),
            API())
@app.post('/index.html', response_class=HTMLResponse)
def main_app_post():
    return (VideoReader(),
            API(),
            HTTPException(status_code=404,
                  detail="Unable to load page or page items."))
@app.post('/', response_class=HTMLResponse)
def main_app_post():
    HTTPException(status_code=404,
                  detail="Unable to load page or page items.")

