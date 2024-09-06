from flask import session
from flask_imp.security import login_check

from app.flask_.services import WebSocketService
from app.flask_.sql import quest_purgatory_sql, quest_sql
from app.utilities import APIResponse
from .. import bp


@bp.get("/join/<int:quest_id>")
@login_check('authenticated', True, 'auth.login')
def join(quest_id):
    # api.quests.join

    user_id = session.get("user_id")
    user_name = session.get("user_name")

    quest = quest_sql.get_by_id(quest_id)

    if not quest:
        return APIResponse.fail(
            'Quest not found'
        )

    if quest.fk_user_id == user_id:
        return APIResponse.fail(
            'You are the owner of this Quest, please join as a Quest Master'
        )

    quest_membership = quest_purgatory_sql.get_joined(user_id, quest_id)

    if quest_membership:
        return APIResponse.fail(
            'You have already requested to join this Quest'
        )

    quest_purgatory_sql.create(quest_id, user_id, quest.quest_code)

    WebSocketService().send(
        quest_code=quest.quest_code,
        payload={
            'user_id': user_id,
            'action': 'send_to_user_in_quest',
            'data': {
                'user_id': quest.fk_user_id,
                'payload': {
                    'message': f'{user_name} has joined the Quest!',
                    'message_status': 'good'
                }
            }
        }
    )

    return APIResponse.success(
        "Quest joined",
        {
            'quest_id': quest_id,
            'quest_code': quest.quest_code
        }
    )
