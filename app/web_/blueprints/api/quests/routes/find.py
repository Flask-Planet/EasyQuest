from flask import session, url_for
from flask_imp.security import login_check

from app.web_.sql import quest_sql, quest_purgatory_sql
from app.utilities import APIResponse
from .. import bp


@bp.get("/find/<string:quest_code>")
@login_check('authenticated', True, 'auth.login')
def find(quest_code):
    # api.quests.find

    user_id = session.get("user_id")

    quest = quest_sql.get_by_quest_code(quest_code)

    if not quest:
        return APIResponse.fail(
            "Quest not found",
            {}
        )

    joined = quest_purgatory_sql.get_joined(user_id, quest.quest_id)

    if joined:
        return APIResponse.fail(
            "You have already requested to join this quest",
            {}
        )

    return APIResponse.success(
        'Quest found',
        {
            'quest_id': quest.quest_id,
            'genre_id': quest.fk_genre_id,
            'quest_code': quest.quest_code,
            'title': quest.title,
            'summary': quest.summary,
            'genre': quest.rel_genre.genre,
            'building': quest.building,
            'live': quest.live,
            'finished': quest.finished,
        }
    )
