import sqlalchemy as sqla

from app.web_.extensions import db


class EncounterCharacter(db.Model):
    # PriKey
    encounter_character_id = sqla.Column(sqla.Integer, primary_key=True)

    # ForKey
    fk_quest_id = sqla.Column(sqla.Integer, sqla.ForeignKey('quest.quest_id'), nullable=False)
    fk_encounter_id = sqla.Column(sqla.Integer, sqla.ForeignKey('encounter.encounter_id'), nullable=False)
    fk_character_id = sqla.Column(sqla.Integer, sqla.ForeignKey('character.character_id'), nullable=False)
