from datetime import datetime

from sqlalchemy import DateTime, String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import Base


class Video(Base):
    __tablename__ = 'videos'

    creator_id: Mapped[str] = mapped_column(String, nullable=False,)
    video_created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False,)
    views_count: Mapped[int] = mapped_column(Integer, nullable=False,)
    likes_count: Mapped[int] = mapped_column(Integer, nullable=False,)
    comments_count: Mapped[int] = mapped_column(Integer, nullable=False,)
    reports_count: Mapped[int] = mapped_column(Integer, nullable=False,)

    snapshots: Mapped[list["VideoSnapshot"]] = relationship(
        back_populates="video",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
