"""Project"""
# Student name: Ewan Keenan
# Student number: 20132799
# Project name: 20132799-dip-prj-adp-occroo-2025
# Project version: v1.0.1
# Date: 10/12/2025

import os
import re
from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import HTMLResponse, FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from starlette.requests import Request

import ocr

BASE_DIR = Path(__file__).resolve().parent
RESOURCES_DIR = BASE_DIR / "resources"
VIDEO_PATH = RESOURCES_DIR / "oop.mp4"
BYTES_PER_RESPONSE = 10_000_000

ocr_engine = None


# Pydantic models
class OCRRequest(BaseModel):
    seconds: int


class SaveOCRRequest(BaseModel):
    seconds: int
    filename: str


# Lifespan for startup/shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    global ocr_engine
    try:
        RESOURCES_DIR.mkdir(exist_ok=True)
        if VIDEO_PATH.exists():
            ocr_engine = ocr.OCR(video=VIDEO_PATH, out_dir=RESOURCES_DIR)
            print(f"OCR engine initialized with default video: {VIDEO_PATH}")
        else:
            ocr_engine = None
            print("No default video found. OCR engine not initialized.")
        yield
    finally:
        ocr_engine = None


# Initialize app with lifespan
app = FastAPI(lifespan=lifespan)

# Static and resource mounts
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/resources", StaticFiles(directory="resources"), name="resources")


# ----------------------
# Utility functions
# ----------------------
def chunk_gen(file_path: Path, start: int, size: int):
    with open(file_path, "rb") as f:
        f.seek(start)
        while size > 0:
            chunk_size = min(size, BYTES_PER_RESPONSE)
            yield f.read(chunk_size)
            size -= chunk_size


# ----------------------
# Routes
# ----------------------
@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    return FileResponse("static/favicon.ico")


@app.get("/")
def root():
    return FileResponse("static/index.html")


@app.get("/html")
def html():
    return HTMLResponse("<h1>Hello</h1>")


@app.get("/resources/{file_name}")
async def video_stream(file_name: str, request: Request):
    file_path = RESOURCES_DIR / file_name
    if not file_path.exists():
        raise HTTPException(404, "Video not found")

    file_size = os.path.getsize(file_path)
    range_header = request.headers.get("Range")

    if range_header:
        match = re.match(r"bytes=(\d+)-(\d*)", range_header)
        if not match:
            raise HTTPException(416, "Invalid range")

        start = int(match.group(1))
        end = int(match.group(2)) if match.group(2) else file_size - 1
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
                        break
                    remaining -= len(data)
                    yield data

        return StreamingResponse(stream(), status_code=206, headers=headers)

    return FileResponse(file_path, media_type="video/mp4")


# ----------------------
# API Endpoints
# ----------------------
@app.post("/api/generate-ocr")
async def gen_ocr(request: OCRRequest):
    global ocr_engine
    if ocr_engine is None:
        raise HTTPException(status_code=400, detail="OCR engine not initialized. Upload a video first.")

    try:
        text = ocr_engine.gen_ocr(sec_num=request.seconds)
        return {"ocr_text": text}
    except Exception as e:
        print("Error generating OCR:", e)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/save-ocr-as-txt")
async def save_ocr(request: SaveOCRRequest):
    global ocr_engine
    if ocr_engine is None:
        raise HTTPException(status_code=400, detail="OCR engine not initialized. Upload a video first.")

    try:
        result = ocr_engine.save_ocr_as_txt(sec_num=request.seconds, filename=request.filename)
        return {"success": True, "saved_path": str(result)}
    except Exception as e:
        print("Error saving OCR:", e)
        raise HTTPException(status_code=500, detail=f"Error saving OCR: {str(e)}")

# Global variable to track current video
current_video_path = RESOURCES_DIR / "oop.mp4"  # default

# Load video endpoint
@app.post("/api/load-video")
async def load_video(file: UploadFile = File(...)):
    global ocr_engine, current_video_path
    try:
        RESOURCES_DIR.mkdir(exist_ok=True)
        video_path = RESOURCES_DIR / file.filename

        # Save uploaded video
        with open(video_path, "wb") as f:
            f.write(await file.read())

        # Initialize OCR engine with new video
        ocr_engine = ocr.OCR(video=video_path, out_dir=RESOURCES_DIR)

        # Update the global current video path
        current_video_path = video_path

        return {"message": "Video loaded successfully!"}
    except Exception as e:
        print("Error loading video:", e)
        raise HTTPException(status_code=500, detail=str(e))


# Stream the latest uploaded video
@app.get("/resources/current-video")
async def stream_current_video(request: Request):
    if not current_video_path.exists():
        raise HTTPException(404, "No video loaded")

    file_path = current_video_path
    file_size = os.path.getsize(file_path)
    range_header = request.headers.get("Range")

    if range_header:
        match = re.match(r"bytes=(\d+)-(\d*)", range_header)
        if not match:
            raise HTTPException(416, "Invalid range")

        start = int(match.group(1))
        end = int(match.group(2)) if match.group(2) else file_size - 1
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
                        break
                    remaining -= len(data)
                    yield data

        return StreamingResponse(stream(), status_code=206, headers=headers)

    # Full video if no range header
    return FileResponse(file_path, media_type="video/mp4")
