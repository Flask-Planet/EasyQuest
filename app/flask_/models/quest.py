from app.flask_.extensions import db
import sqlalchemy as sqla
from sqlalchemy.orm import relationship
from .__mixins__ import CrudMixin


class Quest(db.Model, CrudMixin):
    id_field = "quest_id"

    # PriKey
    quest_id = sqla.Column(sqla.Integer, primary_key=True)

    # ForKey
    fk_genre_id = sqla.Column(sqla.Integer, sqla.ForeignKey('genre.genre_id'), nullable=False)

    # Data
    title = sqla.Column(sqla.String(256), nullable=False)
    summary = sqla.Column(sqla.String(4000), default='', nullable=True)
    live = sqla.Column(sqla.Boolean, default=False)
    finished = sqla.Column(sqla.Boolean, default=False)
    arc_cards = sqla.Column(sqla.JSON, default={}, nullable=True)

    # Tracking
    created = sqla.Column(sqla.DateTime)

    # Relationships
    rel_genre = relationship(
        "Genre",
        primaryjoin="Genre.genre_id==Quest.fk_genre_id",
        back_populates="rel_quests"
    )

    rel_characters = relationship(
        "Character",
        primaryjoin="Character.fk_quest_id==Quest.quest_id",
        back_populates="rel_quest"
    )
