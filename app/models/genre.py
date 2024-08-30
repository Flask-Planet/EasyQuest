import sqlalchemy as sqla
from sqlalchemy.orm import relationship

from app.extensions import db
from .__mixins__ import CrudMixin


class Genre(db.Model, CrudMixin):
    id_field = "genre_id"

    # PriKey
    genre_id = sqla.Column(sqla.Integer, primary_key=True)

    # Data
    genre = sqla.Column(sqla.String(256), nullable=False)
    description = sqla.Column(sqla.String(512), nullable=True)

    # Tracking
    created = sqla.Column(sqla.DateTime)

    # Relationships
    rel_quests = relationship(
        "Quest",
        primaryjoin="Quest.fk_genre_id==Genre.genre_id",
        back_populates="rel_genre"
    )
