from __future__ import print_function
from flask import (
    Blueprint, redirect, render_template, request, session, url_for, flash
)
from utils import drives, get_os
from db_file import get_user_by_email, add_to_db
from custum_decorators import login_required

user_bp = Blueprint('user', __name__)


@user_bp.route('/')
@login_required
def index():
    return render_template('home.html', loginas=session['username'])


@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if len(email) == 0 or len(password) == 0:
            flash("email or password is empty")
            # return redirect(request.url)
        user = get_user_by_email(email)
        if user is None:
            flash("user did not exist")
        elif user.banned:
            flash("You are Banned")
            # return redirect(url_for('user.login'))
        elif user.password == password:
            session['email'] = email
            session['username'] = user.user_name
            session['currentPath'] = drives[0][1] if get_os() == 'Linux' else drives[0][0]
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


# logout
@user_bp.route('/logout')
@login_required
def logout():
    session.pop('username', None)
    session.pop('email', None)
    session.pop('currentPath', None)
    return redirect(url_for('user.index'))

