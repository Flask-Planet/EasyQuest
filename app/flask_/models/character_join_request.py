import sqlalchemy as sqla

from app.flask_.extensions import db


class CharacterJoinRequest(db.Model):
    # PriKey
    character_join_request_id = sqla.Column(sqla.Integer, primary_key=True)

    # ForKey
    fk_user_id = sqla.Column(sqla.Integer, sqla.ForeignKey('user.user_id'), nullable=False)
    fk_character_id = sqla.Column(sqla.Integer, sqla.ForeignKey('character.character_id'), nullable=False)
    fk_quest_id = sqla.Column(sqla.Integer, sqla.ForeignKey('quest.quest_id'), nullable=False)

    # Data
    accepted = sqla.Column(sqla.Boolean, default=False)
    rejected = sqla.Column(sqla.Boolean, default=False)

    rel_quest = db.relationship(
        "Quest",
        primaryjoin="Quest.quest_id==CharacterJoinRequest.fk_quest_id",
        viewonly=True
    )

    rel_user = db.relationship(
        "User",
        primaryjoin="User.user_id==CharacterJoinRequest.fk_user_id",
        viewonly=True
    )

    rel_character = db.relationship(
        "Character",
        primaryjoin="Character.character_id==CharacterJoinRequest.fk_character_id",
        viewonly=True
    )
