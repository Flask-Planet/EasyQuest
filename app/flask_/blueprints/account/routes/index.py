from flask import render_template, session, redirect, url_for, flash
from flask_imp.security import login_check

from app.flask_.sql import user_sql
from .. import bp


@bp.route("/", methods=["GET"])
@login_check('authenticated', True, 'auth.login')
def index():
    user_id = session.get("user_id")
    user = user_sql.get_by_id(user_id)

    if not user:
        flash("You need to be logged in to view this page.", "error")
        return redirect(url_for("auth.logout"))

    return render_template(
        bp.tmpl("index.html"),
        user=user,
    )
