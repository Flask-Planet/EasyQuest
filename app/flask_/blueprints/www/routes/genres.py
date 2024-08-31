from flask import render_template
from flask_imp.security import login_check

from app.flask_.models.genre import Genre
from .. import bp


@bp.get("/genres")
@login_check('authenticated', True, 'auth.login')
def genres():
    q_genres = Genre.read(all_rows=True, order_by="created")

    return render_template(bp.tmpl("genres.html"), q_genres=q_genres)
