from flask import request
from flask_imp.security import login_check, permission_check

from app.web_.sql import quest_sql, arc_card_sql
from app.utilities import APIResponse
from .. import bp


@bp.get("/quest/<int:quest_id>/arc-cards")
@login_check('authenticated', True, 'auth.login')
@permission_check('permission_level', 10, 'www.index')
def quest_edit_get_arc_cards(quest_id):
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


@bp.post("/quest/edit/<int:quest_id>/create-arc-cards-from-json")
@login_check('authenticated', True, 'auth.login')
@permission_check('permission_level', 10, 'www.index')
def quest_edit_create_arc_cards_from_json(quest_id):
    if not request.json:
        return APIResponse.fail(
            "Invalid request",
            400
        )

    json_arc_cards = request.json.get('json_arc_cards', [])

    arc_card_sql.create_arc_cards_from_json(quest_id, json_arc_cards)

    return APIResponse.success(
        "Arc Cards From JSON Created",
        json_arc_cards
    )


@bp.post("/quest/edit/<int:quest_id>/create-arc-card")
@login_check('authenticated', True, 'auth.login')
@permission_check('permission_level', 10, 'www.index')
def quest_edit_create_arc_card(quest_id):
    if not request.json:
        return APIResponse.fail(
            "Invalid request",
            400
        )

    arc_card = request.json.get('arc_card', {})
    result = arc_card_sql.create_arc_card(quest_id, arc_card)

    return APIResponse.success(
        "Arc Card Created",
        {
            'arc_card_id': result.arc_card_id,
            **result.card
        }
    )


@bp.post("/quest/edit/update-arc-card/<int:arc_card_id>")
@login_check('authenticated', True, 'auth.login')
@permission_check('permission_level', 10, 'www.index')
def quest_edit_update_arc_cards(arc_card_id):
    if not request.json:
        return APIResponse.fail(
            "Invalid request",
            400
        )

    arc_card = request.json.get('arc_card', {})
    result = arc_card_sql.update_arc_card(arc_card_id, arc_card)

    return APIResponse.success(
        "Arc Card Updated",
        {
            'arc_card_id': result.arc_card_id,
            **result.card
        }
    )


@bp.get("/quest/edit/delete-arc-card/<int:arc_card_id>")
@login_check('authenticated', True, 'auth.login')
@permission_check('permission_level', 10, 'www.index')
def quest_edit_delete_arc_card(arc_card_id):
    arc_card_sql.delete_by_id(arc_card_id)

    return APIResponse.success(
        "Arc Card Created",
        arc_card_id
    )
