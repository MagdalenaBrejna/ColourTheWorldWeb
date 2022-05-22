from flask import Blueprint, flash, request, redirect, render_template
from models import db, SharedImageModel, UserImageModel
from flask_login import current_user

# application module for processing storing a colouring book


# create the store blueprint that is registered in the main module
store = Blueprint('store', __name__)


# save a colouring on a authorized user's profile. If user is not authorized redirect him to login page. Otherwise, 
# convert a colouring book into binary text to store it in the databas in the more efficient way. Check if the
# project has been saved before. If yes show a proper message. Otherwise, save it in the database.
@store.route('/save', methods=['POST'])
def save_project():
    filename = request.form.get("image_to_save")

    # if user is not authorized redirect him to the login page
    if not current_user.is_authenticated:
        flash("You must be logged in")
        return redirect('/login')

    # prepare a colouring book to save it in the database. Convert it into binary data.
    empPhoto = convertToBinaryData("project\\static\\uploads\\" + filename[1:])
    
    # make sure that this user project doesn't exist.
    user_project = UserImageModel.query.filter_by(title = filename[1:], user = current_user.id).first()
    if user_project is not None:
        flash("Project exists")
        return render_template('created.html', filename = filename[1:])

    # create a new instance of UserImageModel to save a colouring book in the database as a user's private colouring book             
    new_project = UserImageModel(title = filename[1:], img = empPhoto, user = current_user.id)
    db.session.add(new_project)
    db.session.commit()

    return redirect('/projects')                   


# convert an image file into binary that can be better stored in the table in database
def convertToBinaryData(filename):
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData    


# share a created colouring boook with users' community. Convert a colouring book into binary text 
# to store it in the databas in the more efficient way. Check if the project has been saved before
# If yes show a proper message. Otherwise, save it in the database.
@store.route('/share', methods=['POST'])
def share_project(): 
    filename = request.form.get("image_to_share")

    # prepare a colouring book to save in the database. Convert it into binary data.
    empPhoto = convertToBinaryData("project\\static\\uploads\\" + filename)

    # make sure that this user project doesn't exist. 
    if SharedImageModel.query.filter_by(title = filename[1:]).first():
        flash('Project already published')
        return render_template('created.html', filename = filename[1:])

    # create a new instance of SharedImageModel to save a colouring book in the database as a public project that can be downloaded by other users.
    image = SharedImageModel(title = filename[1:], img = empPhoto)
    db.session.add(image)
    db.session.commit()
     
    return render_template('created.html', filename = filename[1:])


# request for return to created page after project sharing
@store.route('/share')
def shared(filename):
    return render_template('created.html', filename=filename)