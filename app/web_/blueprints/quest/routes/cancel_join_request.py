from flask import redirect, url_for, flash, session
from flask_imp.security import login_check

from app.web_.services import WebSocketService
from app.web_.sql import quest_purgatory_sql, quest_sql
from .. import bp


@bp.get("/cancel-join-request/<int:quest_join_request_id>")
@login_check('authenticated', True, 'auth.login')
def cancel_join_request(quest_join_request_id):
    user_id = session.get("user_id")
    user_name = session.get("user_name")
    quest_join_request = quest_purgatory_sql.get_by_id(quest_join_request_id)

    if not quest_join_request:
        flash("Join request not found", "bad")
        return redirect(url_for("quests.index"))

    quest = quest_sql.get_by_id(quest_join_request.fk_quest_id)

    if not quest:
        flash("Quest not found", "bad")
        return redirect(url_for("quests.index"))

    if quest.fk_user_id == user_id:
        flash("You are the owner of this Quest, please join as a Quest Master", "bad")
        return redirect(url_for("quests.index"))

    quest_purgatory_sql.delete_by_id(quest_join_request_id)

    WebSocketService().send(
        quest_code=quest.quest_code,
        payload={
            'user_id': user_id,
            'action': 'send_to_user_in_quest',
            'data': {
                'user_id': quest.fk_user_id,
                'payload': {
                    'action': 'refresh_join_requests',
                    'message': f'{user_name} left purgatory!',
                    'message_status': 'message'
                }
            }
        }
    )

    return redirect(url_for("quests.index"))
