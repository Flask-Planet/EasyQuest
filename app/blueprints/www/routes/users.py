from flask import render_template
from flask_imp.security import login_check, permission_check

from app.models.user import User
from .. import bp


@bp.get("/users")
@login_check('authenticated', True, 'auth.login')
@permission_check('permissions', 10, 'www.index')
def users():
    q_users = User.read(all_rows=True, order_by="created")

    return render_template(
        bp.tmpl("users.html"),
        q_users=q_users
    )
