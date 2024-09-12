from flask import render_template, session
from flask_imp.security import login_check

from app.web_.sql import quest_sql
from .. import bp


@bp.get("/")
@login_check('authenticated', True, 'auth.login')
def index():
    user_id = session.get("user_id")
    users_quests = quest_sql.get_by_user_id(user_id)

    return render_template(
        bp.tmpl("quests.html"),
        users_quests=users_quests
    )
