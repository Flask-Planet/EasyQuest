import random

from flask_imp.security import login_check

from .. import bp


@bp.get("/roll-dice")
@login_check('authenticated', True, 'auth.login')
def your_dice():
    # random dice roll
    roll = random.randint(1, 6)

    return {
        "roll": roll
    }
