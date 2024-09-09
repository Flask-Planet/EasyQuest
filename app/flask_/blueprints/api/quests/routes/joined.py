from flask import session, url_for
from flask_imp.security import login_check

from app.flask_.sql import quest_purgatory_sql, character_sql
from app.utilities import APIResponse
from .. import bp


@bp.get("/joined")
@login_check('authenticated', True, 'auth.login')
def joined():
    # api.quests.joined

    user_id = session.get("user_id")

    quest_memberships = quest_purgatory_sql.get_by_user_id(user_id)

    join_requests = []

    for membership in quest_memberships:
        quest = membership.rel_quest

        join_requests.append(
            {
                'quest_purgatory_id': membership.quest_purgatory_id,
                '__quest__': {
                    'purgatory_url': url_for('quest.purgatory', quest_code=quest.quest_code),
                    'quest_id': quest.quest_id,
                    'genre_id': quest.fk_genre_id,
                    'quest_code': quest.quest_code,
                    'title': quest.title,
                    'summary': quest.summary,
                    'summary_truncated': quest.summary[:80] + '...' if len(quest.summary) > 80 else quest.summary,
                    'genre': quest.rel_genre.genre,  # 2 LEVEL DEEP RELATIONSHIP
                    'building': quest.building,
                    'live': quest.live,
                    'finished': quest.finished,
                }
            }
        )

    return APIResponse.success(
        'Quest memberships retrieved',
        join_requests
    )
