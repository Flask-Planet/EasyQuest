from flask import session, redirect, url_for, flash, request
from flask_imp.security import login_check

from app.flask_.sql import user_sql
from .. import bp


@bp.post("/update-account")
@login_check('authenticated', True, 'auth.login')
def update_account():
    user_id = session.get("user_id")
    user = user_sql.get_by_id(user_id)

    if not user:
        flash("You need to be logged in to view this page.", "error")
        return redirect(url_for("auth.logout"))

    first_name = request.form.get("first_name")
    email_address = request.form.get("email_address")

    if not first_name or not email_address:
        flash("First name and email address are required.", "error")
        return redirect(url_for("account.index"))

    if email_address != user.email_address:

        check_if_available = user_sql.get_using_email_address(email_address)

        if check_if_available:
            flash("Email address already in use.", "error")
            return redirect(url_for("account.index"))

    if first_name != user.first_name:
        session["user_name"] = first_name

    user_sql.update_user(user.user_id, first_name, email_address)

    flash("Account updated successfully.", "success")
    return redirect(url_for("account.index"))
