from sqlalchemy import Column, Integer, String, Date, Float
from sqlalchemy.schema import ForeignKey, PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION
from geoalchemy2 import Geometry

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    userid = Column(String(100), primary_key=True, nullable=False)
    firstname = Column(String(100), nullable=False)
    lastname = Column(String(100), nullable=False)
    lastlogin = Column(Date, nullable=False)

    def __init__(self, userid, firstname, lastname, lastlogin):
        self.userid = userid
        self.firstname = firstname
        self.lastname = lastname
        self.lastlogin = lastlogin

    def __repr__(self):
        return '<User %r>' % (self.firstname + self.lastname)

class UserField(Base):
    __tablename__ = "userfields"

    userid = Column(String(100), ForeignKey("users.userid"), nullable=False)
    clu = Column(Integer, ForeignKey("clu.gid"), nullable=False)
    cluname = Column(String(100), nullable=False)
    lat = Column(Float, nullable=False)
    lon = Column(Float, nullable=False)
    __table_args__ = (
        PrimaryKeyConstraint('userid', 'clu'),
        {},
    )

    def __init__(self, userid, clu, cluname, lat, lon):
        self.userid = userid
        self.clu = clu
        self.cluname = cluname
        self.lat = lat
        self.lon = lon

    def __repr__(self):
        return "<UserField(userid='%s', clu='%s', cluname='%s', lat='%s', lon='%s')>" % (
            self.userid, self.clu, self.cluname, self.lat, self.lon)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class CLU(Base):
    __tablename__ = "clu"

    gid = Column(Integer, primary_key=True, nullable=False)
    calcacres = Column(DOUBLE_PRECISION)
    geom = Column(Geometry('POLYGON'))

    def __init__(self, gid, calcacres, geom):
        self.gid = gid
        self.calcacres = calcacres
        self.geom = geom