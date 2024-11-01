from sqlalchemy.orm import Mapped, mapped_column
from ..db import db
from datetime import datetime
from sqlalchemy import DateTime
from typing import Optional

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    completed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime, nullable=True, default=None
    )
    @property
    def is_complete(self):
        return self.completed_at is not None

    def mark_complete(self):
        self.completed_at = datetime.now()

    def mark_incomplete(self):
        self.completed_at = None

    def to_dict(self):

        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_complete": self.is_complete,
        }
