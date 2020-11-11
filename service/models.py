from db import db
from geoalchemy2 import Geometry
from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION
from sqlalchemy.schema import ForeignKey
from sqlalchemy.schema import PrimaryKeyConstraint


class User(db.Model):
    __tablename__ = "users"

    user_id = Column(String(100), primary_key=True, nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    last_login = Column(Date, nullable=False)

    def __init__(self, user_id, first_name, last_name, last_login):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.last_login = last_login

    def __repr__(self):
        return f"<User {self.first_name + self.last_name}>"


class UserField(db.Model):
    __tablename__ = "user_fields"

    user_id = Column(String(100), ForeignKey("users.user_id"), nullable=False)
    clu = Column(Integer, ForeignKey("clu.gid"), nullable=False)
    clu_name = Column(String(100), nullable=False)
    __table_args__ = (
        PrimaryKeyConstraint("user_id", "clu"),
        {},
    )

    def __init__(self, user_id, clu, clu_name):
        self.user_id = user_id
        self.clu = clu
        self.clu_name = clu_name

    def __repr__(self):
        return f"<UserField(user_id='{self.user_id}', clu='{self.clu}', clu_name='{self.clu_name}')>"

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class CLU(db.Model):
    __tablename__ = "clu"

    gid = Column(Integer, primary_key=True, nullable=False)
    calc_acres = Column(DOUBLE_PRECISION)
    geom = Column(Geometry("MULTIPOLYGON"))

    def __init__(self, gid, calc_acres, geom):
        self.gid = gid
        self.calc_acres = calc_acres
        self.geom = geom
