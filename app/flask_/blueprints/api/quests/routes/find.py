from flask import session, url_for
from flask_imp.security import login_check

from app.flask_.sql import quest_sql, quest_purgatory_sql
from app.utilities import APIResponse
from .. import bp


@bp.get("/find/<string:quest_code>")
@login_check('authenticated', True, 'auth.login')
def find(quest_code):
    # api.quests.find

    user_id = session.get("user_id")

    q_quest = quest_sql.get_by_quest_code(quest_code)

    if not q_quest:
        return APIResponse.fail(
            "Quest not found",
            {}
        )

    q_joined = quest_purgatory_sql.get_joined(user_id, q_quest.quest_id)

    if q_joined:
        return APIResponse.fail(
            "You have already requested to join this quest",
            {}
        )

    return APIResponse.success(
        'Quest found',
        {
            'quest_id': q_quest.quest_id,
            'quest_code': q_quest.quest_code,
            'title': q_quest.title,
            'summary': q_quest.summary,
            'genre': q_quest.rel_genre.genre,  # 2 LEVEL DEEP RELATIONSHIP
            'building': q_quest.building,
            'live': q_quest.live,
            'finished': q_quest.finished,
        }
    )
