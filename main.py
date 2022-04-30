import os
import urllib.request
from flask import Flask, flash, request, redirect, url_for, render_template,send_file
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.utils import secure_filename
from models import UserModel,db,login,ImageModel
from PIL import Image
import cv2


from flask_dropzone import Dropzone
dropzone = Dropzone()

#configuration
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
UPLOAD_FOLDER = 'static/uploads/'

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
 
app = Flask(__name__)
dropzone.init_app(app)

app.secret_key = 'xyz'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['DROPZONE_MAX_FILES'] = 1

 
db.init_app(app)
login.init_app(app)
login.login_view = 'login'
 
@app.before_first_request
def create_all():
    db.create_all() 

#security 
@app.route('/login', methods = ['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect('/projects')
     
    if request.method == 'POST':
        email = request.form['email']
        user = UserModel.query.filter_by(email = email).first()
        if user is not None and user.check_password(request.form['password']):
            login_user(user)
            return redirect('/projects')
     
    return render_template('login.html')
 
@app.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect('/projects')
     
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
 
        if UserModel.query.filter_by(email=email).first():
            return ('Email already Present')
             
        user = UserModel(email=email, username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return redirect('/login')
    return render_template('register.html')
 
 
@app.route('/logout')
def logout():
    logout_user()
    return redirect('/projects')

#pages
@app.route('/')
def home():
   return render_template("make.html")	

@app.route('/projects')
@login_required
def projects():
    return render_template('projects.html')	

def convert_data(data, file_name):
    with open(file_name, 'wb') as file:
        file.write(data)
        return file.name


@app.route('/discover')
def discover():
    images2 = []
    allimages = ImageModel.query.all()
    for mimg in allimages:
        images2.append(convert_data(mimg.img, "static\\img" + str(mimg.id) + ".jpg"))

    return render_template('discover.html', images=images2)
    #return render_template('discover.html')	

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

		#edgesImage = cv2.Canny(image, 0.3, 0.8, 3)
		data = Image.fromarray(laplacian)
		data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

		return render_template('make.html', filename=filename)
	else:
		flash('Allowed image types are -> png, jpg, jpeg, gif')
		return redirect(request.url)   

@app.route('/<filename>')
def display_image(filename):
    return send_file("static\\uploads\\" + filename)

      
@app.route('/created', methods=['POST'])
def show_created():
    filename = request.form.get("image")
    return render_template('created.html', filename=filename)
   

@app.route('/created')
def show_created_temp():
    return render_template('created.html')

def convertToBinaryData(filename):
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData    

@app.route('/share', methods=['POST'])
def share_project(): 
    filename = request.form.get("image")
    #photo = cv2.imread(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    empPhoto = convertToBinaryData("static\\uploads\\" + filename)

    if ImageModel.query.filter_by(title=filename[1:]).first():
            return ('Project already Present')

    image = ImageModel(title=filename[1:], img=empPhoto)
    db.session.add(image)
    db.session.commit()
    #return redirect(request.url, filename)   
    return render_template('created.html', filename=filename[1:])

@app.route('/share')
def shared(filename):
    return render_template('created.html', filename=filename)
    

if __name__ == '__main__':
    app.run()   


