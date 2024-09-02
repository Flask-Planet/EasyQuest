from flask import render_template, request, redirect, url_for
from flask_imp.auth import generate_alphanumeric_validator
from flask_imp.security import login_check, permission_check

from app.flask_.models import dater
from app.flask_.models.genre import Genre
from app.flask_.models.quest import Quest
from .. import bp


@bp.route("/quest/add", methods=["GET", "POST"])
@login_check('authenticated', True, 'auth.login')
@permission_check('permission_level', 10, 'www.index')
def add():
    # POST
    if request.method == "POST":
        title = request.form.get("title")
        summary = request.form.get("summary")
        fk_genre_id = request.form.get("fk_genre_id")

        new_quest = Quest.create(
            {
                "title": title,
                "summary": summary,
                "fk_genre_id": fk_genre_id,
                "created": dater(),
            }
        )

        random_code = (
            generate_alphanumeric_validator(3)
            .replace('0', 'Z')
            .replace('O', 'Y')
        )
        quest_code = f"{random_code}{new_quest.quest_id}"

        Quest.update(
            id_=new_quest.quest_id,
            values={"quest_code": quest_code}
        )

        return redirect(url_for("www.quest.edit", quest_id=new_quest.quest_id))

    # GET
    q_genres = Genre.read(all_rows=True, order_by="created")
    return render_template(
        bp.tmpl("add.html"),
        q_genres=q_genres,
    )
