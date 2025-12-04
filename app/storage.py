from pathlib import Path 
import shutil, os
from fastapi import UploadFile

STORAGE_DIR = Path((os.getenv('STORAGE_DIR') or './storage')).resolve()
VIDEOS_DIR = STORAGE_DIR / 'videos'
OUTPUT_DIR = STORAGE_DIR / 'output'

def ensure_storage():
    STORAGE_DIR.mkdir(parents=True, exist_ok=True)
    VIDEOS_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def save_uploaded_file(video_id: str, file: UploadFile) -> Path:
    ensure_storage()
    out = VIDEOS_DIR / f"{video_id}.mp4"
    with out.open('wb') as f:
        shutil.copyfileobj(file.file, f)
    return out

def get_video_path(video_id: str) -> Path: