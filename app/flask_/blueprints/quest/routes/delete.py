from flask import redirect, url_for, flash
from flask_imp.security import login_check, permission_check

from app.flask_.models.quest import Quest
from .. import bp


@bp.get("/<quest_id>/delete")
@login_check('authenticated', True, 'auth.login')
@permission_check('permission_level', 10, 'www.index')
def delete(quest_id):
    Quest.delete(fields={"quest_id": quest_id}, return_deleted=True)
    flash("Quest deleted", "good")
    return redirect(url_for("quests.index"))
