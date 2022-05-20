from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column

# initialize LoginManager and SQLAlchemy to enable database and security 
login = LoginManager()
db = SQLAlchemy()

# class that builds a users' table schema in the database using SQLAlchemy and Sqllite
class UserModel(UserMixin, db.Model):
    __tablename__ = 'users'
 
    id = Column(db.Integer, primary_key=True)
    email = Column(db.String(80), unique=True)
    username = Column(db.String(100))
    password_hash = Column(db.String(50))
    images = db.relationship('UserImageModel')
 
    # generate and set a hash password
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # check if a given hash passwort is correct 
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
 
# load user with a given id number 
@login.user_loader
def load_user(id):
    return UserModel.query.get(int(id))

# class that builds an image table schema for images shered by users to other
class ImageModel(db.Model):
    __tablename__ = 'shared_images'

    id = Column(db.Integer, primary_key=True)
    title = Column(db.String(50))
    img = Column(db.String(200))    

# class that builds an image table schema for users' personal colouring books
class UserImageModel(db.Model):
    __tablename__ = 'user_images'

    id = Column(db.Integer, primary_key=True)
    title = Column(db.String(50))
    img = Column(db.String(200))
    user = Column(db.Integer, db.ForeignKey('users.id'))   