from flask import Blueprint, request, redirect, render_template
from flask_login import current_user, login_user, logout_user
from models import UserModel, db
from exceptions import AuthenticationException

# application authorization module


# create the auth blueprint that is registered in the main module
auth = Blueprint('auth', __name__)

# login request. If user has been yet authorized, redirect him to his projects gallery. If the
# request method is POST, find user in the database by the given email and check password 
# corectness. If credentials are correct process user authorization. Otherwise, show proper message.
@auth.route('/login', methods = ['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect('/projects')
            
    if request.method == 'POST':
        email = request.form['email']
        user = UserModel.query.filter_by(email = email).first()
        if user is not None and user.check_password(request.form['password']):
            login_user(user)
            return redirect('/projects')
        else:
            try:
                raise AuthenticationException('Wrong login or password')
            finally:
                return render_template('login.html')          
                
    return render_template('login.html')


# register request. If user has been yet authorized, redirect him to his projects gallery. If the
# request method is POST, get request form parameters. Check whether the email exists in the
# database or not. If email doesn't exist, use loaded parameters to create a user account and
# redirect user to the login page. Otherwise, show proper message.
@auth.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect('/projects')
     
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        if UserModel.query.filter_by(email = email).first():
            try:
                raise AuthenticationException('Email already present')
            finally:
                return render_template('register.html')
        else:
            user = UserModel(email = email, username = username)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            return redirect('/login')  
    return render_template('register.html')             

 
# logout requst. Process user logout and redirect him to login page. 
@auth.route('/logout')
def logout():
    logout_user()
    return redirect('/login')