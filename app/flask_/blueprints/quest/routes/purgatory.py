from flask import redirect, url_for, flash, session, render_template
from flask_imp.security import login_check

from app.flask_.sql import quest_sql
from .. import bp


@bp.get("/<string:quest_code>/purgatory")
@login_check('authenticated', True, 'auth.login')
def purgatory(quest_code):
    """
    Player's souls come here before they are sent to voyage on the quest.

    This gives them character creation options and a chance to read the quest
    """
    quest = quest_sql.get_by_quest_code(quest_code)

    user_id = session.get("user_id")
    user_name = session.get("user_name")

    if not quest:
        flash("Quest not found", "bad")
        return redirect(url_for("quests.index"))

    if quest.fk_user_id == user_id:
        flash("You are the owner of this quest, you must join as a quest master!", "bad")
        return redirect(url_for("quests.index"))

    return render_template(
        bp.tmpl("purgatory/purgatory.html"),
        quest=quest,
        user_id=user_id,
        user_name=user_name
    )
