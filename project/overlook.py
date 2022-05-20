from flask import Blueprint, render_template,redirect
from flask_login import login_required
from models import SharedImageModel, UserImageModel, db
from tkinter import filedialog
from tkinter import *
from flask_login import current_user
import os

# application module for colouring overlook and download

# create look blueprint that is registered in the main module
look = Blueprint('look', __name__)

# projects overlook request. Send user saved colouring books to browser.
@look.route('/projects')
@login_required
def projects():
    return render_template('projects.html', images=get_user_images())	

# get user private coloring books stored in the database converted from binary into files
def get_user_images():
    images2 = []
    allimages = UserImageModel.query.all()
    for mimg in allimages:
        if mimg.user == current_user.id:
            images2.append(convert_data(mimg.img, mimg.title))
    return images2 

# save a user colouring book selected by a user into a selected directory
@look.route('/get/<filename>')
def download_user(filename):
    image = UserImageModel.query.filter_by(user=current_user.id, title=filename).first()
    save_project(image, filename)
    return render_template('projects.html', images=get_user_images())



# public projects overview request. It calls render proper tamplate with images stored in the database.
@look.route('/discover')
def discover():
    return render_template('discover.html', images=get_published_images())	

# get public coloring books stored in the database converted from binary into files
def get_published_images():
    images2 = []
    allimages = SharedImageModel.query.all()
    for mimg in allimages:
        images2.append(convert_data(mimg.img, mimg.title))
    return images2   

# save a colouring book selected by a user into a selected directory
@look.route('/download/<filename>')
def download(filename):
    image = SharedImageModel.query.filter_by(title = filename).first()
    save_project(image, filename)
    return render_template('discover.html', images=get_published_images())



# public projects overview request. It calls render proper tamplate with images stored in the database.
@look.route('/published')
def show_published():
    return render_template('published.html', images=get_published_images())

@look.route('/public/<filename>')
def download_published(filename):
    image = SharedImageModel.query.filter_by(title=filename).first()
    save_project(image, filename)
    return render_template('published.html', images=get_published_images())



# convert a given binary text from the database into a file
def convert_data(data, file_name):
    with open(file_name, 'wb') as file:
        file.write(data)
        return file.name   

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