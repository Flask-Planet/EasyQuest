from flask import redirect, url_for
from flask_imp.security import login_check, permission_check

from app.flask_.sql import arc_card_sql
from .. import bp


@bp.get("/<int:quest_id>/arc-card/<int:arc_card_id>/delete")
@login_check('authenticated', True, 'auth.login')
@permission_check('permission_level', 10, 'www.index')
def delete_arc_card(quest_id, arc_card_id):
    arc_card_sql.delete_arc_card(arc_card_id)
    return redirect(url_for("quest.edit", quest_id=quest_id, tab="arc_cards"))
