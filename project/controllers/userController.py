from project.common import *

# import required models
from project.models.userModel import UserModel
from project.models.userPostModel import UserPostModel
from project.models.projectModel import ProjectModel

#USER CONTROLLER

@app.route("/u/<string:username>")
def userProfile(username):
  currentUser = getCurrentUser()
  user = UserModel.getUserByUsername(username, getCurrentUid())

  if user == None:
    return render_template(
      "not-found.html",
      title = "User Not Found!",
      msg = "The user you trying to access not found!",
      currentUser = getCurrentUser()
      )

  userLinks = UserModel.getUserLinks(user["uid"])
  userProjects = ProjectModel.getUserProjects(user["uid"])
  lastUserPosts = UserPostModel.getLastUserPosts(user["uid"], 10, getCurrentUid())
  popularProjects = ProjectModel.getPopularProjects(10)
  whoToFollowList = UserModel.getWhoToFollowList(5, getCurrentUid())

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