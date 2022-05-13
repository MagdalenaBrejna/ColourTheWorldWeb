from flask import Flask, render_template, send_from_directory
from models import db, login
from flask_dropzone import Dropzone
import os

#configuration

app = Flask(__name__)
app.secret_key = 'xyz'

dropzone = Dropzone()
dropzone.init_app(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/projekt'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['DROPZONE_MAX_FILES'] = 1

db.init_app(app)
login.init_app(app)

from auth import auth
app.register_blueprint(auth)

from overlook import look
app.register_blueprint(look)

from store import store
app.register_blueprint(store)

from create import create_img
app.register_blueprint(create_img)

login.login_view = 'auth.login'

@app.before_first_request
def create_all():
    db.create_all() 

@app.route('/favicon.ico')  
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')  

if __name__ == '__main__':
    app.run()   