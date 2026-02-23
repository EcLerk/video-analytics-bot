from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.schemas.snapshot import SnapshotSchema


@dataclass
class VideoSchema:
    id: UUID
    creator_id: UUID
    video_created_at: datetime
    views_count: int
    likes_count: int
    comments_count: int
    reports_count: int
    created_at: datetime
    updated_at: datetime

    def __post_init__(self):
        self.id = UUID(self.id) if isinstance(self.id, str) else self.id
        self.creator_id = UUID(self.creator_id) if isinstance(self.creator_id, str) else self.creator_id
        self.video_created_at = datetime.fromisoformat(self.video_created_at) if isinstance(self.video_created_at,
                                                                                str) else self.video_created_at
        self.created_at = datetime.fromisoformat(self.created_at) if isinstance(self.created_at,
                                                                                str) else self.created_at
        self.updated_at = datetime.fromisoformat(self.updated_at) if isinstance(self.updated_at,
                                                                                str) else self.updated_at
