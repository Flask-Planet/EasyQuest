from flask import render_template
from flask_imp.security import login_check

from app.flask_.models.genre import Genre
from app.flask_.models.quest import Quest
from .. import bp


@bp.get("/quests")
@login_check('authenticated', True, 'auth.login')
def quests():
    q_quests = Quest.read(all_rows=True, order_by="created", order_desc=True)
    q_genres = Genre.read(all_rows=True, order_by="created")

    return render_template(
        bp.tmpl("quests.html"),
        q_quests=q_quests,
        q_genres=q_genres,
    )
