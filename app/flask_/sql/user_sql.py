from app.flask_.extensions import db
from app.flask_.models import User
from flask_imp.auth import generate_salt, encrypt_password, generate_private_key
from sqlalchemy import update, select, insert


def add_user(first_name, email_address, password, permission_level=1):
    salt = generate_salt()
    password = encrypt_password(password, salt)
    private_key = generate_private_key(email_address)

    sql = (
        insert(User)
        .values({
            'first_name': first_name,
            'email_address': email_address,
            'password': password,
            'salt': salt,
            'private_key': private_key,
            'permission_level': permission_level,
        })
        .returning(User)
    )

    return db.session.execute(sql).scalar_one()


def login(email_address, password) -> User | None:
    if email_address is None or password is None:
        return None

    sql = (
        select(User)
        .where(User.email_address == email_address)
    )

    return db.session.execute(sql).scalar_one_or_none()


def confirm_private_key(private_key) -> User | None:
    if private_key is None:
        return None

    sql = (
        select(User)
        .where(User.private_key == private_key)
    )

    return db.session.execute(sql).scalar_one_or_none()


def reset_password(email_address, password) -> str:
    salt = generate_salt()
    password = encrypt_password(password, salt)

    sql = (
        update(User)
        .where(User.email_address == email_address)
        .values({
            'password': password,
            'salt': salt
        })
    )

    db.session.execute(sql)
    db.session.commit()
    return password


def get_using_email_address(email_address) -> User | None:
    sql = select(User).where(User.email_address == email_address)
    return db.session.execute(sql).scalar_one_or_none()


__all__ = [
    "add_user",
    "login",
    "confirm_private_key",
    "reset_password",
    "get_using_email_address"
]
