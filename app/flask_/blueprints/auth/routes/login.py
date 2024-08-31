from app.flask_.sql import user_sql
from flask import render_template, request, session, redirect, url_for, flash
from flask_imp.security import login_check
from .. import bp


@bp.get("/login")
@login_check('authenticated', False, fail_endpoint='www.quests')
def login():
    return render_template(bp.tmpl("login.html"))


@bp.post("/login")
@login_check('authenticated', False, fail_endpoint='www.quests')
def login_post():
    user = user_sql.login(
        email_address=request.form.get('email_address', None),
        password=request.form.get('password', None)
    )

    if user:
        session['authenticated'] = True
        session['user_id'] = user.user_id
        session['permission_level'] = user.permission_level
        return redirect(url_for('www.quests'))

    flash('Invalid login credentials', 'bad')
    return redirect(url_for('auth.login'))
