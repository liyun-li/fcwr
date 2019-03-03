from sqlalchemy import Column, String, CheckConstraint as CC
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'

    open_id = Column(String(255), primary_key=True)
    gender = Column(String(1))

    __table_args__ = (
        CC('gender = "M" or gender = "F"'),
    )
