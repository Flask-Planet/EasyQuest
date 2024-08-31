from flask import redirect, url_for
from flask_imp.security import login_check, permission_check

from app.flask_.extensions import db
from .. import bp


@bp.get("/reset-database")
@login_check('authenticated', 'auth.login')
@permission_check('permission_level', 10, 'www.index')
def reset_database():
    db.drop_all()
    db.create_all()
    return redirect(url_for("www.index"))
