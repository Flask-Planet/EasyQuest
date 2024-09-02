import sqlalchemy as sqla
from sqlalchemy.orm import relationship

from app.flask_.extensions import db


class Encounter(db.Model):
    # PriKey
    encounter_id = sqla.Column(sqla.Integer, primary_key=True)

    # ForKey
    fk_quest_id = sqla.Column(sqla.Integer, sqla.ForeignKey('quest.quest_id'), nullable=False)

    possible = sqla.Column(sqla.Boolean, nullable=False, default=True)
    finished = sqla.Column(sqla.Boolean, nullable=False, default=False)

    # Tracking
    created = sqla.Column(sqla.DateTime)

    # Relationships
    rel_quest = relationship(
        "Quest",
        primaryjoin="Quest.quest_id==Encounter.fk_quest_id",
        back_populates="rel_encounters"
    )

    rel_characters = relationship(
        "EncounterCharacter",
        primaryjoin="EncounterCharacter.fk_encounter_id==Encounter.encounter_id",
        viewonly=True
    )

    rel_np_characters = relationship(
        "EncounterNPCharacter",
        primaryjoin="EncounterNPCharacter.fk_encounter_id==Encounter.encounter_id",
        viewonly=True
    )
