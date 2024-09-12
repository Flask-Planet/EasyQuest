import sqlalchemy as sqla

from app.web_.extensions import db


class EncounterNPCharacter(db.Model):
    # PriKey
    encounter_np_character_id = sqla.Column(sqla.Integer, primary_key=True)

    # ForKey
    fk_quest_id = sqla.Column(sqla.Integer, sqla.ForeignKey('quest.quest_id'), nullable=False)
    fk_encounter_id = sqla.Column(sqla.Integer, sqla.ForeignKey('encounter.encounter_id'), nullable=False)
    fk_np_character_id = sqla.Column(sqla.Integer, sqla.ForeignKey('np_character.np_character_id'), nullable=False)

    # Tracking
    finished = sqla.Column(sqla.Boolean, nullable=False, default=False)
