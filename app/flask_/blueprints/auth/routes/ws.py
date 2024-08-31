from app.flask_.globals import APIResponse
from app.flask_.sql import user_sql
from .. import bp


@bp.get("/auth/ws/<int:user_id>/<string:private_key>")
def auth_ws(user_id, private_key):
    user = user_sql.confirm_private_key(user_id, private_key)

    if not user:
        print("User not found")
        return APIResponse.fail("Unauthorized")

    return APIResponse.success("Authorized")
