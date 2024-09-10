from flask import redirect, url_for, flash
from flask_imp.security import login_check

from app.flask_.sql import quest_sql
from .. import bp


@bp.get("/<quest_id>/delete")
@login_check('authenticated', True, 'auth.login')
def delete(quest_id):
    quest = quest_sql.get_by_id(quest_id)

    if not quest:
        flash("Quest not found", "bad")
        return redirect(url_for("quests.index"))

    quest_sql.delete_by_id(quest_id)

    flash("Quest deleted", "good")
    return redirect(url_for("quests.index"))
