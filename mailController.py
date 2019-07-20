from common import *

#Mail Libs
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#MAIL CONTROLLER
def sendMail(email):
  msg = MIMEMultipart()
  msg["From"] = MAIL_ADDR
  msg["To"] = email["To"]
  msg["Subject"] = email["Subject"]

  textBody = MIMEText(email["Body"], "html")

  msg.attach(textBody)

  try:
    mail = smtplib.SMTP(MAIL_HOST, MAIL_PORT)
    mail.ehlo()
    mail.starttls()
    mail.login(MAIL_ADDR, MAIL_PASS)
    mail.sendmail(msg["From"], msg["To"], msg.as_string())
    mail.close()
    return True
  
  except:
    return False
  
@app.route("/password-reset", methods = ["GET", "POST"])
def passwordReset():
  if request.method == "POST":
    email = request.form.get("email")
    hashCodeFromUser = request.form.get("hash")
    password = request.form.get("password")
    confirmPassword = request.form.get("confirm-password")

    if email != None and ModelObject["userModel"].isThereThisEmail(email):
      hashCode = generatePasswordResetHashCode(email)

      if hashCodeFromUser != None and password != None and confirmPassword != None:
        if hashCode == hashCodeFromUser and password == confirmPassword:
          #Hash Password
          hashed_password = sha256_crypt.encrypt(password)

          #Get user id
          userId = ModelObject["userModel"].getUserByEmail(email)["uid"]

          #Update password
          ModelObject["userModel"].updatePassword(userId, hashed_password)

          flash("Your password updated succesfully. Now you can log in.", "success")
          return redirect(url_for("login"))

      else:
        #Send password reset mail

        sendMail({
          "To" : email,
          "Subject" : "Password Reset - devSeater",
          "Body" : render_template("mail/password-reset-mail.html", SITE_ADDR = SITE_ADDR, email = email, hashCode = hashCode)
        })

    else:
      return redirect(url_for("index"))
        
    #Show message
    flash("If you have entered your email address properly, we sent you an email. Please check your inbox.", "success")
    return redirect(url_for("passwordReset"))

  else:
    email = request.args.get("email")
    hashCode = request.args.get("hash")

    return render_template("intro/password-reset.html", email = email, hashCode = hashCode)

@app.route("/email-verify")
def emailVerify():
  if request.method == "GET":
    email = request.args.get("email")
    hashCode = request.args.get("hash")
    
    if email != None and ModelObject["userModel"].isThereThisEmail(email) and hashCode != None:
      if hashCode == generateEmailVerificationHashCode(email):
        ModelObject["userModel"].verifyEmail(email)
        flash("Your email address verified successfully!", "success")
        return redirect(url_for("login"))

  return redirect(url_for("index"))


def generatePasswordResetHashCode(email):
  user = ModelObject["userModel"].getUserByEmail(email)
  h = hashlib.sha256()
  stringToHash = user["email"] + user["password"] + user["full_name"] + user["username"]
  h.update(stringToHash.encode("utf-8"))
  return h.hexdigest()

def generateEmailVerificationHashCode(email):
  user = ModelObject["userModel"].getUserByEmail(email)
  h = hashlib.sha256()
  stringToHash = user["email"] + user["password"] + user["full_name"] + user["username"]
  h.update(stringToHash.encode("utf-8"))
  return h.hexdigest()

def sendVerificationEmail(email):
  hashCode = generateEmailVerificationHashCode(email)
  sendMail({
    "To" : email,
    "Subject" : "Email Verification - devSeater",
    "Body" : render_template("mail/email-verification-mail.html", email = email, hashCode = hashCode, SITE_ADDR = SITE_ADDR)
  })