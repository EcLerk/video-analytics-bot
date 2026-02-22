from sqlalchemy.orm import DeclarativeBase

from app.db.models.mixins import UuidMixin, TimeStampMixin


class Base(DeclarativeBase, UuidMixin, TimeStampMixin):
    __abstract__ = True
    pass

