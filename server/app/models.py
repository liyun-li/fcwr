from sqlalchemy import Column, String, CheckConstraint as CC
from flask_sqlalchemy import SQLAlchemy
import enum

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'

    open_id = Column(String(255), primary_key=True)
    # own gender
    gender = Column(String(1))
    # liked gender
    like_gender = Column(String(1))
    # number
    number = Column(db.Integer)

    __table_args__ = (
        CC('gender = "M" or gender = "F"'),
    )
