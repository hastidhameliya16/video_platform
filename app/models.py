from datetime import datetime

from sqlalchemy import Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class Video(Base):
    __tablename__ = "videos"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(Text, default="uploaded")
    manifest_path: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())