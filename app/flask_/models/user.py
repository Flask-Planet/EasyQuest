import sqlalchemy as sqla
from flask_imp.auth import (
    authenticate_password
)
from sqlalchemy.orm import relationship

from app.flask_.extensions import db
from .__mixins__ import CrudMixin


class User(db.Model, CrudMixin):
    __id_field__ = 'user_id'
    __session__ = db.session

    # PriKey
    user_id = sqla.Column(sqla.Integer, primary_key=True)

    # Data
    first_name = sqla.Column(sqla.String(128), nullable=True)
    email_address = sqla.Column(sqla.String(512), nullable=False)
    password = sqla.Column(sqla.String(512), nullable=False)
    salt = sqla.Column(sqla.String(4), nullable=False)
    private_key = sqla.Column(sqla.String(256), nullable=False)
    disabled = sqla.Column(sqla.Boolean, default=False)

    # Permissions
    # 10 = admin, 1 = user
    permission_level = sqla.Column(sqla.Integer, nullable=True)

    # Tracking
    created = sqla.Column(sqla.DateTime)
    deleted = sqla.Column(sqla.Boolean, default=False)

    # Relationships
    rel_characters = relationship(
        "Character",
        primaryjoin="Character.fk_user_id==User.user_id",
        back_populates="rel_user"
    )

    @classmethod
    def login(cls, email_address, password):
        if email_address is None or password is None:
            return False
        user = cls.read(fields={'email_address': email_address}, _auto_output=False).first()
        if user:
            if authenticate_password(password, user.password, user.salt):
                return user
        return None

    @classmethod
    def exists(cls, email_address):
        return cls.read(fields={'email_address': email_address}, _auto_output=False).one_or_none() is not None

    @classmethod
    def enable(cls, user_id):
        cls.update(id_=user_id, values={'disabled': False})
        return

    @classmethod
    def disable(cls, user_id):
        cls.update(id_=user_id, values={'disabled': True})
        return
