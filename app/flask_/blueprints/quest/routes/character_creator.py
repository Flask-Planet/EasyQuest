from flask import redirect, url_for, flash, session, render_template, request
from flask_imp.security import login_check

from app.flask_.sql import quest_sql, arc_card_sql, character_sql
from .. import bp


@bp.route("/<string:quest_code>/character-creator/arc/<int:arc_card_id>", methods=["GET", "POST"])
@login_check('authenticated', True, 'auth.login')
def character_creator(quest_code, arc_card_id):
    user_id = session.get("user_id")
    user_name = session.get("user_name")

    quest = quest_sql.get_by_quest_code(quest_code)

    if not quest:
        flash("Quest not found", "bad")
        return redirect(url_for("quests.index"))

    if quest.fk_user_id == user_id:
        flash("You are the owner of the Quest, you cannot create a character, you control the bad guys!", "bad")
        return redirect(url_for("quests.index"))

    arc_card = arc_card_sql.get_by_id(arc_card_id)

    if not arc_card:
        flash("Arc Card not found", "bad")
        return redirect(url_for("quest.purgatory", quest_code=quest_code))

    if request.method == "POST":
        full_name = request.form.get("full_name")
        back_story = request.form.get("back_story")

        character_sql.create(
            user_id=user_id,
            quest_id=quest.quest_id,
            full_name=full_name,
            back_story=back_story,
            display_picture="",
            arc_card_id=arc_card_id,
            arc=arc_card.arc,
            description=arc_card.description,
            modifier=arc_card.modifier,
            bonus=arc_card.bonus,
            weapon_name=arc_card.starting_weapon_name,
            weapon_damage=arc_card.starting_weapon_damage,
            health=arc_card.health,
            current_health=arc_card.health,
            defence=arc_card.defence,
            strength=arc_card.strength,
            agility=arc_card.agility,
            intelligence=arc_card.intelligence,
            luck=arc_card.luck,
            perception=arc_card.perception,
            persuasion=arc_card.persuasion,
            gold=10,
            inventory=[
                {
                    "code": "pc",
                    "name": "Purgatory Token",
                    "description": "A mysterious token that sits as a reminder of a strange place.",
                }
            ],
        )

        flash("Character created", "good")
        return redirect(url_for("quest.purgatory", quest_code=quest_code))

    return render_template(
        bp.tmpl("character_creator/character-creator.html"),
        quest=quest,
        user_name=user_name,
        arc_card=arc_card,
    )
