from flask_imp.security import login_check

from app.web_.sql import character_sql
from app.utilities import APIResponse
from .. import bp


@bp.route("/user/<int:user_id>/character/<int:character_id>", methods=["GET"])
@login_check('authenticated', True, 'auth.login')
def character(user_id, character_id):
    character = character_sql.get_by_id(character_id)
    if not character:
        return APIResponse.fail("Character not found", 404)

    if character.fk_user_id != user_id:
        return APIResponse.fail("Character not found", 404)

    return APIResponse.success(
        "Users character",
        {
            'character_id': character.character_id,
            'full_name': character.full_name,
            'back_story': character.back_story,
            'display_picture': character.display_picture,
            'arc': character.arc,
            'description': character.description,
            'modifier': character.modifier,
            'bonus': character.bonus,
            'weapon_name': character.weapon_name,
            'weapon_damage': character.weapon_damage,
            'health': character.health,
            'current_health': character.current_health,
            'defence': character.defence,
            'strength': character.strength,
            'agility': character.agility,
            'intelligence': character.intelligence,
            'luck': character.luck,
            'perception': character.perception,
            'persuasion': character.persuasion,
            'sleeping': character.sleeping,
            'confused': character.confused,
            'poisoned': character.poisoned,
            'buffed': character.buffed,
            'gold': character.gold,
            'inventory': [
                {
                    'name': item.name,
                    'description': item.description,
                }
                for item in character.inventory
            ],
        }
    )
