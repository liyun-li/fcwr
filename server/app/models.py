from sqlalchemy import Column, String, \
    ForeignKey as FK, CheckConstraint as CC
from flask_sqlalchemy import SQLAlchemy
import enum

db = SQLAlchemy()


class UserStatus(enum.Enum):
    NonSex = "Gender not selected"
    Waiting = "Waiting in the queue"
    Assigned = "Already assigned a number"


class User(db.Model):
    __tablename__ = 'user'

    open_id = Column(String(255), primary_key=True)
    # gender
    gender = Column(String(1))
    # preference
    preference = Column(String(1))
    # refer to `UserStatus`
    status = Column(db.Enum(UserStatus))

    __table_args__ = (
        CC('gender = "M" or gender = "F"'),
        CC('preference = "M" or preference = "F"')
    )


class Waitlist(db.Model):
    __tablename__ = 'waitlist'

    open_id = Column(String(255), FK('user.open_id'), primary_key=True)


class Matches(db.Model):
    __tablename__ = 'matches'

    group_id = Column(String(4), primary_key=True)
    user_1 = Column(String(255), FK('user.open_id'))
    user_2 = Column(String(255), FK('user.open_id'))
