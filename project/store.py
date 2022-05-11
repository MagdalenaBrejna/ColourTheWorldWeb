from flask import Blueprint
from models import ImageModel
from flask import flash, request, redirect, render_template
from flask_login import current_user
from models import db, ImageModel
from models import UserImageModel

store = Blueprint('store', __name__)

@store.route('/save', methods=['POST'])
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

@store.route('/share', methods=['POST'])
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

@store.route('/share')
def shared(filename):
    return render_template('created.html', filename=filename)