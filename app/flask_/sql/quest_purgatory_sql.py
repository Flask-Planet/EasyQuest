from sqlalchemy import select, insert, update, delete

from app.flask_.extensions import db
from app.flask_.models import QuestPurgatory


def create(quest_id, user_id, quest_code) -> QuestPurgatory:
    sql = (
        insert(QuestPurgatory)
        .returning(QuestPurgatory)
        .values(
            fk_quest_id=quest_id,
            fk_user_id=user_id,
            quest_code=quest_code
        )
    )
    result = db.session.execute(sql).scalar_one_or_none()
    db.session.commit()

    return result


def get_by_id(quest_purgatory_id) -> QuestPurgatory | None:
    sql = (
        select(QuestPurgatory)
        .where(QuestPurgatory.quest_purgatory_id == quest_purgatory_id)
    )
    return db.session.execute(sql).scalar_one_or_none()


def get_by_user_id(user_id) -> list[QuestPurgatory] | None:
    sql = (
        select(QuestPurgatory)
        .where(
            QuestPurgatory.fk_user_id == user_id
        )
    )
    return db.session.execute(sql).scalars().all()


def get_joined(user_id, quest_id) -> QuestPurgatory | None:
    sql = (
        select(QuestPurgatory)
        .where(
            QuestPurgatory.fk_user_id == user_id,
            QuestPurgatory.fk_quest_id == quest_id,
        )
    )
    return db.session.execute(sql).scalar_one_or_none()


def get_by_quest_id(quest_id) -> list[QuestPurgatory] | None:
    sql = (
        select(QuestPurgatory)
        .where(QuestPurgatory.fk_quest_id == quest_id)
    )
    return db.session.execute(sql).scalars().all()


def get_by_quest_id_user_id(quest_id, user_id) -> QuestPurgatory:
    sql = (
        select(QuestPurgatory)
        .where(
            QuestPurgatory.fk_quest_id == quest_id,
            QuestPurgatory.fk_user_id == user_id
        )
    )
    return db.session.execute(sql).scalar_one_or_none()


def get_by_quest_code(quest_code) -> list[QuestPurgatory] | None:
    sql = (
        select(QuestPurgatory)
        .where(QuestPurgatory.quest_code == quest_code)
    )

    return db.session.execute(sql).scalars().all()


def block(quest_purgatory_id, user_id) -> None:
    sql = (
        update(QuestPurgatory)
        .where(
            QuestPurgatory.quest_purgatory_id == quest_purgatory_id,
            QuestPurgatory.fk_user_id == user_id
        )
        .values(
            blocked=True
        )
    )

    db.session.execute(sql)
    db.session.commit()


def unblock(quest_purgatory_id, user_id) -> None:
    sql = (
        update(QuestPurgatory)
        .where(
            QuestPurgatory.quest_purgatory_id == quest_purgatory_id,
            QuestPurgatory.fk_user_id == user_id
        )
        .values(
            blocked=False
        )
    )

    db.session.execute(sql)
    db.session.commit()


def delete_by_user_id(user_id) -> None:
    sql = (
        delete(QuestPurgatory)
        .where(
            QuestPurgatory.fk_user_id == user_id,
        )
    )

    db.session.execute(sql)
    db.session.commit()


def delete_by_id(quest_purgatory_id) -> None:
    sql = (
        delete(QuestPurgatory)
        .where(
            QuestPurgatory.quest_purgatory_id == quest_purgatory_id,
        )
    )

    db.session.execute(sql)
    db.session.commit()
