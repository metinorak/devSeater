from common import *
from mailController import sendVerificationEmail

#HOME CONTROLLER
@app.route("/", methods = ["GET", "POST"])
def index():
  if not isLoggedIn():
    if request.method == "POST":
      email = request.form.get("email").strip()
      name = request.form.get("name").strip()
      username = request.form.get("username").strip()
      password = request.form.get("password").strip()
      terms = request.form.get("terms")
      
      #Validate all values
      errorMessages = dict()
      if(len(email) == 0):
        errorMessages["email"] = "Please enter an email address"
      elif(ModelObject["userModel"].isThereThisEmail(email)):
        errorMessages["email"] = "This email address is already taken"
      elif(not isValidEmail(email)):
        errorMessages["email"] = "Please enter a valid email address"
      
      if(len(name) < 3):
        errorMessages["name"] = "Name should be at least 3 characters"

      if(len(username) < 1):
        errorMessages["username"] = "Username should be at least 1 character"
      elif(ModelObject["userModel"].isThereThisUsername(username)):
        errorMessages["username"] = "This username is already taken"
      
      if(len(password) < 6):
        errorMessages["password"] = "Password should be at least 6 characters"
      
      if(terms != "on"):
        errorMessages["terms"] = "You should accept terms"

      if(not errorMessages):
        ModelObject["userModel"].addUser({
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
    userProjects = ModelObject["projectModel"].getUserProjects(session["uid"])
    lastFollowingPosts = ModelObject["userPostModel"].getLastFollowingPosts(session["uid"], 10)

    popularProjects = ModelObject["projectModel"].getPopularProjects(10)
    whoToFollowList = ModelObject["userModel"].getWhoToFollowList(5, getCurrentUid())

    #Get Current User Informations
    currentUser = ModelObject["userModel"].getUser(session["uid"])

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
      if(ModelObject["userModel"].login(email, password)):
        createSession(email)
        return redirect(url_for("index"))
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
  return render_template("about.html")

@app.route("/contact", methods = ["POST", "GET"])
def contact():
  return render_template("contact.html")

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template(
      'not-found.html',
      title = "404 Not Found!",
      message = "The page you trying to load not found.",
      currentUser = getCurrentUser()
      )