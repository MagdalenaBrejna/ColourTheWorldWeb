import os
from flask import Blueprint
from flask import Flask, flash, request, redirect, render_template, send_file
from flask_login import login_required
from werkzeug.utils import secure_filename
from models import db, login
from PIL import Image
import cv2

create_img = Blueprint('create_img', __name__)

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
UPLOAD_FOLDER = 'project/static/uploads/'

#create.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@create_img.route('/create')
@login_required
def create():
    return render_template('create.html')		   
	
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

@create_img.route('/created', methods=['POST'])
def show_created():
    filename = request.form.get("image")
    return render_template('created.html', filename=filename)
   

@create_img.route('/<filename>')
def display_image(filename):
    return send_file("static\\uploads\\" + filename)

      
@create_img.route('/created')
def show_created_temp():
    return render_template('created.html')