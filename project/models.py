from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager

from sqlalchemy import Table, Column, Integer, ForeignKey
 
login = LoginManager()
db = SQLAlchemy()
 
class UserModel(UserMixin, db.Model):
    __tablename__ = 'users'
 
    id = Column(db.Integer, primary_key=True)
    email = Column(db.String(80), unique=True)
    username = Column(db.String(100))
    password_hash = Column(db.String(50))
    images = db.relationship('UserImageModel')
 
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
     
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
 
 
@login.user_loader
def load_user(id):
    return UserModel.query.get(int(id))


class ImageModel(db.Model):
    __tablename__ = 'shared_images'

    id = Column(db.Integer, primary_key=True)
    title = Column(db.String(50))
    img = Column(db.String(200))    


class UserImageModel(db.Model):
    __tablename__ = 'user_images'

    id = Column(db.Integer, primary_key=True)
    title = Column(db.String(50))
    img = Column(db.String(200))
    user = Column(db.Integer, db.ForeignKey('users.id'))   