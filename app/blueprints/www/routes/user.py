from flask import redirect, url_for
from flask_imp.security import login_check, permission_check

from app.models.user import User
from .. import bp


@bp.get("/enable/user/<user_id>")
@login_check('authenticated', True, 'auth.login')
@permission_check('permission_level', 10, 'www.index')
def enable_user(user_id):
    User.enable(user_id)
    return redirect(url_for('www.users'))


@bp.get("/disable/user/<user_id>")
@login_check('authenticated', True, 'auth.login')
@permission_check('permission_level', 10, 'www.index')
def disable_user(user_id):
    User.disable(user_id)
    return redirect(url_for('www.users'))
