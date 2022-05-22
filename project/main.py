from flask import Flask, send_from_directory
from models import db, login
from flask_dropzone import Dropzone
import os

# application configuration module


# initialize application
app = Flask(__name__)
app.secret_key = 'xyz'

# initialize dropzone that enable load user image
dropzone = Dropzone()
dropzone.init_app(app)

# set application database and dropzone configurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['DROPZONE_MAX_FILES'] = 1

# initialize database and user authentication
db.init_app(app)
login.init_app(app)

# register application modules using blueprints
from auth import auth
app.register_blueprint(auth)

from overlook import look
app.register_blueprint(look)

from store import store
app.register_blueprint(store)

from create import create_img
app.register_blueprint(create_img)

# set login view
login.login_view = 'auth.login'

# application database configuration request
@app.before_first_request
def create_all():
    db.create_all() 

@app.route('/favicon.ico')  
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype = 'image/vnd.microsoft.icon')  

# run application
if __name__ == '__main__':
    app.run()   