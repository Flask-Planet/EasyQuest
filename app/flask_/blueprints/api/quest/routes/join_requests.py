from flask_imp.security import login_check

from app.flask_.globals import APIResponse
from app.flask_.sql import quest_sql
from .. import bp


@bp.get("/quest/<int:quest_id>/join-requests")
@login_check('authenticated', True, 'auth.login')
def join_requests(quest_id):
    quest = quest_sql.get_by_id(quest_id)

    if not quest:
        return APIResponse.fail(
            "Quest not found",
            404
        )

    return APIResponse.success(
        "Arc Cards",
        [{
            'arc_card_id': card.arc_card_id,
            **card.card
        } for card in quest.rel_arc_cards]
    )
