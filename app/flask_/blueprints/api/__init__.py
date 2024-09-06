from flask_imp import ImpBlueprint
from flask_imp.config import ImpBlueprintConfig

bp = ImpBlueprint(__name__, ImpBlueprintConfig(
    enabled=True,
    url_prefix="/api",
))

bp.import_nested_blueprint("characters")
bp.import_nested_blueprint("quests")
