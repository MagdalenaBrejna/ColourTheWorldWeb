import os
from flask import Flask, flash, request, redirect, render_template, send_file
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from models import db, login, ImageModel
from models import UserImageModel
from PIL import Image
import cv2

from flask_dropzone import Dropzone

dropzone = Dropzone()

#configuration
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
UPLOAD_FOLDER = 'project/static/uploads/'

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
 
app = Flask(__name__)
dropzone.init_app(app)

app.secret_key = 'xyz'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/projekt'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
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

login.login_view = 'auth.login'

from flask import send_from_directory

#@app.route('/favicon.ico')
#def favicon():
#    return send_from_directory(os.path.join(app.root_path, 'static'),'favicon.ico', mimetype='image/vnd.microsoft.icon')

#pages


@app.route('/')
def home():
   return render_template("make.html")	

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

@app.route('/save', methods=['POST'])
def save_project():
    filename = request.form.get("image2")
    if not current_user.is_authenticated:
        flash("You must be logged in")
        return redirect('/login')

    empPhoto = convertToBinaryData("project\\static\\uploads\\" + filename[1:])
    user_projects = UserImageModel.query.all()
    for project in user_projects:
        print(str(project.title) + ' ' + str(project.id) + "\n")
        if project.title == filename[1:] and project.user == current_user.id:
            flash("Project exists")
            return render_template('created.html', filename=filename[1:])
                
    new_project = UserImageModel(title=filename[1:], img=empPhoto, user=current_user.id)
    db.session.add(new_project)
    db.session.commit()

    return redirect('/projects')                   

def convertToBinaryData(filename):
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData    

@app.route('/share', methods=['POST'])
def share_project(): 
    filename = request.form.get("image")
    empPhoto = convertToBinaryData("project\\static\\uploads\\" + filename)

    if ImageModel.query.filter_by(title=filename[1:]).first():
        flash('Project already Present')
        return render_template('created.html', filename=filename[1:])

    image = ImageModel(title=filename[1:], img=empPhoto)
    db.session.add(image)
    db.session.commit()
     
    return render_template('created.html', filename=filename[1:])

@app.route('/share')
def shared(filename):
    return render_template('created.html', filename=filename)
    


if __name__ == '__main__':
    app.run()   


