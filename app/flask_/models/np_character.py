import sqlalchemy as sqla
from sqlalchemy.orm import relationship

from app.flask_.extensions import db
from .__mixins__ import CrudMixin


class NPCharacter(db.Model, CrudMixin):
    # PriKey
    np_character_id = sqla.Column(sqla.Integer, primary_key=True)

    # ForKey
    fk_quest_id = sqla.Column(sqla.Integer, sqla.ForeignKey('quest.quest_id'), nullable=True)
    fk_np_arc_card_id = sqla.Column(sqla.Integer, sqla.ForeignKey('np_arc_card.np_arc_card_id'), nullable=True)

    # Personal
    full_name = sqla.Column(sqla.String(256), nullable=False)
    back_story = sqla.Column(sqla.String(4000), nullable=False)
    display_picture = sqla.Column(sqla.String(256), nullable=True)

    # Arc
    arc = sqla.Column(sqla.String(256), nullable=True)
    description = sqla.Column(sqla.String(1024), nullable=True)
    modifier = sqla.Column(sqla.String(256), nullable=True)
    bonus = sqla.Column(sqla.String(256), nullable=True)

    # Weapon
    weapon_name = sqla.Column(sqla.String(255), nullable=True)
    weapon_damage = sqla.Column(sqla.Integer, nullable=True, default=0)

    # Combat
    health = sqla.Column(sqla.Integer, nullable=False, default=100)
    current_health = sqla.Column(sqla.Integer, nullable=False, default=100)
    defence = sqla.Column(sqla.Integer, nullable=False, default=1)

    # Combat Markers
    hostile = sqla.Column(sqla.Boolean, nullable=False, default=False)
    unique = sqla.Column(sqla.Boolean, nullable=False, default=False)
    dead = sqla.Column(sqla.Boolean, nullable=False, default=False)

    # Attributes
    strength = sqla.Column(sqla.Integer, nullable=False, default=0)
    agility = sqla.Column(sqla.Integer, nullable=False, default=0)
    intelligence = sqla.Column(sqla.Integer, nullable=False, default=0)
    luck = sqla.Column(sqla.Integer, nullable=False, default=0)
    perception = sqla.Column(sqla.Integer, nullable=False, default=0)
    persuasion = sqla.Column(sqla.Integer, nullable=False, default=0)

    # Status Effects
    sleeping = sqla.Column(sqla.Boolean, nullable=False, default=False)
    confused = sqla.Column(sqla.Boolean, nullable=False, default=False)
    poisoned = sqla.Column(sqla.Boolean, nullable=False, default=False)
    buffed = sqla.Column(sqla.Boolean, nullable=False, default=False)

    # Gold
    gold = sqla.Column(sqla.Integer, nullable=False, default=0)

    # Inventory
    inventory = sqla.Column(sqla.JSON, nullable=True)

    # Tracking
    created = sqla.Column(sqla.DateTime)

    # Relationships
    rel_quest = relationship(
        "Quest",
        back_populates="rel_np_characters"
    )
