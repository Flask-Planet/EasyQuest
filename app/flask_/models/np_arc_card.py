import sqlalchemy as sqla
from sqlalchemy.orm import relationship

from app.flask_.extensions import db


class NPArcCard(db.Model):

    # PriKey
    np_arc_card_id = sqla.Column(sqla.Integer, primary_key=True)

    # ForKey
    fk_quest_id = sqla.Column(sqla.Integer, sqla.ForeignKey('quest.quest_id'), nullable=False)

    # Arc
    arc = sqla.Column(sqla.String(255), nullable=False)
    description = sqla.Column(sqla.String, nullable=True)
    modifier = sqla.Column(sqla.String, nullable=True)
    bonus = sqla.Column(sqla.String, nullable=True)

    # Weapon
    starting_weapon_name = sqla.Column(sqla.String(255), nullable=True)
    starting_weapon_damage = sqla.Column(sqla.Integer, nullable=True, default=0)

    # Combat
    health = sqla.Column(sqla.Integer, nullable=False, default=100)
    defence = sqla.Column(sqla.Integer, nullable=False, default=1)
    hostile = sqla.Column(sqla.Boolean, nullable=False, default=False)
    unique = sqla.Column(sqla.Boolean, nullable=False, default=False)

    # Attributes
    strength = sqla.Column(sqla.Integer, nullable=False, default=0)
    agility = sqla.Column(sqla.Integer, nullable=False, default=0)
    intelligence = sqla.Column(sqla.Integer, nullable=False, default=0)
    luck = sqla.Column(sqla.Integer, nullable=False, default=0)
    perception = sqla.Column(sqla.Integer, nullable=False, default=0)
    persuasion = sqla.Column(sqla.Integer, nullable=False, default=0)

    # Tracking
    order = sqla.Column(sqla.Integer, nullable=False, default=0)
    created = sqla.Column(sqla.DateTime)

    # Relationships
    rel_quest = relationship(
        "Quest",
        primaryjoin="Quest.quest_id==NPArcCard.fk_quest_id",
        back_populates="rel_np_arc_cards"
    )
