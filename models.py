from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager
from datetime import datetime
from sqlalchemy.dialects.sqlite import BLOB


 
login = LoginManager()
db = SQLAlchemy()
 
class UserModel(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True)
    firstname = db.Column(db.String(100),nullable=False)
    lastname=db.Column(db.String(200),nullable=False)
    password_hash = db.Column(db.String())
    article=db.relationship('Article',backref='user')
    def set_password(self,password):
        self.password_hash = generate_password_hash(password)  
    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    Title  = db.Column(db.String(200))
    SubTitle = db.Column(db.String(200))
    FirstName  = db.Column(db.String(200))
    LastName = db.Column(db.String(200))
    Subject  = db.Column(db.Text)
    date = db.Column(db.DateTime, default=datetime.today)
    Body = db.Column(db.Text)
    articleimg = db.Column(BLOB)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
@login.user_loader
def load_user(id):
    return UserModel.query.get(int(id))