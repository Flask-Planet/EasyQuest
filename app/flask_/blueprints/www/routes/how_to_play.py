from flask import render_template
from flask_imp.security import login_check

from .. import bp


@bp.get("/how-to-play")
@login_check('authenticated', True, 'auth.login')
def how_to_play():
    return render_template(bp.tmpl("how-to-play.html"))
