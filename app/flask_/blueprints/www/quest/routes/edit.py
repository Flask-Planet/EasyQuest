from flask import render_template, redirect, url_for, flash, request
from flask_imp.security import login_check, permission_check

from app.flask_.models.genre import Genre
from app.flask_.models.quest import Quest
from .. import bp


@bp.route("/quest/<quest_id>/edit", methods=["GET", "POST"])
@login_check('authenticated', True, 'auth.login')
@permission_check('permission_level', 10, 'www.index')
def edit(quest_id):
    #
    # POST
    #
    if request.method == "POST":
        title = request.form.get("title")
        summary = request.form.get("summary")
        fk_genre_id = request.form.get("fk_genre_id")

        Quest.update(
            id_=quest_id,
            values={
                "title": title,
                "summary": summary,
                "fk_genre_id": fk_genre_id
            }
        )

        flash("Quest Updated", "good")
        return redirect(url_for("www.quest.edit", quest_id=quest_id))

    #
    # GET
    #
    q_quest = Quest.read(id_=quest_id)

    if not q_quest:
        flash("Quest not found", "bad")
        return redirect(url_for("www.quests"))

    q_genres = Genre.read(all_rows=True, order_by="created")

    return render_template(
        bp.tmpl("edit.html"),
        q_quest=q_quest,
        q_genres=q_genres,
    )
