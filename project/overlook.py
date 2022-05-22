from flask import Blueprint, render_template,request
from flask_login import login_required
from models import SharedImageModel, UserImageModel
from tkinter import filedialog
from tkinter import *
from flask_login import current_user
import os

# application module for colouring books overlook and download


# create the look blueprint that is registered in the main module
look = Blueprint('look', __name__)

# user projects overlook request. It sends user's saved in the database colouring books to the browser
@look.route('/projects')
@login_required
def projects():
    return render_template('projects.html', images = get_user_images())	

# get user private coloring books stored in the database and conver them from binaries into files
def get_user_images():
    images = []
    binary_images = UserImageModel.query.filter_by(user = current_user.id).all()
    for image in binary_images:
        images.append(convert_data(image.img, image.title))
    return images 

# save a user colouring book selected by a user into a selected directory in computer files (download)
@look.route('/get/<filename>')
def download_user(filename):
    image = UserImageModel.query.filter_by(user = current_user.id, title = filename).first()
    save_project(image, filename)
    return render_template('projects.html', images = get_user_images())



# public projects overview request. It sends community saved in the database colouring books to the browser (discover.html)
@look.route('/discover')
def discover():
    return render_template('discover.html', images = get_published_images())	

# get public coloring books stored in the database and convert them from binaries into files
def get_published_images():
    images = []
    binary_images = SharedImageModel.query.all()
    for image in binary_images:
        images.append(convert_data(image.img, image.title))
    return images   

# save a colouring book selected by a user into a selected directory in computer files (download)
@look.route('/download/<filename>')
def download(filename):
    image = SharedImageModel.query.filter_by(title = filename).first()
    save_project(image, filename)
    return render_template('discover.html', images = get_published_images())



# public projects overview request. It sends community saved in the database colouring books to the browser ("published.html")
@look.route('/published')
def show_published():
    return render_template('published.html', images = get_published_images())

# save a colouring book selected by a user into a selected directory in computer files (download)
@look.route('/public/<filename>')
def download_published(filename):
    image = SharedImageModel.query.filter_by(title = filename).first()
    save_project(image, filename)
    return render_template('published.html', images = get_published_images())



# save an unsaved and unpublished colouring book into a selected directory in computer files (download)
@look.route('/saveproject', methods=['POST'])
def download_project():
    image = request.form.get("image_to_download")
    with open("project\\static\\uploads\\" + image[1:], 'rb') as file:
        img = file.read()
    with open(os.path.join(getUserDirectoryPath(), image[1:]), 'wb') as file:
        file.write(img)
    return render_template('created.html', filename = image[1:])



# convert a given binary text from the database into a file
def convert_data(data, file_name):
    with open("project\\static\\uploads\\" + file_name, 'wb') as file:
        file.write(data)
        return file.name[8:]   

# save a selected colouring book in a selected directory
def save_project(image, filename):
    with open(os.path.join(getUserDirectoryPath(), filename), 'wb') as file:
        file.write(image.img)

# open a directory dialog to let user choose a place to save a colouring book
def getUserDirectoryPath():
    win = Tk()
    win.withdraw()
    win.attributes('-topmost', True)
    directory = filedialog.askdirectory()
    win.destroy()
    return directory