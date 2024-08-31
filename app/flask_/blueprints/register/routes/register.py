from flask import render_template, request, flash, redirect, url_for, session
from flask_imp.security import login_check

from app.flask_.config import zepto_settings
from app.flask_.services.zepto import ZeptoEmailService
from app.flask_.models import User
from .. import bp


@bp.get("/")
@login_check('authenticated', False, fail_endpoint='www.quests')
def register():
    return render_template(bp.tmpl("register.html"))


@bp.post("/")
@login_check('authenticated', False, fail_endpoint='www.quests')
def register_post():
    first_name = request.form.get('first_name', None)
    email_address = request.form.get('email_address', None)
    password = request.form.get('password', None)
    password_confirm = request.form.get('password_confirm', None)

    if password != password_confirm:
        flash('Passwords do not match', 'bad')
        session.get('temp', {}).update({
            'first_name': first_name,
        })
        return redirect(url_for('register.register'))

    if User.exists(email_address=email_address):
        flash('Email address already in use', 'bad')
        session.get('temp', {}).update({
            'first_name': first_name,
        })
        return redirect(url_for('register.register'))

    user = User.add_user(
        first_name=first_name,
        email_address=email_address,
        password=password,
    )

    session['authenticated'] = True
    session['user_id'] = user.user_id
    session['permission_level'] = user.permission_level

    zepto_service = ZeptoEmailService(zepto_settings)

    zepto_service.send(
        [user.email_address],
        "Welcome to EasyQuest",
        render_template(bp.tmpl("email__welcome.html"), user=user),
    )

    flash('Registration successful', 'good')
    return redirect(url_for('www.quests'))
