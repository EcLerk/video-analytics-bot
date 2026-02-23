from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class SnapshotSchema:
    id: UUID
    video_id: UUID
    views_count: int
    likes_count: int
    comments_count: int
    reports_count: int
    delta_views_count: int
    delta_likes_count: int
    delta_comments_count: int
    delta_reports_count: int
    created_at: datetime
    updated_at: datetime

    def __post_init__(self):
        self.id = UUID(self.id) if isinstance(self.id, str) else self.id
        self.video_id = UUID(self.video_id) if isinstance(self.video_id, str) else self.video_id
        self.created_at = datetime.fromisoformat(self.created_at) if isinstance(self.created_at,
                                                                                str) else self.created_at
        self.updated_at = datetime.fromisoformat(self.updated_at) if isinstance(self.updated_at,
                                                                                str) else self.updated_at