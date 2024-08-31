from app.globals import APIResponse
from app.models import User
from .. import bp


@bp.get("/auth/ws/<string:private_key>")
def auth_ws(private_key):
    user = User.read(field=("private_key", private_key))

    if not user:
        print("User not found")
        return APIResponse.fail("Unauthorized")

    if user.private_key != private_key:
        print("Private key mismatch")
        return APIResponse.fail("Unauthorized")

    return APIResponse.success("Authorized")
