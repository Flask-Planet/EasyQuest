from flask import session, url_for
from flask_imp.security import login_check

from app.flask_.sql import quest_purgatory_sql, character_sql
from app.utilities import APIResponse
from .. import bp


@bp.get("/<string:quest_code>/user/<int:user_id>/character-join-requests")
@login_check('authenticated', True, 'auth.login')
def user_character_join_requests(quest_code):
    # api.quests.user_character_join_requests

    user_id = session.get("user_id")

    character_join_requests = quest_purgatory_sql.get_by_user_id(user_id)

    return APIResponse.success(
        'Joint requests retrieved',
        join_requests
    )
