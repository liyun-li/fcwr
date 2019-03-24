from sqlalchemy import Column, String, CheckConstraint as CC
from flask_sqlalchemy import SQLAlchemy
import enum

db = SQLAlchemy()

class UserStatus(enum.Enum):
    NonSex = "sex not selected"
    Waiting = "waiting in the queue"
    Assigned = "already assigned a number"

class User(db.Model):
    __tablename__ = 'user'

    open_id = Column(String(255), primary_key=True)
    # own gender
    gender = Column(String(1))
    # liked gender
    like_gender = Column(String(1))

    status = Column(db.Enum(UserStatus))

    # number
    number = Column(db.Integer)

    __table_args__ = (
        CC('gender = "M" or gender = "F"'),
    )
