from project.common import *
from project.controllers.mailController import sendVerificationEmail

# import required models
from project.models.userModel import UserModel
from project.models.userPostModel import UserPostModel
from project.models.projectModel import ProjectModel
from project.models.contactModel import ContactModel

@app.route("/deneme")
def fsdnfkjjf():
  return "fdfdsf"

#HOME CONTROLLER
@app.route("/", methods = ["GET", "POST"])
def index():
  if not isLoggedIn():
    if request.method == "POST":
      # USER REGISTRATION

      email = request.form.get("email").strip()
      name = request.form.get("name").strip()
      username = request.form.get("username").strip()
      password = request.form.get("password").strip()
      terms = request.form.get("terms")
      
      #Validate all values
      errorMessages = dict()
      if(not isValidEmail(email)):
        errorMessages["email"] = "Please enter a valid email address"
      elif(UserModel.isThereThisEmail(email)):
        errorMessages["email"] = "This email address is already taken"

      if(len(name) < 3):
        errorMessages["name"] = "Name should be at least 3 characters"

      if(not isValidUsername(username)):
        errorMessages["username"] = "Username value may only consist of A-z0-9 and -, _"
      elif(UserModel.isThereThisUsername(username)):
        errorMessages["username"] = "This username is already taken"
      
      if not isValidPassword(password):
        errorMessages["password"] = "Password should be at least 6 characters"
      
      if(terms != "on"):
        errorMessages["terms"] = "You should accept terms"

      if(not errorMessages):
        UserModel.addUser({
          "email" : email,
          "username" : username,
          "full_name" : name,
          "password" : password
        })

        sendVerificationEmail(email)

        flash("User created successfully, please check your inbox for email verification", "success")

        return redirect(url_for("login"))

      else:
        return render_template("intro/intro.html", form = request.form, errorMessages = errorMessages)

    else:
      return render_template("intro/intro.html")
  else:
    #Logged In

    #Get User Projects
    userProjects = ProjectModel.getUserProjects(session["uid"])
    lastFollowingPosts = UserPostModel.getLastFollowingPosts(session["uid"], 10)

    popularProjects = ProjectModel.getPopularProjects(10)
    whoToFollowList = UserModel.getWhoToFollowList(5, getCurrentUid())

    #Get Current User Informations
    currentUser = UserModel.getUser(session["uid"])

    return render_template(
      "index.html",
      userProjects = userProjects,
      popularProjects = popularProjects,
      lastFollowingPosts = lastFollowingPosts,
      currentUser = currentUser,
      whoToFollowList = whoToFollowList
      )

@app.route("/login", methods = ["GET", "POST"])
def login():
  if not isLoggedIn():
    if request.method == "POST":
      #User Login
      email = request.form.get("email")
      password = request.form.get("password")
      if(UserModel.login(email, password)):
        user = UserModel.getUserByEmail(email)

        if user["isEmailVerified"]:
          createSession(email)
          return redirect(url_for("index"))
        else:
          flash("""
          You didn't activate your email address. Please activate your email address.
          If you didn't receive an email, <a href="/send-verification-mail/{}">click here.</a> 
          """.format(email))
          return redirect(url_for("login"))

      else:
        flash("Email or password is not correct")
        return redirect(url_for("login"))
    else:
      return render_template("intro/login.html")
  else:
    return redirect(url_for("index"))

@app.route("/logout")
@login_required
def logout():
  session.clear()
  return redirect(url_for("index"))

@app.route("/about")
def about():
  return render_template("intro/about.html")

@app.route("/terms-and-conditions")
def terms():
  return render_template("intro/terms-and-conditions.html")

@app.route("/privacy-policy")
def privacy():
  return render_template("intro/privacy-policy.html")

@app.route("/contact", methods = ["POST", "GET"])
def contact():
  if request.method == "POST":
    name = request.form.get("name").strip()
    email = request.form.get("email").strip()
    subject = request.form.get("subject").strip()
    message = request.form.get("message").strip()

    isValid = True

    #Validation
    if name == None or name == "":
      isValid = False
      flash("Please enter a name", "alert")
    if not isValidEmail(email):
      isValid = False
      flash("Please enter a valid email", "alert")
    if subject == None or subject == "":
      isValid = False
      flash("Please enter a subject", "alert")
    if message == None or message == "":
      isValid = False
      flash("Please enter a message", "alert")
    
    if isValid:
      ContactModel.addContactMessage({
        "name" : name,
        "subject" : subject,
        "email" : email,
        "message" : message
      })
      
      flash("Message sent successfully", "success")
    
  return render_template("intro/contact.html")

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template(
      'not-found.html',
      title = "404 Not Found!",
      message = "The page you trying to load not found.",
      currentUser = getCurrentUser()
      )

@app.route("/sitemap.xml")
def sitemap():
  lastUsers = UserModel.getLastUsers(500)
  lastProjects = ProjectModel.getLastProjects(500)

  return render_template(
    "sitemap.xml",
    lastUsers = lastUsers,
    lastProjects = lastProjects,
    SITE_ADDR = SITE_ADDR
  )