# create a virtual environmenent
# activate the environment 

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

app = FastAPI()
from app import repositories
from app.db import get_db


@app.get("/health")
def get_health():
    return {"status" : "ok"}
@app.post("/videos", status_code=201)
def create_video(title: str, db: Session = Depends(get_db)):
    video = repositories.create_video(db, title=title, manifest_path="hls/master.m3u8")
    return {"id": video.id, "title": video.title}


@app.get("/videos/{video_id}")
def get_video(video_id: int, db: Session = Depends(get_db)):
    video = repositories.get_video(db, video_id)
    if video is None:
        raise HTTPException(status_code=404, detail="video not found")
    return {"id": video.id, "title": video.title, "status": video.status}


@app.get("/v1.0/manifest")
def get_manifest(ItemID: int, db: Session = Depends(get_db)):
    video = repositories.get_video(db, ItemID)
    if video is None or video.manifest_path is None:
        raise HTTPException(status_code=404, detail="manifest not found")
    return FileResponse(video.manifest_path, media_type="application/vnd.apple.mpegurl")


@app.get("/v1.0/showfeed")
def show_feed(UserID: int, limit: int = 20, offset: int = 0, db: Session = Depends(get_db)):
    videos = repositories.list_videos(db, limit=limit, offset=offset)
    return {"user_id": UserID, "videos": [{"id": v.id, "title": v.title} for v in videos]}