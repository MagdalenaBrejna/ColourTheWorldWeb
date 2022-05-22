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
 
    # declare table columns
    id = Column(db.Integer, primary_key = True)
    email = Column(db.String(80), unique = True)
    username = Column(db.String(100))
    password_hash = Column(db.String(50))
    images = db.relationship('UserImageModel')
 
    # generate and set a hashed password
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # check if a given hashed passwort is correct 
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
 
# load user of a given id number 
@login.user_loader
def load_user(id):
    return UserModel.query.get(int(id))

# parent class that builds parent table for all colouring books' projects. (implemented joined table inheritance)
class ImageModel(db.Model):
    __tablename__ = 'all_images'

    # declare table columns
    id = Column(db.Integer, primary_key = True)
    title = Column(db.String(50))
    img = Column(db.String(200))
    type = Column(db.String(50))     

    __mapper_args__ = {
        'polymorphic_identity':'all_images',
        'polymorphic_on':type
    }

# child class that builds table for community colouring books. It inherits from ImageModel (joined table inheritance)
class SharedImageModel(ImageModel):
    __tablename__ = 'public_images'

    # declare a table id connected with the all_images table. It lets id be unique in all child tables together
    id = Column(db.Integer, db.ForeignKey('all_images.id'), primary_key = True)
 
    __mapper_args__ = {
        'polymorphic_identity':'shared',
    } 

# child class that builds table for users private colouring books. It inherits from ImageModel (joined table inheritance)
class UserImageModel(ImageModel):
    __tablename__ = 'private_images'

    # declare a table id connected with the all_images table. It lets id be unique in all child tables together. Set the connection with users table
    id = Column(db.Integer,  db.ForeignKey('all_images.id'), primary_key = True)
    user = Column(db.Integer, db.ForeignKey('users.id')) 

    __mapper_args__ = {
        'polymorphic_identity':'user'
    }    
