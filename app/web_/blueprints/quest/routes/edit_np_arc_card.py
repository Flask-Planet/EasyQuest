from flask import render_template, redirect, url_for, flash, request
from flask_imp.security import login_check

from app.web_.models.quest import Quest
from app.web_.sql import np_arc_card_sql
from .. import bp


@bp.route("/<int:quest_id>/np-arc-card/<int:np_arc_card_id>/edit", methods=["GET", "POST"])
@login_check('authenticated', True, 'auth.login')
def edit_np_arc_card(quest_id, np_arc_card_id):
    #
    # POST
    #
    if request.method == "POST":
        np_arc_card_sql.update_np_arc_card(
            np_arc_card_id=np_arc_card_id,
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

        return redirect(url_for(
            "quest.edit",
            quest_id=quest_id,
            tab="np_arc_cards"
        ))

    #
    # GET
    #
    q_quest = Quest.read(id_=quest_id)

    if not q_quest:
        flash("Quest not found", "bad")
        return redirect(url_for("quests"))

    q_np_arc_card = np_arc_card_sql.get_by_id(np_arc_card_id)

    return render_template(
        bp.tmpl("edit-np-arc-card.html"),
        q_quest=q_quest,
        q_np_arc_card=q_np_arc_card,
    )
