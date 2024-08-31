from app.flask_.config import zepto_settings
from app.flask_.services.zepto import ZeptoEmailService
from app.flask_.sql import user_sql
from flask import render_template, request, flash, redirect, url_for
from flask_imp.auth import generate_password
from flask_imp.security import login_check
from .. import bp


@bp.get("/forgot-password")
@login_check('authenticated', False, fail_endpoint='www.quests')
def forgot_password():
    return render_template(bp.tmpl("forgot_password.html"))


@bp.post("/forgot-password")
@login_check('authenticated', False, fail_endpoint='www.quests')
def forgot_password_post():
    user = user_sql.get_using_email_address(request.form.get('email_address', None))

    if user:
        password = user_sql.reset_password(user.email_address, generate_password())

        zepto_service = ZeptoEmailService(zepto_settings)
        zepto_service.send(
            [user.email_address],
            "EasyQuest: Your New Password",
            render_template(bp.tmpl("email__forgot_password.html"), password=password),
        )

        flash('Your new password has been sent to your email address', 'good')
        return redirect(url_for('auth.check_your_email'))

    flash('Invalid email address', 'bad')
    return redirect(url_for('auth.forgot_password'))
