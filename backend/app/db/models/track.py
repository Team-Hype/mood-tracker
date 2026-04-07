from app.db.models.mixins.index import UUIDMixin

from .. import DeclarativeBase as Base


class MoodTrack(UUIDMixin, Base):
    __tablename__ = "mood_track"
    pass
