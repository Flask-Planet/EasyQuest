from flask_imp.security import login_check

from app.web_.sql import arc_card_sql
from app.utilities import APIResponse
from .. import bp


@bp.get("/arc-cards/<int:quest_id>")
@login_check('authenticated', True, 'auth.login')
def arc_cards(quest_id):
    # api.quests.arc_cards

    q_arc_cards = arc_card_sql.get_by_quest_id(quest_id)

    if not q_arc_cards:
        return APIResponse.fail(
            "Arc cards not found",
            {}
        )

    return APIResponse.success(
        'Arc cards found',
        [
            {
                'arc_card_id': arc_card.arc_card_id,
                'arc': arc_card.arc,
                'description': arc_card.description,
                'modifier': arc_card.modifier,
                'bonus': arc_card.bonus,
                'starting_weapon_name': arc_card.starting_weapon_name,
                'starting_weapon_damage': arc_card.starting_weapon_damage,
                'health': arc_card.health,
                'defence': arc_card.defence,
                'strength': arc_card.strength,
                'agility': arc_card.agility,
                'intelligence': arc_card.intelligence,
                'luck': arc_card.luck,
                'perception': arc_card.perception,
                'persuasion': arc_card.persuasion,
                'order': arc_card.order,
                'created': arc_card.created,
            }
            for arc_card in q_arc_cards
        ]
    )
