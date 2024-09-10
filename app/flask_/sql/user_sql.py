from flask_imp.auth import generate_salt, encrypt_password, generate_private_key
from sqlalchemy import update, select, insert, delete

from app.flask_.extensions import db
from app.flask_.models import User
from app.flask_.sql import quest_sql, character_sql


def get_by_id(user_id) -> User | None:
    sql = (
        select(User)
        .where(User.user_id == user_id)
    )
    return db.session.execute(sql).scalar_one_or_none()


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

    result = db.session.execute(sql).scalar_one()
    db.session.commit()

    return result


def update_user(user_id, first_name, email_address):
    sql = (
        update(User)
        .where(User.user_id == user_id)
        .values({
            'first_name': first_name,
            'email_address': email_address,
        })
    )

    db.session.execute(sql)
    db.session.commit()


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


def delete_by_id(user_id):
    sql = (
        delete(User)
        .where(User.user_id == user_id)
    )

    db.session.execute(sql)
    db.session.commit()

__all__ = [
    "add_user",
    "login",
    "confirm_private_key",
    "reset_password",
    "get_using_email_address"
]
