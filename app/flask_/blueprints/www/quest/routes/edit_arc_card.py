from flask import render_template, redirect, url_for, flash, request
from flask_imp.security import login_check, permission_check

from app.flask_.models.quest import Quest
from app.flask_.sql import arc_card_sql
from .. import bp


@bp.route("/quest/<int:quest_id>/arc-card/<int:arc_card_id>/edit", methods=["GET", "POST"])
@login_check('authenticated', True, 'auth.login')
@permission_check('permission_level', 10, 'www.index')
def edit_arc_card(quest_id, arc_card_id):
    #
    # POST
    #
    if request.method == "POST":
        arc_card_sql.update_arc_card(
            arc_card_id=arc_card_id,
            arc=request.form.get("arc"),
            description=request.form.get("description"),
            modifier=request.form.get("modifier"),
            bonus=request.form.get("bonus"),
            starting_weapon_name=request.form.get("starting_weapon_name"),
            starting_weapon_damage=request.form.get("starting_weapon_damage"),
            health=request.form.get("health"),
            defence=request.form.get("defence"),
            strength=request.form.get("strength"),
            agility=request.form.get("agility"),
            intelligence=request.form.get("intelligence"),
            luck=request.form.get("luck"),
            perception=request.form.get("perception"),
            persuasion=request.form.get("persuasion"),
        )

        return redirect(url_for("www.quest.edit", quest_id=quest_id, tab="arc_cards"))

    #
    # GET
    #
    q_quest = Quest.read(id_=quest_id)

    if not q_quest:
        flash("Quest not found", "bad")
        return redirect(url_for("www.quests"))

    q_arc_card = arc_card_sql.get_by_id(arc_card_id)

    return render_template(
        bp.tmpl("edit-arc-card.html"),
        q_quest=q_quest,
        q_arc_card=q_arc_card,
    )
