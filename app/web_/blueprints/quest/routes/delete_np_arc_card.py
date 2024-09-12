from flask import redirect, url_for
from flask_imp.security import login_check

from app.web_.sql import np_arc_card_sql
from .. import bp


@bp.get("/<int:quest_id>/np-arc-card/<int:np_arc_card_id>/delete")
@login_check('authenticated', True, 'auth.login')
def delete_np_arc_card(quest_id, np_arc_card_id):
    np_arc_card_sql.delete_by_id(np_arc_card_id)
    return redirect(url_for("quest.edit", quest_id=quest_id, tab="np_arc_cards"))
