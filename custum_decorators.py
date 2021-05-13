from functools import wraps
from flask import session, abort


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
