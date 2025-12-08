# Imports
from starlette.responses import StreamingResponse

import video_playback as play
import ocr as trans
from preliminary import simple_api

from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from fastapi import FastAPI, HTTPException
import os
from starlette.requests import Request

import re


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

app.mount("/static", StaticFiles(directory="static"), name="static")

BYTES_PER_RESPONSE = 10000000

def chunk_gen(file_path, start, size):
    with open(file_path, 'rb') as f:
        f.seek(start)
        while size > 0:
            chunk_size = min(size, BYTES_PER_RESPONSE)
            yield f.read(chunk_size)
            size -= chunk_size

@app.get("/favicon.ico", include_in_schema=False)
def favicon():
       return FileResponse("static/favicon.ico")

@app.get('/')
def root():
       return FileResponse("static/index.html")

@app.get('/html')
def html():
       return HTMLResponse("<h1>Hello</h1>")


@app.get('/static/index.html')
def main_app():
    try:
        return FileResponse("static/index.html")
    except Exception:
        raise HTTPException(status_code=404, detail="Unable to load page or page items.")

@app.get('/resources/{file_name}')
async def oop_vid_stream(file_name: str, request: Request):
    file_path = f"./resources/{file_name}"

    if not os.path.isfile(file_path):
        raise HTTPException(404, "Video not found")

    file_size = os.path.getsize(file_path)
    range_header = request.headers.get("Range")

    if range_header:
        match = re.match(r"bytes=(\d+)-(\d*)", range_header)
        if not match:
            raise HTTPException(416, "Invalid range")

        start = int(match.group(1))
        end = match.group(2)
        end = int(end) if end else file_size - 1

        if start >= file_size:
            raise HTTPException(416, "Range not satisfiable")

        chunk_size = end - start + 1

        headers = {
                "Content-Range": f"bytes {start}-{end}/{file_size}",
                "Accept-Ranges": "bytes",
                "Content-Length": str(chunk_size),
                "Content-Type": "video/mp4"
            }

        async def stream():
            with open(file_path, "rb") as f:
                f.seek(start)
                remaining = chunk_size
                while remaining > 0:
                    data = f.read(min(remaining, 1024 * 1024))
                    if not data:
                        raise ValueError('Unable to read data.')
                    remaining -= len(data)
                    yield data

        return StreamingResponse(stream(), status_code=206, headers=headers)

    return FileResponse(file_path, media_type="video/mp4")

@app.post('/static/index.html')
def main_app_post():
    try:
        return FileResponse("static/index.html")
    except Exception:
        raise HTTPException(status_code=404, detail="Unable to load page or page items.")


@app.post('/', response_class=HTMLResponse)
def root_post():
    try:
        return FileResponse("static/index.html")
    except Exception:
        raise HTTPException(status_code=404, detail="Unable to access site.")

