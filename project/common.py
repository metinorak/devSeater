from flask import render_template, flash,redirect,url_for,session,logging,request
from werkzeug.utils import secure_filename
import re
from passlib.hash import sha256_crypt
import hashlib
from functools import wraps
from project.config import *
import random
import string
from project import app

# import required models
from project.model.user import UserModel

#Common Functions

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" in session:
          return f(*args, **kwargs)
        else:
          flash("Please log in to see this page", "danger")
          return redirect(url_for("login"))
    return decorated_function


def isLoggedIn():
  return ("logged_in" in session)

def isValidPassword(password):
  if len(password) < 6:
    return False
  return True

def isValidEmail(email):
  p = re.compile("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
  return (p.fullmatch(email) != None)

def isValidUsername(username):
  p = re.compile("([A-z0-9_-]*)")
  return (p.fullmatch(username) != None)

def isValidProjectName(projectName):
  if projectName == "" or projectName == None:
    return False
  p = re.compile("([A-z0-9_-]*)")
  return (p.fullmatch(projectName) != None)

def createSession(email):
  user = UserModel.getUserByEmail(email)
  if user:
    session["logged_in"] = True
    session["username"] = user["username"]
    session["email"] = email
    session["full_name"] = user["full_name"]
    session["uid"] = user["uid"]

def isAnAllowedPhotoFile(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_PHOTO_EXTENSIONS

def getCurrentUser():
  if isLoggedIn():
    user = UserModel.getUser(session["uid"])
    #Remove password field
    user.pop("password")
    return user
  else:
    return None

def getCurrentUid():
  if isLoggedIn():
    return session["uid"]
  return None

def generateCode(length=6):
  chars = string.ascii_letters + string.digits
  code = ''.join(random.choice(chars) for i in range(length))
  return code
