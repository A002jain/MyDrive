from functools import wraps
from flask import session, abort, redirect, url_for, flash
from db_file import get_user_by_email


def admin_role(func):
    @wraps(func)
    def check_admin():
        try:
            if session['username'] == "admin":
                return func()
            return abort(404)
        except KeyError:
            return abort(404)
    return check_admin


def login_required(func):
    @wraps(func)
    def check_login(**kwargs):
        if 'username' in session:
            tag = kwargs.get('tag')
            if tag is not None:
                return func(tag)
            return func()
        return redirect(url_for('user.login'))
    return check_login


def check_ban_user(func):
    @wraps(func)
    def check_user():
        try:
            user = get_user_by_email(session['email'])
            if user.banned and user is not None:
                flash('You are Banned')
                return redirect(url_for('user.logout'))
            return
        except KeyError:
            return redirect(url_for('user.login'))
    return check_user


# def user_verified(func):
#     @wraps(func)
#     def verified(**kwargs):
#         try:
#             if session['verified']:
#                 flash('You are not VERIFIED')
#                 return redirect(url_for('user.index'))
#             tag = kwargs.get('tag')
#             if tag is not None:
#                 return func(tag)
#             else:
#                 return func()
#         except KeyError:
#             pass
#     return verified
