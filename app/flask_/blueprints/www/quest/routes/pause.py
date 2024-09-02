from flask import request, redirect, url_for, flash
from flask_imp.security import login_check, permission_check

from app.flask_.models.quest import Quest
from .. import bp


@bp.get("/quest/<quest_id>/pause")
@login_check('authenticated', True, 'auth.login')
@permission_check('permission_level', 10, 'www.index')
def pause(quest_id):
    Quest.update(id_=quest_id, values={"live": False, "building": False})
    flash("Quest is now paused", "good")

    if request.args.get("var") == "edit":
        return redirect(url_for("www.quest.edit", quest_id=quest_id))

    return redirect(url_for("www.quest", quest_id=quest_id))
