from flask import render_template, request, redirect, url_for, session
from flask_imp.auth import generate_alphanumeric_validator
from flask_imp.security import login_check

from app.web_.models.genre import Genre
from app.web_.models.quest import Quest
from app.utilities import DatetimeDeltaMC
from .. import bp


@bp.route("/add", methods=["GET", "POST"])
@login_check('authenticated', True, 'auth.login')
def add():
    # POST
    if request.method == "POST":
        title = request.form.get("title")
        summary = request.form.get("summary")
        fk_genre_id = request.form.get("fk_genre_id")

        user_id = session.get("user_id")

        new_quest = Quest.create(
            {
                "title": title,
                "summary": summary,
                "fk_genre_id": fk_genre_id,
                "fk_user_id": user_id,
                "created": DatetimeDeltaMC().datetime,
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

        return redirect(url_for("quest.edit", quest_id=new_quest.quest_id))

    # GET
    genres = Genre.read(all_rows=True, order_by="created")

    genres_json = [
        {
            "genre_id": genre.genre_id,
            "genre": genre.genre,
            "description": genre.description
        }
        for genre in genres
    ]

    return render_template(
        bp.tmpl("add.html"),
        genres=genres_json,
    )
