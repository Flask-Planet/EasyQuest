from flask import redirect, url_for, flash, session
from flask_imp.security import login_check, permission_check

from app.flask_.services import WebSocketService
from app.flask_.sql import quest_sql, quest_purgatory_sql, character_join_request_sql, character_sql
from .. import bp


@bp.get("/<string:quest_code>/leave")
@login_check('authenticated', True, 'auth.login')
def leave(quest_code):
    user_id = session.get("user_id")
    user_name = session.get("user_name")

    quest = quest_sql.get_by_quest_code(quest_code)

    if not quest:
        flash("Quest not found", "bad")
        return redirect(url_for("quests.index"))

    quest_purgatory_sql.delete_by_user_id(user_id)
    character_join_request_sql.delete_by_user_id(user_id)
    character_sql.delete_by_user_id(user_id)

    flash(
        f"You have left Quest [{quest_code}]", "good"
    )

    WebSocketService().send(
        quest_code=quest.quest_code,
        payload={
            'user_id': user_id,
            'action': 'send_to_user_in_quest',
            'data': {
                'user_id': quest.fk_user_id,
                'payload': {
                    'message': f'{user_name} has left the Quest!',
                    'message_status': 'bad'
                }
            }
        }
    )

    return redirect(url_for("quests.index"))
