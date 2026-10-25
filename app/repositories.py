from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Video


def get_video(db: Session, video_id: int) -> Video | None:
    return db.get(Video, video_id)


def list_videos(db: Session, limit: int = 20, offset: int = 0) -> list[Video]:
    stmt = select(Video).order_by(Video.id).limit(limit).offset(offset)
    return list(db.scalars(stmt))


def create_video(db: Session, title: str, manifest_path: str | None = None) -> Video:
    video = Video(title=title, manifest_path=manifest_path)
    db.add(video)
    db.commit()
    db.refresh(video)
    return video