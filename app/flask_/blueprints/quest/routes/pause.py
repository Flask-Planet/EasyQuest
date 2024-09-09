from flask import request, redirect, url_for, flash
from flask_imp.security import login_check

from app.flask_.models.quest import Quest
from .. import bp


@bp.get("/<quest_id>/pause")
@login_check('authenticated', True, 'auth.login')
def pause(quest_id):
    Quest.update(id_=quest_id, values={"live": False, "building": False})
    flash("Quest is now paused", "good")

    if request.args.get("var") == "edit":
        return redirect(url_for("quest.edit", quest_id=quest_id))

    return redirect(url_for("www.quest", quest_id=quest_id))
