from sqlalchemy import select, update, insert, delete

from app.flask_.extensions import db
from app.flask_.models import ArcCard
from app.utilities import DatetimeDeltaMC


def get_by_id(arc_card_id) -> ArcCard | None:
    sql = (
        select(ArcCard)
        .where(ArcCard.arc_card_id == arc_card_id)
    )
    return db.session.execute(sql).scalar_one_or_none()


def get_by_quest_id(quest_id) -> list[ArcCard] | None:
    sql = (
        select(ArcCard)
        .where(ArcCard.fk_quest_id == quest_id)
    )
    return db.session.execute(sql).scalars().all()


def create_arc_card(
        fk_quest_id,
        arc,
        description=None,
        modifier=None,
        bonus=None,
        starting_weapon_name=None,
        starting_weapon_damage=None,
        health=None,
        defence=None,
        strength=None,
        agility=None,
        intelligence=None,
        luck=None,
        perception=None,
        persuasion=None,
) -> ArcCard:
    sql = (
        insert(ArcCard)
        .values(
            fk_quest_id=fk_quest_id,
            arc=arc,
            description=description,
            modifier=modifier,
            bonus=bonus,
            starting_weapon_name=starting_weapon_name,
            starting_weapon_damage=starting_weapon_damage,
            health=health,
            defence=defence,
            strength=strength,
            agility=agility,
            intelligence=intelligence,
            luck=luck,
            perception=perception,
            persuasion=persuasion,
            order=0,
            created=DatetimeDeltaMC().datetime,
        )
        .returning(ArcCard)
    )

    result = db.session.execute(sql).scalar_one()
    db.session.commit()

    return result


def create_arc_cards_from_json(quest_id, arc_cards_raw: dict[str, list]):
    arc_cards = arc_cards_raw.get('arc_cards', [])

    def health(value):
        if not isinstance(value, int):
            return 100
        if value < 1:
            return 100
        return value

    def defence(value):
        if not isinstance(value, int):
            return 1
        if value < 1:
            return 1
        if value > 5:
            return 5
        return value

    def int_val(value):
        if isinstance(value, str):
            try:
                return int(value)
            except ValueError:
                return 0
        if not isinstance(value, int):
            return 0
        return value

    def str_val(value):
        if isinstance(value, str):
            return value
        return ''

    for c in arc_cards:
        db.session.execute(
            insert(ArcCard).values(
                fk_quest_id=quest_id,
                arc=str_val(c.get('arc', 'UNKNOWN')),
                description=str_val(c.get('description', '')),
                modifier=str_val(c.get('modifier', '')),
                bonus=str_val(c.get('bonus', '')),
                starting_weapon_name=str_val(c.get('starting_weapon_name', 'Unarmed')),
                starting_weapon_damage=int_val(c.get('starting_weapon_damage', 5)),
                health=health(c.get('health', 100)),
                defence=defence(c.get('defence', 1)),
                strength=int_val(c.get('strength', 0)),
                agility=int_val(c.get('agility', 0)),
                intelligence=int_val(c.get('intelligence', 0)),
                luck=int_val(c.get('luck', 0)),
                perception=int_val(c.get('perception', 0)),
                persuasion=int_val(c.get('persuasion', 0)),
                order=int_val(c.get('order', 0)),
                created=DatetimeDeltaMC().datetime,
            )
        )

    db.session.commit()


def update_arc_card(
        arc_card_id,
        arc,
        description=None,
        modifier=None,
        bonus=None,
        starting_weapon_name=None,
        starting_weapon_damage=None,
        health=None,
        defence=None,
        strength=None,
        agility=None,
        intelligence=None,
        luck=None,
        perception=None,
        persuasion=None,
) -> ArcCard | None:
    sql = (
        update(ArcCard)
        .where(ArcCard.arc_card_id == arc_card_id)
        .values(
            arc=arc,
            description=description,
            modifier=modifier,
            bonus=bonus,
            starting_weapon_name=starting_weapon_name,
            starting_weapon_damage=starting_weapon_damage,
            health=health,
            defence=defence,
            strength=strength,
            agility=agility,
            intelligence=intelligence,
            luck=luck,
            perception=perception,
            persuasion=persuasion,
        )
        .returning(ArcCard)
    )

    result = db.session.execute(sql).scalar_one_or_none()
    db.session.commit()

    return result


def delete_by_id(arc_card_id) -> int:
    sql = (
        delete(ArcCard)
        .where(ArcCard.arc_card_id == arc_card_id)
    )

    db.session.execute(sql)
    db.session.commit()

    return arc_card_id


def delete_by_quest_id(quest_id) -> int:
    sql = (
        delete(ArcCard)
        .where(ArcCard.fk_quest_id == quest_id)
    )

    db.session.execute(sql)
    db.session.commit()

    return quest_id
