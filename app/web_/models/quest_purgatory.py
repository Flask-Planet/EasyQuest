import sqlalchemy as sqla

from app.web_.extensions import db


class QuestPurgatory(db.Model):
    # PriKey
    quest_purgatory_id = sqla.Column(sqla.Integer, primary_key=True)

    # ForKey
    fk_user_id = sqla.Column(sqla.Integer, sqla.ForeignKey('user.user_id'), nullable=False)
    fk_quest_id = sqla.Column(sqla.Integer, sqla.ForeignKey('quest.quest_id'), nullable=False)

    quest_code = sqla.Column(sqla.String, nullable=False)
    blocked = sqla.Column(sqla.Boolean, default=False)

    rel_user = db.relationship(
        "User",
        primaryjoin="User.user_id==QuestPurgatory.fk_user_id",
        viewonly=True
    )

    rel_quest = db.relationship(
        "Quest",
        primaryjoin="Quest.quest_id==QuestPurgatory.fk_quest_id",
        viewonly=True
    )
