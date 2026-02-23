import json
from dataclasses import dataclass, asdict

from app.db.models import VideoModel, SnapshotModel
from app.db.session import Session
from app.schemas.snapshot import SnapshotSchema
from app.schemas.video import VideoSchema


async def load_data() -> None:
    with open("scripts/videos.json", "r", encoding="utf-8") as f:
        raw_data = json.load(f)["videos"]

    videos: list[VideoModel] = []
    snapshots: list[SnapshotModel] = []

    for item in raw_data:
        video = VideoSchema(**{k: v for k, v in item.items() if k != "snapshots"})
        videos.append(VideoModel(**asdict(video)))

        snapshots.extend(
            SnapshotModel(**asdict(SnapshotSchema(**snap)))
            for snap in item.get("snapshots", [])
        )

    async with Session() as session:
        async with session.begin():
            for video in videos:
                await session.merge(video)
            for snapshot in snapshots:
                await session.merge(snapshot)
