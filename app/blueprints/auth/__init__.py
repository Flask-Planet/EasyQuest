from flask import redirect, url_for
from flask_imp import ImpBlueprint
from flask_imp.config import ImpBlueprintConfig

bp = ImpBlueprint(
    __name__,
    ImpBlueprintConfig(
        enabled=True,
        url_prefix="/auth",
        template_folder="templates",
    )
)

bp.import_resources()


@bp.get("/")
def index():
    return redirect(url_for('auth.login'))
