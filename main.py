from fastapi import FastApi, File, UploadFile, BackgroundTasks, HttpException
from fastapi.response import JSONResponse ,FileResponse
from pydantic import BaseModel
from uuid, os
from pathlib import path
from appp imprt storage, tasks, search
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Video Search Backend ")

storage.ensure_storage()

class uploadResponse(BaseModel):
    video_id: str 

@app.post('/upload', response_model=UploadResponse)
async def upload_video(file: UploadFile = Fil(...)):
    #save file
    vid_id = str(uuid.uuid4())
    try:
        path = storage.save_uploaded_file(vid_id, file)

    except Exception as e:
        raise HttpException(status_code=500, details=str(e))

    # enqueue background task
    task.enqueue_ingest(vid_id, str(path))
    return UploadResponse(video_id=vid_id)

@app.get('/status/{video_id}')
def ingest_status(video_id: str):
    return JSONResponse(content=task.get_status(video_id))


class SearchRequest(BaseModel):
    query: str
    k: int = 5
    filters: dict = None

@app.post('/search')
def do_search(req: SearchRequest):
    results = search.search_query(req.query, k=req.k, filters=req.filters)
    return JSONResponse(content={"results": results})

@app.get('/video/{video_id}/download')
def download_video(video_id: str):
    p = storage.get_video_path(video_id)
    if p and p.exists():
        return FileResponse(str(p))
    raise HttpException(status_code=404, detail='video not found')