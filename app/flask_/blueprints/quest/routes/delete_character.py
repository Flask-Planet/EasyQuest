from flask import redirect, url_for, flash, session
from flask_imp.security import login_check

from app.flask_.services import WebSocketService
from app.flask_.sql import quest_sql, character_sql, character_join_request_sql
from .. import bp


@bp.get("/<string:quest_code>/delete-character/<int:character_id>")
@login_check('authenticated', True, 'auth.login')
def delete_character(quest_code, character_id):
    user_id = session.get("user_id")
    user_name = session.get("user_name")

    quest = quest_sql.get_by_quest_code(quest_code)

    if not quest:
        flash("Quest not found", "bad")
        return redirect(url_for("quests.index"))

    if quest.fk_user_id == user_id:
        flash("You are the owner of the Quest, you cannot delete a character, you control the bad guys!", "bad")
        return redirect(url_for("quests.index"))

    character_join_request_sql.delete_by_character_id(character_id)
    character_sql.delete_by_id(character_id)

    WebSocketService().send(
        quest_code=quest.quest_code,
        payload={
            'user_id': user_id,
            'action': 'send_to_user_in_quest',
            'data': {
                'user_id': quest.fk_user_id,
                'payload': {
                    'message': f'{user_name} has deleted a character!',
                    'message_status': 'bad'
                }
            }
        }
    )

    flash("Character deleted", "good")
    return redirect(url_for("quest.purgatory", quest_code=quest_code))
