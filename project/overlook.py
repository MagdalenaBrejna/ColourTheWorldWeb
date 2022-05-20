from flask import Blueprint
from flask import redirect, flash, render_template
from flask_login import login_required
from models import ImageModel
from tkinter import filedialog
from tkinter import *
import os

look = Blueprint('look', __name__)

@look.route('/projects')
@login_required
def projects():
    return render_template('projects.html')	

@look.route('/discover')
def discover():
    return render_template('discover.html', images=get_published_images())	

def get_published_images():
    images2 = []
    allimages = ImageModel.query.all()
    for mimg in allimages:
        images2.append(convert_data(mimg.img, mimg.title))
    return images2   

def convert_data(data, file_name):
    with open(file_name, 'wb') as file:
        file.write(data)
        return file.name

@look.route('/download/<filename>', methods=['POST'])
def download(filename):
    image = ImageModel.query.filter_by(title = filename).first()
    with open(os.path.join(getUserDirectoryPath(), filename), 'wb') as file:
        file.write(image.img)
    return render_template('discover.html', images=get_published_images())

def getUserDirectoryPath():
    win = Tk()
    win.withdraw()
    win.attributes('-topmost', True)
    folder_selected = filedialog.askdirectory()
    return folder_selected