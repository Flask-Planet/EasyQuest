from flask import render_template, redirect, url_for, flash, session, current_app
from flask_imp.security import login_check

from app.web_.sql import quest_sql, user_sql, character_sql
from .. import bp


@bp.get("/<string:quest_code>/<int:character_id>/voyage")
@login_check('authenticated', True, 'auth.login')
def voyage(quest_code, character_id):
    quest = quest_sql.get_by_quest_code(quest_code)
    user_id = session.get("user_id")

    user = user_sql.get_by_id(user_id)

    if not quest:
        flash("Quest not found", "bad")
        return redirect(url_for("quests.index"))

    if quest.fk_user_id == user_id:
        flash("You are the owner of this quest, you must join as a quest master!", "bad")
        return redirect(url_for("quests.index"))

    character = character_sql.get_by_id(character_id)

    if not character:
        flash("Character not found", "bad")
        return redirect(url_for("quests.index"))

    # FUNCTIONALITY IS HANDED OFF TO ALPINEJS + API + WEBSOCKETS IN THE TEMPLATE
    return render_template(
        bp.tmpl("voyage/voyage.html"),
        quest=quest,
        character=character,
        ws_uri=f"{current_app.config['WS_URI']}/quest/{quest_code}/voyage",
        private_key=user.private_key,
    )
