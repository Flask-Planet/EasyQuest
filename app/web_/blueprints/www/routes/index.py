from flask import url_for, redirect
from flask_imp.security import login_check

from .. import bp


@bp.get("/")
@login_check('authenticated', True, 'auth.login')
def index():
    return redirect(url_for("quests.index"))
