from datetime import datetime, timezone

from sqlalchemy import DateTime, UUID
from sqlalchemy.orm import Mapped, mapped_column


class TimeStampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(tz=timezone.utc),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(tz=timezone.utc),
        onupdate=lambda: datetime.now(tz=timezone.utc),
    )


class UuidMixin:
    id: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
        primary_key=True,
    )
