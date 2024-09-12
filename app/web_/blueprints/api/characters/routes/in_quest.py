from flask_imp.security import login_check

from app.web_.sql import character_sql
from app.utilities import APIResponse
from .. import bp


@bp.route("/user/<int:user_id>/in-quest/<int:quest_id>", methods=["GET"])
@login_check('authenticated', True, 'auth.login')
def in_quest(user_id, quest_id):
    characters = character_sql.get_by_user_id_quest_id(user_id, quest_id)

    return APIResponse.success(
        "Characters in quest",
        [
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
                'inventory': character.inventory,
            }
            for character in characters
        ]
    )
