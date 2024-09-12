from flask import session, redirect, url_for, flash
from flask_imp.security import login_check

from app.web_.sql import user_sql, quest_sql, quest_purgatory_sql, character_sql, character_join_request_sql
from .. import bp


@bp.route("/delete", methods=["GET"])
@login_check('authenticated', True, 'auth.login')
def delete():
    user_id = session.get("user_id")
    user = user_sql.get_by_id(user_id)

    if not user:
        flash("You need to be logged in to view this page.", "error")
        return redirect(url_for("auth.logout"))

    # Delete all users quests
    users_quests = quest_sql.get_by_user_id(user_id)
    if users_quests:
        for quest in users_quests:
            quest_sql.delete_by_id(quest.quest_id)

    # Delete all users joined quests
    quest_purgatory_sql.delete_by_user_id(user_id)

    # Delete all users character join requests for quests
    character_join_request_sql.delete_by_user_id(user_id)

    # Delete all users characters
    character_sql.delete_by_user_id(user_id)

    # Delete user
    user_sql.delete_by_id(user_id)

    return redirect(url_for("auth.logout"))
