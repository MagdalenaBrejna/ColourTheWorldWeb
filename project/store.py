from flask import Blueprint, flash, request, redirect, render_template
from models import db, SharedImageModel, UserImageModel
from flask_login import current_user
from exceptions import AuthenticationException

# application module for processing storing a colouring book


# create the store blueprint that is registered in the main module
store = Blueprint('store', __name__)


# save a colouring book. If user is not authorized redirect him to login page. Otherwise, 
# convert a colouring book into binary text to store it in the databas in the more efficient way. Check if the
# project has been saved before. If yes show a proper message. Otherwise, save it in the database.
@store.route('/save', methods=['POST'])
def save_project():
    # if user is not authorized redirect him to the login page
    '''
    if not current_user.is_authenticated:
        try:
            raise AuthenticationException('You must be logged in')
        finally:
            return render_template('login.html')

    filename = request.form.get("image_to_save")
    if save_image(filename):
        return redirect('/projects')
    else:                          
        return render_template('created.html', filename = filename[1:])         
    '''
    if not current_user.is_authenticated:
        flash("You must be logged in")
        return redirect('/login')

    filename = request.form.get("image_to_save")
    if save_image(filename):
        return redirect('/projects')
    else:                          
        return render_template('created.html', filename = filename[1:]) 
       


# save a colouring on an authorized user's profile. If user is not authorized redirect him to login page. Otherwise, 
# convert a colouring book into binary text to store it in the databas in the more efficient way. Check if the
# project has been saved before. If yes show a proper message. Otherwise, save it in the database.
@store.route('/saveuser', methods=['POST'])
def save_project_for_login():
    filename = request.form.get("image_to_save")
    if save_image(filename):
        return redirect('/projects')
    else:                          
        return render_template('newCreated.html', filename = filename[1:])


# process image saving
def save_image(filename):
    # prepare a colouring book to save it in the database. Convert it into binary data.
    empPhoto = convertToBinaryData("project\\static\\uploads\\" + filename[1:])
    
    # make sure that this user project doesn't exist.
    if UserImageModel.query.filter_by(title = filename[1:], user = current_user.id).first():
        flash("Project exists")
        return False

    # save a project in the database            
    saveUserImage(empPhoto, filename)
    return True    


# create a new instance of UserImageModel to save a colouring book in the database as a user's private colouring book 
def saveUserImage(empPhoto, filename):
    new_project = UserImageModel(title = filename[1:], img = empPhoto, user = current_user.id)
    db.session.add(new_project)
    db.session.commit()



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
    share('created.html', filename)
    return render_template('created.html', filename = filename[1:])


# share a created colouring boook with users' community by logged in user. Convert a colouring book 
# into binary text to store it in the databas in the more efficient way. Check if the project has 
# been saved before. If yes show a proper message. Otherwise, save it in the database.
@store.route('/shareuser', methods=['POST'])
def share_project_for_login(): 
    filename = request.form.get("image_to_share")
    share('newCreated.html', filename)
    return render_template('newCreated.html', filename = filename[1:])


# process image sharing
def share(path, filename):
    # prepare a colouring book to save in the database. Convert it into binary data.
    empPhoto = convertToBinaryData("project\\static\\uploads\\" + filename)

    # make sure that this project doesn't exist. 
    if SharedImageModel.query.filter_by(title = filename[1:]).first():
        flash('Project already published')
        return render_template(path, filename = filename[1:])

    # save project in the database
    saveSharedImage(empPhoto, filename)
     

# create a new instance of SharedImageModel to save a colouring book in the database as a public project that can be downloaded by other users.
def saveSharedImage(empPhoto, filename):    
    image = SharedImageModel(title = filename[1:], img = empPhoto)
    db.session.add(image)
    db.session.commit()


# request for return to created page after project sharing
@store.route('/share')
def shared(filename):
    return render_template('created.html', filename=filename)