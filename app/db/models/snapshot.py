import uuid

from sqlalchemy import UUID, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import Base


class Snapshot(Base):
    __tablename__ = "snapshots"

    video_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("videos.id", ondelete="CASCADE"),
        nullable=False,
    )
    views_count: Mapped[int] = mapped_column(Integer, nullable=False,)
    likes_count: Mapped[int] = mapped_column(Integer, nullable=False,)
    comments_count: Mapped[int] = mapped_column(Integer, nullable=False,)
    reports_count: Mapped[int] = mapped_column(Integer, nullable=False,)
    delta_views_count: Mapped[int] = mapped_column(Integer, nullable=False,)
    delta_likes_count: Mapped[int] = mapped_column(Integer, nullable=False,)
    delta_comments_count: Mapped[int] = mapped_column(Integer, nullable=False,)
    delta_reports_count: Mapped[int] = mapped_column(Integer, nullable=False,)

    video: Mapped["Video"] = relationship(
        back_populates="snapshots",
    )
