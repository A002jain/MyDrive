from functools import wraps
from flask import session, abort, redirect, url_for, flash
from db_file import get_user_by_email


def admin_role(func):
    @wraps(func)
    def check_admin():
        try:
            if session['username'] == "admin":
                return func()
            else:
                return abort(404)
        except KeyError:
            abort(404)
    return check_admin


def login_required(func):
    @wraps(func)
    def check_login(**kwargs):
        if 'username' in session:
            tag = kwargs.get('tag')
            if tag is not None:
                return func(tag)
            else:
                return func()
        else:
            return redirect(url_for('user.login'))
    return check_login


def check_ban_user(func):
    @wraps(func)
    def check_user():
        try:
            user = get_user_by_email(session['email'])
            if user.banned and user is not None:
                flash('You are Banned')
                return redirect(url_for('user.login'))
        except KeyError:
            pass
    return check_user
