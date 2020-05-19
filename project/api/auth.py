from flask import session
from flask_restful import abort
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" in session:
          return f(*args, **kwargs)
        else:
          abort(401, message="Unauthorized action!")
    return decorated_function