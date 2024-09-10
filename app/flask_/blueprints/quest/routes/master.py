import os

from flask import render_template, redirect, url_for, flash, session, current_app
from flask_imp.security import login_check

from app.flask_.sql import quest_sql, user_sql
from .. import bp


@bp.get("/<string:quest_code>/master")
@login_check('authenticated', True, 'auth.login')
def master(quest_code):
    q_quest = quest_sql.get_by_quest_code(quest_code)

    user = user_sql.get_by_id(session.get("user_id"))

    if not q_quest:
        flash("Quest not found", "bad")
        return redirect(url_for("quests.index"))

    # FUNCTIONALITY IS HANDED OFF TO ALPINEJS + API + WEBSOCKETS IN THE TEMPLATE
    return render_template(
        bp.tmpl("master/master.html"),
        q_quest=q_quest,
        ws_uri=f"{current_app.config['WS_URI']}/quest/{quest_code}/master",
        private_key=user.private_key,
    )
