import os
from flask import Blueprint, flash, request, redirect, render_template, send_file
from flask_login import login_required
from werkzeug.utils import secure_filename
from PIL import Image
import cv2

# application module for colouring creation

# create create_img blueprint that is registered in the main module
create_img = Blueprint('create_img', __name__)

# set configurations for uploading files - restrict available file extensions and destination folder
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
UPLOAD_FOLDER = 'project/static/uploads/'

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# get a form to create a colouring
@create_img.route('/')
def home():
   return render_template("make.html")	

# get a form to create a colouring by an authenticated user
@create_img.route('/create')
@login_required
def create():
    return render_template('create.html')		   

# upload request. A file selected in dropzone is stored in the request's files. If a user file wasn't successfuly uploaded,
# user gets a proper messase using flash. When a user file is in files, it is checked in respect of allowed extensions. If
# file is allowed, application saves it and convert into a colouring book. New image is sending back to the browser.	
@create_img.route('/', methods=['POST'])
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
		file.save(os.path.join(UPLOAD_FOLDER, filename))

		#create a colouring
		image2 = cv2.imread(os.path.join(UPLOAD_FOLDER, filename))
		image = cv2.cvtColor(image2 , cv2.COLOR_RGB2GRAY)
		dst = cv2.GaussianBlur(image, (3, 3), cv2.BORDER_DEFAULT, 0.5)
		laplacian = cv2.Laplacian(dst, -10, 3)
		laplacian = 255 - laplacian

		data = Image.fromarray(laplacian)
		data.save(os.path.join(UPLOAD_FOLDER, filename))

		return render_template('make.html', filename=filename)
	else:
		flash('Allowed image types are -> png, jpg, jpeg, gif')
		return redirect(request.url)   

# show a colouring book request. Application get an image from html form
# and send it back to the browser to show conversion result.
@create_img.route('/created', methods=['POST'])
def show_created():
    filename = request.form.get("image")
    return render_template('created.html', filename=filename)
   
# send stored image with the given filename into browser
@create_img.route('/<filename>')
def display_image(filename):
    return send_file("static\\uploads\\" + filename)

# show tamplate that display created colouring book      
@create_img.route('/created')
def show_created_temp():
    return render_template('created.html')