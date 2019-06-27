from common import *

#USER CONTROLLER

@app.route("/u/<string:username>")
def userProfile(username):
  currentUser = getCurrentUser()
  user = ModelObject["userModel"].getUserByUsername(username, getCurrentUid())

  if user == None:
    return render_template(
      "not-found.html",
      title = "User Not Found!",
      msg = "The user you trying to access not found!",
      currentUser = getCurrentUser()
      )

  userLinks = ModelObject["userModel"].getUserLinks(user["uid"])
  userProjects = ModelObject["projectModel"].getUserProjects(user["uid"])
  lastUserPosts = ModelObject["userPostModel"].getLastUserPosts(user["uid"], 10, getCurrentUid())
  popularProjects = ModelObject["projectModel"].getPopularProjects(10)
  whoToFollowList = ModelObject["userModel"].getWhoToFollowList(5, getCurrentUid())

  #Remove password and email fields
  user.pop("password")
  user.pop("email")

  return render_template(
    "user-profile.html",
    currentUser = currentUser,
    user = user,
    userLinks = userLinks,
    userProjects = userProjects,
    lastUserPosts = lastUserPosts,
    popularProjects = popularProjects,
    whoToFollowList = whoToFollowList
    )
    
@app.route("/settings")
@login_required
def settings():
  return render_template(
    "user-settings.html",
    currentUser = getCurrentUser()    
    )