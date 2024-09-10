from flask import session, redirect, url_for, flash, request
from flask_imp.security import login_check

from app.flask_.sql import user_sql
from .. import bp


@bp.post("/update-password")
@login_check('authenticated', True, 'auth.login')
def update_password():
    user_id = session.get("user_id")
    user = user_sql.get_by_id(user_id)

    if not user:
        flash("You need to be logged in to view this page.", "error")
        return redirect(url_for("auth.logout"))

    new_password = request.form.get("new_password")
    confirm_new_password = request.form.get("confirm_new_password")

    if new_password != confirm_new_password:
        flash("Passwords do not match.", "error")
        return redirect(url_for("account.index"))

    user_sql.reset_password(user.email_address, new_password)
    flash("Password updated successfully.", "success")
    return redirect(url_for("account.index"))
