from flask import session, redirect, url_for

from .. import bp


@bp.get("/logout")
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
