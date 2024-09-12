from flask import render_template, redirect, url_for, flash
from flask_imp.security import login_check

from app.web_.models.character import Character
from app.web_.models.quest import Quest
from .. import bp


@bp.get("/<quest_id>/character-manager")
@login_check('authenticated', True, 'auth.login')
def quest_character_manager(quest_id):
    q_quest = Quest.read(id_=quest_id)

    if not q_quest:
        flash("Quest not found", "bad")
        return redirect(url_for("quests.index"))

    waiting_characters = Character.read(
        fields={
            "fk_quest_id": quest_id,
            "approved": False,
        }
    )

    approved_characters = Character.read(
        fields={
            "fk_quest_id": quest_id,
            "approved": True,
        }
    )

    return render_template(
        bp.tmpl("quest-character-manager.html"),
        q_quest=q_quest,
        waiting_characters=waiting_characters,
        approved_characters=approved_characters,
    )
