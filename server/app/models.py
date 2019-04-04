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
    '''User Information'''

    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    open_id = Column(String(255))
    # gender
    gender = Column(String(1))
    # preference
    preference = Column(String(1))
    # refer to `UserStatus`
    status = Column(db.Enum(UserStatus))

    # how many people waiting in front of you??
    queue = Column(Integer)

    # do you have a match?
    match = Column(String(255), FK('user.open_id'))

    # wechat group id
    group_id = Column(Integer, FK('group.group_id'))

    __table_args__ = (
        CC('gender = "M" or gender = "F"'),
        CC('preference = "M" or preference = "F"'),
        UC('open_id'),
        UC('match')
    )


class Group(db.Model):
    '''WeChat group ID'''

    __tablename__ = 'group'

    group_id = Column(Integer, primary_key=True)

    __table_args__ = (CC('group_id > 999 and group_id < 10000'),)


class Matched(db.Model):
    '''For preventing the same matches multiple times'''

    __tablename__ = 'matched'

    user_1 = Column(String(255), FK('user.open_id'), primary_key=True)
    user_2 = Column(String(255), FK('user.open_id'), primary_key=True)
