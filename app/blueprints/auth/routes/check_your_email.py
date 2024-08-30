from flask import render_template
from flask_imp.security import login_check

from .. import bp


@bp.get("/check-your-email")
@login_check('authenticated', False, fail_endpoint='www.quests')
def check_your_email():
    return render_template(bp.tmpl("check_your_email.html"))
