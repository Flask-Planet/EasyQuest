from flask import render_template, request, session, redirect, url_for, flash
from flask_imp.security import login_check, include_csrf

from app.flask_.sql import user_sql
from .. import bp


@bp.get("/login")
@login_check('authenticated', False, fail_endpoint='quests.index')
@include_csrf()
def login():
    return render_template(bp.tmpl("login.html"))


@bp.post("/login")
@login_check('authenticated', False, fail_endpoint='quests')
@include_csrf()
def login_post():
    user = user_sql.login(
        email_address=request.form.get('email_address', None),
        password=request.form.get('password', None)
    )

    if user:
        session['authenticated'] = True
        session['user_id'] = user.user_id
        session['user_name'] = user.first_name
        session['permission_level'] = user.permission_level
        return redirect(url_for("quests.index"))

    flash("Invalid login credentials", "bad")
    return redirect(url_for('auth.login'))
