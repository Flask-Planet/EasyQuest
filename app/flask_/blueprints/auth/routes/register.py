from flask import render_template, request, flash, redirect, url_for, session
from flask_imp.security import login_check, include_csrf

from app.flask_.models import User
from app.flask_.sql import user_sql
from .. import bp


@bp.route("/register", methods=["GET", "POST"])
@login_check('authenticated', False, fail_endpoint='quests.index')
@include_csrf()
def register():
    #
    # POST
    #
    if request.method == "POST":

        first_name = request.form.get('first_name', None)
        email_address = request.form.get('email_address', None)
        password = request.form.get('password', None)
        password_confirm = request.form.get('password_confirm', None)

        if password != password_confirm:
            flash("Passwords do not match", "bad")
            return render_template(
                bp.tmpl("register.html"),
                first_name=first_name,
                email_address=email_address,
            )

        if User.exists(email_address=email_address):
            flash("Email address already in use", "bad")
            return render_template(
                bp.tmpl("register.html"),
                first_name=first_name,
            )

        user = user_sql.add_user(
            first_name=first_name,
            email_address=email_address,
            password=password,
        )

        session['authenticated'] = True
        session['user_id'] = user.user_id
        session['user_name'] = user.first_name
        session['permission_level'] = user.permission_level

        # zepto_service = ZeptoEmailService(zepto_settings)
        #
        # zepto_service.send(
        #     [user.email_address],
        #     "Welcome to EasyQuest",
        #     render_template(bp.tmpl("email__welcome.html"), user=user),
        # )

        flash("Registration successful", "good")
        return redirect(url_for('quests.index'))

    #
    # GET
    #
    return render_template(bp.tmpl("register.html"))
