import json

from flask import render_template, request, redirect, url_for, flash
from flask_imp.security import login_check, permission_check

from app.web_.models.quest import Quest
from app.web_.sql import arc_card_sql
from .. import bp


@bp.route("/<int:quest_id>/arc-card/add", methods=["GET", "POST"])
@login_check('authenticated', True, 'auth.login')
def add_arc_card(quest_id):
    #
    # POST
    #
    if request.method == "POST":
        arc_card_sql.create_arc_card(
            fk_quest_id=quest_id,
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
            tab="arc_cards"
        ))

    #
    # GET
    #
    q_quest = Quest.read(id_=quest_id)

    if not q_quest:
        flash("Quest not found", "bad")
        return redirect(url_for("quests.index"))

    return render_template(
        bp.tmpl("add-arc-card.html"),
        q_quest=q_quest,
    )


@bp.post("/<int:quest_id>/arc-card/add-json")
@login_check('authenticated', True, 'auth.login')
@permission_check('permission_level', 10, 'www.index')
def add_json_arc_cards(quest_id):
    json_data = request.form.get("json_data", "{}")
    parse_json_data = json.loads(json_data)

    arc_card_sql.create_arc_cards_from_json(
        quest_id=quest_id,
        arc_cards_raw=parse_json_data
    )

    return redirect(url_for(
        "quest.edit",
        quest_id=quest_id,
        tab="arc_cards"
    ))
