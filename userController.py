from common import *

#USER CONTROLLER

@app.route("/u/<string:username>")
def userProfile(username):
  currentUser = getCurrentUser()
  user = ModelObject["userModel"].getUserByUsername(username, session["uid"])
  userLinks = ModelObject["userModel"].getUserLinks(user["uid"])
  userProjects = ModelObject["projectModel"].getUserProjects(user["uid"])
  lastUserPosts = ModelObject["userPostModel"].getLastUserPosts(user["uid"], 10, getCurrentUid())

  #Remove password and email fields
  user.pop("password")
  user.pop("email")

  print(userLinks)

  return render_template(
    "user-profile.html",
    currentUser = currentUser,
    user = user,
    userLinks = userLinks,
    userProjects = userProjects,
    lastUserPosts = lastUserPosts
    )