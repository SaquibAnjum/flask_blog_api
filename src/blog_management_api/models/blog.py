from datetime import datetime, timezone
from ..extensions import db

class Blog(db.Model):
    __tablename__="blogs"

    id=db.Column(
        db.Integer,
        primary_key=True
    )
    title=db.Column(
        db.String(200),
        nullable=False
    )
    content=db.Column(
        db.Text,
        nullable=False
    )
    author_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )
    status=db.Column(
        db.String(20),
        nullable=False,
        default="draft"
    )
    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    updated_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    published_at = db.Column(
        db.DateTime(timezone=True),
        nullable=True
    )