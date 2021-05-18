from __future__ import print_function
from flask import (
    Blueprint, redirect, render_template, request, session, url_for, flash
)
from utils import drives, get_os
from db_file import get_user_by_email, add_to_db, get_folder_db_data, update_password
from custum_decorators import login_required

user_bp = Blueprint('user', __name__)


@user_bp.route('/')
@login_required
def index():
    return render_template('home.html')


@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if len(email) == 0 or len(password) == 0:
            flash("email or password is empty")
            return redirect(request.url)
        user = get_user_by_email(email)
        if user is None:
            flash("user did not exist")
        elif user.banned:
            flash("You are Banned")
        elif user.password == password:
            session['email'] = email
            session['username'] = user.user_name
            session['verified'] = user.verified
            if user.verified and user.user_name == "admin":
                session['currentPath'] = drives[0][1] if get_os() == 'Linux' else drives[0][0]
            else:
                session['currentPath'] = get_folder_db_data(enable=True)[0].folder_path
            return redirect(url_for('user.index'))
        else:
            flash("incorrect username or password ")
        return redirect(request.url)
    return render_template('index.html')


# Register user
@user_bp.route('/register', methods=['GET'])
def register():
    return render_template('register.html')


@user_bp.route('/add', methods=['POST'])
def add():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        if username == "admin":
            flash("cannot create account with username admin")
            return redirect(url_for('user.register'))
        if len(username) == 0 or len(username) == 0 or len(password) == 0:
            flash("email, username or password is empty")
            return redirect(url_for('user.register'))
        if len(password) > 8:
            flash("password should not greater then 8")
            return redirect(url_for('user.register'))
        add_to_db(email=email, user_name=username, password=password)
        flash("User created")
        return redirect(url_for('user.login'))
    else:
        return render_template('register.html')


@user_bp.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        user_email = session['email']
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        if len(user_email) == 0 or len(current_password) == 0 or len(new_password) == 0:
            flash("email, username or password is empty")
            # return redirect(url_for('user.change_password'))
        flag = update_password(user_email, current_password, new_password)
        if flag:
            flash("Password updated")
            return redirect(url_for('user.logout'))
        return redirect(url_for('user.change_password'))
    return render_template("change_password.html")
# logout


@user_bp.route('/logout')
@login_required
def logout():
    session.pop('username', None)
    session.pop('email', None)
    session.pop('currentPath', None)
    session.pop('verified', None)
    session.pop('current_video_path', None)
    session.pop('video_list', None)
    return redirect(url_for('user.login'))

