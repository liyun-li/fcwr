from sqlalchemy import Integer, Column, String, ForeignKey as FK, \
    CheckConstraint as CC, UniqueConstraint as UC
from flask_sqlalchemy import SQLAlchemy
import enum

db = SQLAlchemy()


class UserStatus(enum.Enum):
    Selecting = "Need to select gender and preference"
    Waiting = "Waiting in queue"
    Assigned = "Assigned a number"


class User(db.Model):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    open_id = Column(String(255))
    # gender
    gender = Column(String(1))
    # preference
    preference = Column(String(1))
    # refer to `UserStatus`
    status = Column(db.Enum(UserStatus))

    __table_args__ = (
        CC('gender = "M" or gender = "F"'),
        CC('preference = "M" or preference = "F"'),
        UC('open_id')
    )


class Matches(db.Model):
    __tablename__ = 'matches'

    group_id = Column(String(4), primary_key=True)
    user_1 = Column(String(255), FK('user.open_id'))
    user_2 = Column(String(255), FK('user.open_id'))
