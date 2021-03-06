from __future__ import print_function
from flask import (
    Blueprint, redirect, render_template, request, session, url_for, flash
)
from utils import userList, drives, get_os

user_bp = Blueprint('user', __name__)


@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    user = []
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user.append(username)
        user.append(password)
        if len(username) == 0 or len(password) == 0:
            flash("username or password is empty")
            return redirect(request.url)
        if user in userList:
            session['username'] = request.form['username']
            session['currentPath'] = drives[0][1] if get_os() == 'Linux' else drives[0][0]
            return redirect(url_for('drive.index'))
        else:
            flash("incorrect username or password ")
            return redirect(request.url)
    return render_template('index.html', name="!", user_list=userList, userCount=len(userList))


# Register user
@user_bp.route('/register', methods=['GET'])
def register():
    return render_template('register.html')


@user_bp.route('/add', methods=['POST'])
def add():
    user = []
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if len(username) == 0 or len(password) == 0:
            flash("username or password is empty")
            return redirect(url_for('user.register'))
        if len(password) > 8:
            flash("password should not greater then 8")
            return redirect(url_for('user.register'))
        user.append(username)
        user.append(password)
        userList.append(user)
        return redirect(url_for('user.login'))
    else:
        return render_template('register.html')


# logout
@user_bp.route('/logout')
def logout():
    if 'username' not in session:
        return "login first <a href='/login'>login</a>"
    session.pop('username', None)
    session.pop('currentPath', None)
    return redirect(url_for('drive.index'))
