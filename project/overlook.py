from flask import Blueprint, render_template
from flask_login import login_required
from models import ImageModel
from tkinter import filedialog
from tkinter import *
import os

# application module for colouring overlook

# create look blueprint that is registered in the main module
look = Blueprint('look', __name__)

# projects overlook request. todo...
@look.route('/projects')
@login_required
def projects():
    return render_template('projects.html')	

# public projects overview request. It calls render proper tamplate with images stored in the database.
@look.route('/discover')
def discover():
    return render_template('discover.html', images=get_published_images())	

# get public coloring books stored in the database converted from binary into files
def get_published_images():
    images2 = []
    allimages = ImageModel.query.all()
    for mimg in allimages:
        images2.append(convert_data(mimg.img, mimg.title))
    return images2   

# convert a given binary text from the database into a file
def convert_data(data, file_name):
    with open(file_name, 'wb') as file:
        file.write(data)
        return file.name

# save a colouring book selected by a user into a selected directory
@look.route('/download/<filename>', methods=['POST'])
def download(filename):
    image = ImageModel.query.filter_by(title = filename).first()
    with open(os.path.join(getUserDirectoryPath(), filename), 'wb') as file:
        file.write(image.img)
    return render_template('discover.html', images=get_published_images())

# open a directory dialog to let user choose a place to save a colouring book
def getUserDirectoryPath():
    win = Tk()
    win.withdraw()
    win.attributes('-topmost', True)
    return filedialog.askdirectory()