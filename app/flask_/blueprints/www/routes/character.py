from flask import render_template, request, redirect, url_for, session
from flask_imp.security import login_check, permission_check

from app.flask_.models import dater
from app.flask_.models.character import Character
from app.flask_.models.quest import Quest
from .. import bp


@bp.get("/create-character")
@login_check('authenticated', True, 'auth.login')
def create_character():
    q_quests = Quest.read(field=('live', True), order_by="created")
    characters = Character.read(field=("fk_user_id", session.get('user_id')))

    existing_characters = {}
    for character in characters:
        existing_characters[character.fk_quest_id] = character.character_id

    return render_template(
        bp.tmpl("create-character.html"),
        q_quests=q_quests,
        existing_characters=existing_characters
    )


@bp.get("/create-character/for/<quest_id>")
@login_check('authenticated', True, 'auth.login')
def create_quest_character(quest_id):
    q_quest = Quest.read(id_=quest_id)
    arc_cards = q_quest.arc_cards

    return render_template(
        bp.tmpl("create-quest-character.html"),
        q_quest=q_quest,
        arc_cards=arc_cards,
    )


@bp.get("/edit-character/<character_id>/for/<quest_id>")
@login_check('authenticated', True, 'auth.login')
def edit_quest_character(character_id, quest_id):
    q_quest = Quest.read(id_=quest_id)
    arc_cards = q_quest.arc_cards

    q_character = Character.read(id_=character_id)

    return render_template(
        bp.tmpl("edit-quest-character.html"),
        q_quest=q_quest,
        arc_cards=arc_cards,
        q_character=q_character
    )


@bp.get("/approve-character/<character_id>/for/<quest_id>")
@login_check('authenticated', True, 'auth.login')
@permission_check('permission_level', 10, 'www.index')
def approve_quest_character(character_id, quest_id):
    Character.update(
        id_=character_id,
        values={
            "approved": True,
        }
    )

    return redirect(url_for("www.quest_character_manager", quest_id=quest_id))


@bp.get("/lock-character/<character_id>/for/<quest_id>")
@login_check('authenticated', True, 'auth.login')
@permission_check('permission_level', 10, 'www.index')
def lock_quest_character(character_id, quest_id):
    Character.update(
        id_=character_id,
        values={
            "locked": True,
        }
    )

    return redirect(url_for("www.quest_character_manager", quest_id=quest_id))


@bp.get("/unlock-character/<character_id>/for/<quest_id>")
@login_check('authenticated', True, 'auth.login')
@permission_check('permission_level', 10, 'www.index')
def unlock_quest_character(character_id, quest_id):
    Character.update(
        id_=character_id,
        values={
            "locked": False,
        }
    )

    return redirect(url_for("www.quest_character_manager", quest_id=quest_id))


@bp.post("/add-character/to/<quest_id>")
@login_check('authenticated', True, 'auth.login')
def add_character_to_quest(quest_id):
    full_name = request.form.get("full_name")
    arc_card_name = request.form.get("arc_card")
    back_story = request.form.get("back_story")

    q_quest = Quest.read(id_=quest_id)
    arc_cards = q_quest.arc_cards
    arc_card_json = arc_cards.get(arc_card_name, {})

    Character.create(values={
        "fk_user_id": session.get("user_id"),
        "fk_quest_id": quest_id,
        "full_name": full_name,
        "arc": arc_card_name,
        "arc_card": arc_card_json,
        "back_story": back_story,
        "created": dater(),
        **arc_card_json
    }, wash_attributes=True)

    return redirect(url_for("www.quest", quest_id=quest_id))


@bp.post("/update-character-stats/<character_id>/to/<quest_id>")
@login_check('authenticated', True, 'auth.login')
@permission_check('permission_level', 10, 'www.index')
def update_character_stats(character_id, quest_id):
    health = request.form.get("health")
    sleeping = True if request.form.get("sleeping") == 'true' else False
    confused = True if request.form.get("confused") == 'true' else False
    poisoned = True if request.form.get("poisoned") == 'true' else False
    buffed = True if request.form.get("buffed") == 'true' else False
    weapon = request.form.get("weapon")
    attack = request.form.get("attack")
    defence = request.form.get("defence")

    Character.update(
        id_=character_id,
        values={
            "health": health,
            "sleeping": sleeping,
            "confused": confused,
            "poisoned": poisoned,
            "buffed": buffed,
            "weapon": weapon,
            "attack": attack,
            "defence": defence,
        }
    )

    return redirect(url_for("www.quest_character_manager", quest_id=quest_id))


@bp.post("/update-character/<character_id>/to/<quest_id>")
@login_check('authenticated', True, 'auth.login')
def update_character_to_quest(character_id, quest_id):
    full_name = request.form.get("full_name")
    arc_card_name = request.form.get("arc_card")
    back_story = request.form.get("back_story")

    q_quest = Quest.read(id_=quest_id)
    arc_cards = q_quest.arc_cards
    arc_card_json = arc_cards.get(arc_card_name, {})

    Character.update(
        id_=character_id,
        values={
            "fk_user_id": session.get("user_id"),
            "fk_quest_id": quest_id,
            "full_name": full_name,
            "arc": arc_card_name,
            "arc_card": arc_card_json,
            "back_story": back_story,
            **arc_card_json
        },
        wash_attributes=True
    )

    return redirect(url_for("www.quest", quest_id=quest_id))


@bp.get("/delete-character/<character_id>/from/<quest_id>")
@login_check('authenticated', True, 'auth.login')
def delete_character_from_quest(character_id, quest_id):
    Character.delete(id_=character_id)

    return redirect(url_for("www.quest", quest_id=quest_id))


@bp.get("/character/stats/<character_id>")
@login_check('authenticated', True, 'auth.login')
def character_stats(character_id):
    character = Character.read(id_=character_id)

    if not character:
        return {
            "health": 0,
            "attack": 0,
            "defence": 0,
            "weapon": "",
            "sleeping": False,
            "confused": False,
            "poisoned": False,
            "buffed": False,
        }

    return {
        "health": character.health,
        "attack": character.attack,
        "defence": character.defence,
        "weapon": character.weapon,
        "sleeping": character.sleeping,
        "confused": character.confused,
        "poisoned": character.poisoned,
        "buffed": character.buffed,
    }
