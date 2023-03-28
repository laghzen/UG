from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///history.db'
db = SQLAlchemy(app)


class Exist_User(db.Model):
    __tablename__ = 'exist_user'
    login = db.Column(db.String(255), nullable=False, primary_key=True)
    password = db.Column(db.String(32), nullable=False)

    def __repr__(self):
        return '<Exist_User %r>' % self.id_customer


class History(db.Model):
    __tablename__ = 'history'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.Integer)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    value = db.Column(db.Integer)

    def __repr__(self):
        return '<History %r>' % self.id_customer


with app.app_context():
    db.create_all()