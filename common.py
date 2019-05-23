from flask import Flask, render_template, flash,redirect,url_for,session,logging,request
from werkzeug.utils import secure_filename
import re
from passlib.hash import sha256_crypt
import hashlib
from functools import wraps
from models.config import *

#Mail Libs
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


app = Flask(__name__)
app.secret_key = "martymclfy"

from models import Objects as ModelObject


#Common Functions
#Kullanıcı giriş kontrolü decorator'ı
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
  user = ModelObject["userModel"].getUserByEmail(email)
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
    user = ModelObject["userModel"].getUser(session["uid"])

    #Remove password and email field
    user.pop("password")
    user.pop("email")
    return user
  else:
    return None


