from sqlalchemy import select, update

from app.flask_.extensions import db
from app.flask_.models import Quest


def get_by_id(quest_id) -> Quest | None:
    sql = (
        select(Quest)
        .where(Quest.quest_id == quest_id)
    )
    return db.session.execute(sql).scalar_one_or_none()


def get_by_user_id(user_id) -> list[Quest] | None:
    sql = (
        select(Quest)
        .where(Quest.fk_user_id == user_id)
    )
    return db.session.execute(sql).scalars().all()


def get_by_quest_code_list(quest_codes: list) -> list[Quest] | None:
    sql = (
        select(Quest)
        .where(Quest.quest_code.in_(quest_codes))
    )
    return db.session.execute(sql).scalar_one_or_none()


def get_by_quest_code(quest_code) -> Quest | None:
    sql = (
        select(Quest)
        .where(Quest.quest_code == quest_code)
    )
    return db.session.execute(sql).scalar_one_or_none()


def update_arc_cards(quest_id, arc_cards) -> Quest | None:
    quest = get_by_id(quest_id)

    if not quest:
        return None

    sql = (
        update(Quest)
        .where(Quest.quest_id == quest_id)
        .values({
            'arc_cards': arc_cards
        })
        .returning(Quest)
    )

    return db.session.execute(sql).scalar_one_or_none()
