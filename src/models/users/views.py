from flask import Blueprint, request, url_for, render_template, session, flash
from werkzeug.utils import redirect
import src.models.users.errors as UserErrors
#from src.models.users.user import User
from src.common.database import Database
from src.models.users.user import User
import hashlib

user_blueprint = Blueprint('users', __name__)

@user_blueprint.route('/')
def home():
    return 'Hello'

@user_blueprint.route('/login', methods=['POST', 'GET'])
def login_user():
    if request.method == 'POST':
        # check login is valid
        email = request.form['email']
        password = request.form['hashed']
        password = hashlib.sha512(password.encode()).hexdigest()

        try:
            if User.is_login_valid(email, password):
                session['email'] = email
                user = Database.find_one(collection='users', query={'email':email})
                user_id = user['_id']
                return redirect(url_for('.welcome_page', user_id=user_id))
        except UserErrors.UserError as e:
            return e.message

    return render_template('login.html')




@user_blueprint.route('/register', methods=['POST', 'GET'])
def register_user():
    if request.method == 'POST':
        # check login is valid
        email = request.form['email']
        password = request.form['hashed']
        password = hashlib.sha512(password.encode()).hexdigest()

        try:
            if User.register_user(email, password):
                session['email'] = email
                user = User.get_by_email(email)
                user_id = user._id
                return redirect(url_for('.welcome_page', user_id=user_id))
        except UserErrors.UserError as e:
            return e.message

    return render_template('register.html')


@user_blueprint.route('/welcome/')
@user_blueprint.route('/welcome/<string:user_id>')
def welcome_page(user_id=None):
    if session['email'] is None:
        flash('You are not logged in')
        return redirect('/')
    if user_id is None:
        try:
            user = User.get_by_email(session['email'])
            user_id = user._id
        except:
            flash('You are not logged in')
            return redirect('/')
    else:
        user = User.get_by_id(user_id)
    return render_template('what_are_you_working_on.html', email=session['email'], user_id=user_id, split_list=user.split_list)





@user_blueprint.route('/logout')
def logout_user():
    session['email'] = None
    flash('You logged out')
    return redirect('/')


