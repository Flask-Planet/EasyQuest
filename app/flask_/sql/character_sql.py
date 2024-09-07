from sqlalchemy import select, func, delete, insert

from app.flask_.extensions import db
from app.flask_.models import Character


def create(
        user_id,
        quest_id,
        full_name,
        back_story,
        display_picture,
        arc_card_id,
        arc,
        description,
        modifier,
        bonus,
        weapon_name,
        weapon_damage,
        health,
        current_health,
        defence,
        strength,
        agility,
        intelligence,
        luck,
        perception,
        persuasion,
        gold,
        inventory
) -> None:
    sql = (
        insert(Character)
        .values(
            fk_user_id=user_id,
            fk_quest_id=quest_id,
            full_name=full_name,
            back_story=back_story,
            display_picture=display_picture,
            arc_card_id=arc_card_id,
            arc=arc,
            description=description,
            modifier=modifier,
            bonus=bonus,
            weapon_name=weapon_name,
            weapon_damage=weapon_damage,
            health=health,
            current_health=current_health,
            defence=defence,
            strength=strength,
            agility=agility,
            intelligence=intelligence,
            luck=luck,
            perception=perception,
            persuasion=persuasion,
            gold=gold,
            inventory=inventory
        )
    )
    db.session.execute(sql)
    db.session.commit()


def get_by_id(character_id) -> Character | None:
    sql = (
        select(Character)
        .where(Character.character_id == character_id)
    )
    return db.session.execute(sql).scalar_one_or_none()


def get_by_user_id(user_id) -> list[Character] | None:
    sql = (
        select(Character)
        .where(
            Character.fk_user_id == user_id
        )
    )
    return db.session.execute(sql).scalars().all()


def get_by_user_id_quest_id(user_id, quest_id) -> list[Character] | None:
    sql = (
        select(Character)
        .where(
            Character.fk_user_id == user_id,
            Character.fk_quest_id == quest_id
        )
    )
    return db.session.execute(sql).scalars().all()


def count_by_user_id_quest_id(user_id, quest_id) -> list[Character] | None:
    sql = (
        select(func.count(Character.character_id))
        .where(
            Character.fk_user_id == user_id,
            Character.fk_quest_id == quest_id
        )
    )
    return db.session.execute(sql).scalars().all()


def delete_by_id(character_id) -> None:
    sql = (
        delete(Character)
        .where(Character.character_id == character_id)
    )
    db.session.execute(sql)
    db.session.commit()


def delete_by_quest_id_user_id(quest_id, user_id) -> None:
    sql = (
        delete(Character)
        .where(
            Character.fk_quest_id == quest_id,
            Character.fk_user_id == user_id
        )
    )
    db.session.execute(sql)
    db.session.commit()


def delete_by_user_id(user_id) -> None:
    sql = (
        delete(Character)
        .where(Character.fk_user_id == user_id)
    )
    db.session.execute(sql)
    db.session.commit()
