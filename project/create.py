import os
from flask import Blueprint, flash, request, redirect, render_template, send_file
from flask_login import login_required
from werkzeug.utils import secure_filename
from PIL import Image
import cv2
from exceptions import ImageException

# application module for colouring book creation


# create the create_img blueprint that is registered in the main module
create_img = Blueprint('create_img', __name__)

# declare constant path for the folder that store uploaded colouring books
UPLOAD_FOLDER = 'project/static/uploads/'


# show the form to create a colouring book
@create_img.route('/')
def home():
   return render_template("make.html")	

# show the form to create a colouring book by an authenticated user
@create_img.route('/create')
@login_required
def create():
    return render_template('create.html')	


# upload request. A file selected in the dropzone is stored in the request's files. If a user file wasn't successfuly uploaded,
# user gets a proper messase using flash. File extension correctness is validated by the dropzone, so there is no need to check
# this later. If file is allowed, application saves it and convert into a colouring book. The new image is being sent back to the browser.
@create_img.route('/', methods=['POST'])
def upload_image():
	if 'file' not in request.files:
		try:
			raise ImageException("No file part", "make.html")
		finally:
			redirect(request.url)	

	file = request.files['file']
	if file.filename == '':
		try:
			raise ImageException("No image selected for uploading", "make.html")
		finally:
			redirect(request.url)	
	else:
		# save an input image
		filename = secure_filename(file.filename)
		file.save(os.path.join(UPLOAD_FOLDER, filename))

		try:
			image_matrix = cv2.imread(os.path.join(UPLOAD_FOLDER, filename))
		except Exception:
			raise ImageException("Invalid image", "make.html")	
		else:	
			# create a colouring book
			image = cv2.cvtColor(image_matrix , cv2.COLOR_RGB2GRAY)
			dst = cv2.GaussianBlur(image, (3, 3), cv2.BORDER_DEFAULT, 0.5)
			laplacian = cv2.Laplacian(dst, -10, 3)
			laplacian = 255 - laplacian

			# save a ready image
			data = Image.fromarray(laplacian)
			data.save(os.path.join(UPLOAD_FOLDER, filename))
		finally:
			return render_template('make.html', filename = filename)


# show tamplate that display a created colouring book      
@create_img.route('/created')
def show_created_temp():
    return render_template('created.html')		

# show a colouring book request. Application gets an image from html
# form and sends it back to the browser to show a conversion result.
@create_img.route('/created', methods=['POST'])
def show_created():
	filename = request.form.get("image")
	if filename == '':
		try:
			raise ImageException("Image cannot be empty", "make.html")
		finally:	
			return render_template('make.html')
	return render_template('created.html', filename = filename)


# show tamplate that display a created colouring book for logged in user    
@create_img.route('/createduser')
def show_created_temp_for_login():
    return render_template('newCreated.html')	

# show a colouring book request. Application gets an image from html
# form and sends it back to the browser to show a conversion result
# for logged in user.
@create_img.route('/createduser', methods=['POST'])
def show_created_for_login():
	filename = request.form.get("image")
	if filename == '':
		try:
			raise ImageException("Image cannot be empty", "create.html")
		finally:	
			return render_template('create.html')
	return render_template('newCreated.html', filename = filename)	

   
# send stored image of the given filename into browser
@create_img.route('/<filename>')
def display_image(filename):
    return send_file("static\\uploads\\" + filename)