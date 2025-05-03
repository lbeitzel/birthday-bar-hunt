from . import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    name = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))
    isAdmin = db.Column(db.Boolean)
    questionNum = db.Column(db.Integer)
    hintNum = db.Column(db.Integer)
    

class Question(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    hint1 = db.Column(db.String(200))
    hint2 = db.Column(db.String(200))
    hint3 = db.Column(db.String(200))
    answer = db.Column(db.String(100))


class Option(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    option1 = db.Column(db.String(100))
    option2 = db.Column(db.String(100))
    option3 = db.Column(db.String(100))
    option4 = db.Column(db.String(100))
    option5 = db.Column(db.String(100))
    option6 = db.Column(db.String(100))
    option7 = db.Column(db.String(100))
    option8 = db.Column(db.String(100))
    option9 = db.Column(db.String(100))
    option10 = db.Column(db.String(100))
    option11 = db.Column(db.String(100))
    option12 = db.Column(db.String(100))
