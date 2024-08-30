import sqlalchemy as sqla

from app.extensions import db


class System(db.Model):
    # PriKey
    system_id = sqla.Column(sqla.Integer, primary_key=True)
    created_at = sqla.Column(sqla.DateTime, server_default=sqla.func.now())

    @classmethod
    def get_system(cls):
        query = sqla.select(cls)
        return db.session.execute(query).scalar()
