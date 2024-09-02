import os

from flask import render_template, redirect, url_for, flash
from flask_imp.security import login_check

from app.flask_.sql import quest_sql
from .. import bp


@bp.get("/quest/<string:quest_code>/master")
@login_check('authenticated', True, 'auth.login')
def master(quest_code):
    q_quest = quest_sql.get_by_quest_code(quest_code)

    if not q_quest:
        flash("Quest not found", "bad")
        return redirect(url_for("www.quests"))

    # FUNCTIONALITY IS HANDED OFF TO ALPINEJS + API + WEBSOCKETS IN THE TEMPLATE
    return render_template(
        bp.tmpl("master/index.html"),
        q_quest=q_quest,
        ws_uri=os.getenv("WS_URI"),
    )
