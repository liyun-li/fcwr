from sqlalchemy import (
    Column, Integer, String, ForeignKey, Float, Boolean, BigInteger,
    CheckConstraint as CC, UniqueConstraint as UC
)
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from time import time

db = SQLAlchemy()
ma = Marshmallow()


class Account(db.Model):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), nullable=False, unique=True)
    username = Column(String(32), nullable=False, unique=True)
    first = Column(String(32), nullable=False)
    last = Column(String(32), nullable=False)
    password = Column(String(72), nullable=False)

    __table_args__ = (
        CC('length(password) > 50'),
    )

    def __repr__(self):
        return 'User {}: {} {}'.format(self.username, self.last, self.first)
