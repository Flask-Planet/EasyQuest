import os

from flask import render_template, redirect, url_for, flash, session
from flask_imp.security import login_check

from app.flask_.sql import quest_sql, user_sql
from .. import bp


@bp.get("/<string:quest_code>/voyage")
@login_check('authenticated', True, 'auth.login')
def voyage(quest_code):
    q_quest = quest_sql.get_by_quest_code(quest_code)
    user_id = session.get("user_id")

    user = user_sql.get_by_id(user_id)

    if not q_quest:
        flash("Quest not found", "bad")
        return redirect(url_for("quests.index"))

    if q_quest.fk_user_id == user_id:
        flash("You are the owner of this quest, you must join as a quest master!", "bad")
        return redirect(url_for("quests.index"))

    # FUNCTIONALITY IS HANDED OFF TO ALPINEJS + API + WEBSOCKETS IN THE TEMPLATE
    return render_template(
        bp.tmpl("voyage/voyage.html"),
        q_quest=q_quest,
        ws_uri=f"{os.getenv('WS_URI')}/quest/{quest_code}/voyage",
        private_key=user.private_key,
    )
