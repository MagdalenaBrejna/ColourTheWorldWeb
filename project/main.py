import os
from flask import Flask, flash, request, redirect, render_template, send_file
from flask_login import login_required
from werkzeug.utils import secure_filename
from models import db, login
from PIL import Image
import cv2

from flask_dropzone import Dropzone

dropzone = Dropzone()

#configuration
#ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
#UPLOAD_FOLDER = 'project/static/uploads/'
 
app = Flask(__name__)
dropzone.init_app(app)

app.secret_key = 'xyz'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/projekt'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['DROPZONE_MAX_FILES'] = 1

 
db.init_app(app)
login.init_app(app)

 
@app.before_first_request
def create_all():
    db.create_all() 

from auth import auth
app.register_blueprint(auth)

from overlook import look
app.register_blueprint(look)

from store import store
app.register_blueprint(store)

from create import create_img
app.register_blueprint(create_img)

login.login_view = 'auth.login'

@app.route('/')
def home():
   return render_template("make.html")	
'''
@app.route('/create')
@login_required
def create():
    return render_template('create.html')		   
	
@app.route('/', methods=['POST'])
def upload_image():
	if 'file' not in request.files:
		flash('No file part')
		return redirect(request.url)
	file = request.files['file']
	if file.filename == '':
		flash('No image selected for uploading')
		return redirect(request.url)
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

		image2 = cv2.imread(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		image = cv2.cvtColor(image2 , cv2.COLOR_RGB2GRAY)
		dst = cv2.GaussianBlur(image, (3, 3), cv2.BORDER_DEFAULT, 0.5)
		laplacian = cv2.Laplacian(dst, -10, 3)
		laplacian = 255 - laplacian

		data = Image.fromarray(laplacian)
		data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

		return render_template('make.html', filename=filename)
	else:
		flash('Allowed image types are -> png, jpg, jpeg, gif')
		return redirect(request.url)   

@app.route('/created', methods=['POST'])
def show_created():
    filename = request.form.get("image")
    return render_template('created.html', filename=filename)
   

@app.route('/<filename>')
def display_image(filename):
    return send_file("static\\uploads\\" + filename)

      
@app.route('/created')
def show_created_temp():
    return render_template('created.html')
'''

if __name__ == '__main__':
    app.run()   