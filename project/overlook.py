from flask import Blueprint
from flask import render_template
from flask_login import login_required
from models import ImageModel

look = Blueprint('look', __name__)

@look.route('/projects')
@login_required
def projects():
    return render_template('projects.html')	

@look.route('/discover')
def discover():
    images2 = []
    allimages = ImageModel.query.all()
    for mimg in allimages:
        images2.append(convert_data(mimg.img, mimg.title))
    return render_template('discover.html', images=images2)	

def convert_data(data, file_name):
    with open(file_name, 'wb') as file:
        file.write(data)
        return file.name
        