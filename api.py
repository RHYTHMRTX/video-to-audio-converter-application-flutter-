from pathlib import Path
import shutil
import subprocess
import tempfile

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from starlette.background import BackgroundTask

app = FastAPI(title="Sonic Extract API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["*"],
)

ALLOWED_FORMATS = {"mp3": "libmp3lame", "wav": "pcm_s16le"}
ALLOWED_VIDEO_EXTENSIONS = {".mp4", ".mov", ".avi", ".mkv", ".webm", ".m4v"}


def remove_directory(directory: str) -> None:
    shutil.rmtree(directory, ignore_errors=True)


@app.post("/convert")
async def convert(file: UploadFile = File(...), format: str = Form("mp3")):
    output_format = format.lower().strip()
    original_filename = file.filename or "input video"
    extension = Path(original_filename).suffix.lower()
    if output_format not in ALLOWED_FORMATS:
        raise HTTPException(status_code=400, detail="Format must be mp3 or wav")
    if extension not in ALLOWED_VIDEO_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Unsupported video format")

    work_directory = tempfile.mkdtemp(prefix="sonic-extract-")
    input_path = Path(work_directory) / f"input{extension}"
    output_path = Path(work_directory) / f"audio.{output_format}"
    try:
        with input_path.open("wb") as destination:
            shutil.copyfileobj(file.file, destination)

        command = [
            "ffmpeg",
            "-y",
            "-i",
            str(input_path),
            "-vn",
            "-acodec",
            ALLOWED_FORMATS[output_format],
            str(output_path),
        ]
        result = subprocess.run(command, capture_output=True, text=True, check=False)
        if result.returncode != 0 or not output_path.exists():
            raise HTTPException(status_code=422, detail="The video could not be converted")

        return FileResponse(
            output_path,
            media_type="audio/mpeg" if output_format == "mp3" else "audio/wav",
            filename=f"{Path(original_filename).stem}.{output_format}",
            background=BackgroundTask(remove_directory, work_directory),
        )
    except HTTPException:
        remove_directory(work_directory)
        raise
    except Exception as error:
        remove_directory(work_directory)
        raise HTTPException(status_code=500, detail="Conversion service failed") from error
