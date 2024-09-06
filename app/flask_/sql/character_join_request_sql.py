from sqlalchemy import select, insert, update, delete

from app.flask_.extensions import db
from app.flask_.models import CharacterJoinRequest


def create(user_id, character_id, quest_id) -> CharacterJoinRequest:
    sql = (
        insert(CharacterJoinRequest)
        .returning(CharacterJoinRequest)
        .values(
            fk_user_id=user_id,
            fk_character_id=character_id,
            fk_quest_id=quest_id,
        )
    )
    result = db.session.execute(sql).scalar_one_or_none()
    db.session.commit()

    return result


def get_by_id(character_join_request_id) -> CharacterJoinRequest | None:
    sql = (
        select(CharacterJoinRequest)
        .where(CharacterJoinRequest.character_join_request_id == character_join_request_id)
    )
    return db.session.execute(sql).scalar_one_or_none()


def get_by_user_id(user_id) -> list[CharacterJoinRequest] | None:
    sql = (
        select(CharacterJoinRequest)
        .where(
            CharacterJoinRequest.fk_user_id == user_id
        )
    )
    return db.session.execute(sql).scalars().all()


def get_by_user_id_quest_id(user_id, quest_id) -> list[CharacterJoinRequest] | None:
    sql = (
        select(CharacterJoinRequest)
        .where(
            CharacterJoinRequest.fk_user_id == user_id,
            CharacterJoinRequest.fk_quest_id == quest_id,
        )
    )
    return db.session.execute(sql).scalars().all()


def get_by_quest_id(quest_id) -> list[CharacterJoinRequest] | None:
    sql = (
        select(CharacterJoinRequest)
        .where(CharacterJoinRequest.fk_quest_id == quest_id)
    )
    return db.session.execute(sql).scalars().all()


def get_pending_by_quest_id(quest_id) -> list[CharacterJoinRequest] | None:
    sql = (
        select(CharacterJoinRequest)
        .where(
            CharacterJoinRequest.fk_quest_id == quest_id,
            CharacterJoinRequest.accepted == False,
            CharacterJoinRequest.rejected == False,
        )
    )
    return db.session.execute(sql).scalars().all()


def get_accepted_by_quest_id(quest_id) -> list[CharacterJoinRequest] | None:
    sql = (
        select(CharacterJoinRequest)
        .where(
            CharacterJoinRequest.fk_quest_id == quest_id,
            CharacterJoinRequest.accepted == True,
            CharacterJoinRequest.rejected == False,
        )
    )
    return db.session.execute(sql).scalars().all()


def get_ignored_by_quest_id(quest_id) -> list[CharacterJoinRequest] | None:
    sql = (
        select(CharacterJoinRequest)
        .where(
            CharacterJoinRequest.fk_quest_id == quest_id,
            CharacterJoinRequest.accepted == False,
            CharacterJoinRequest.rejected == True,
        )
    )
    return db.session.execute(sql).scalars().all()


def accept(character_join_request_id) -> None:
    sql = (
        update(CharacterJoinRequest)
        .where(
            CharacterJoinRequest.character_join_request_id == character_join_request_id,
        )
        .values(
            accepted=True,
            rejected=False
        )
    )

    db.session.execute(sql)
    db.session.commit()


def reject(character_join_request_id) -> None:
    sql = (
        update(CharacterJoinRequest)
        .where(
            CharacterJoinRequest.character_join_request_id == character_join_request_id,
        )
        .values(
            accepted=False,
            rejected=True
        )
    )

    db.session.execute(sql)
    db.session.commit()


def delete_by_user_id(user_id) -> None:
    sql = (
        delete(CharacterJoinRequest)
        .where(
            CharacterJoinRequest.fk_user_id == user_id,
        )
    )

    db.session.execute(sql)
    db.session.commit()


def delete_by_id(character_join_request_id) -> None:
    sql = (
        delete(CharacterJoinRequest)
        .where(
            CharacterJoinRequest.character_join_request_id == character_join_request_id,
        )
    )

    db.session.execute(sql)
    db.session.commit()


def delete_by_character_id(character_id) -> None:
    sql = (
        delete(CharacterJoinRequest)
        .where(
            CharacterJoinRequest.fk_character_id == character_id,
        )
    )

    db.session.execute(sql)
    db.session.commit()
