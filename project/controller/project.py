from project.common import *

# import required models
from project.model.project import ProjectModel
from project.model.projectPost import ProjectPostModel
from project.model.user import UserModel
from project.model.skill import SkillModel
from project.model.seater import SeaterModel

@app.route("/create-a-project", methods = ["GET", "POST"])
def createAProject():
  if request.method == "POST":
    projectName = request.form.get("project-name")
    shortDescription = request.form.get("short-description")
    fullDescription = request.form.get("full-description")
    links = request.form.getlist("links[]")
    linkNames = request.form.getlist("link-names[]")

    errorMessages = dict()

    if not isValidProjectName(projectName):
      errorMessages["projectName"] = "A project name can consist of letters, numbers and - _ characters."
    
    if shortDescription == "" or shortDescription == None:
      errorMessages["shortDescription"] = "Short description cannot be empty."
    
    if not errorMessages:
      project = {
        "project_name": projectName,
        "short_description": shortDescription,
        "full_description": fullDescription
      }
      ProjectModel.createProject(project, session["uid"])

      #Add project links
      pid = ProjectModel.getProjectByProjectName(projectName)["pid"]
      
      if pid != None:
        for link, name in zip(links, linkNames):
          ProjectModel.addProjectLink(pid, name, link)

      return redirect(url_for("projectPage", projectName = projectName))
    else:
      return render_template("create-a-project.html", 
      currentUser = getCurrentUser(), 
      errorMessages = errorMessages, 
      form = request.form)

  else:
    return render_template("create-a-project.html", currentUser = getCurrentUser())


@app.route("/p/<string:projectName>")
def projectPage(projectName):
  currentUser = getCurrentUser()
  project = ProjectModel.getProjectByProjectName(projectName)

  if project == None:
    return render_template(
      "not-found.html",
      title = "Project Not Found!",
      msg = "The project you trying to access not found!",
      currentUser = getCurrentUser()
      )

  projectLinks = ProjectModel.getProjectLinks(project["pid"])
  lastProjectPosts = ProjectPostModel.getLastProjectPosts(project["pid"], 10, getCurrentUid())
  numberOfMembers = ProjectModel.getNumberOfMembers(project["pid"])
  numberOfEmptySeaters = SeaterModel.getProjectEmptySeaterNumber(project["pid"])
  popularProjects = ProjectModel.getPopularProjects(10)
  whoToFollowList = UserModel.getWhoToFollowList(5, getCurrentUid())


  return render_template(
    "project-page.html",
    currentUser = currentUser,
    project = project,
    projectLinks = projectLinks,
    lastProjectPosts = lastProjectPosts,
    numberOfMembers = numberOfMembers,
    numberOfEmptySeaters = numberOfEmptySeaters,
    popularProjects = popularProjects,
    whoToFollowList = whoToFollowList
    )
  
@app.route("/p/<string:projectName>/seaters/<string:sid>")
def seaterPage(projectName, sid):
  project = ProjectModel.getProjectByProjectName(projectName)
  seater = SeaterModel.getSeater(sid, getCurrentUid())
  seater["skills"] = SkillModel.getSeaterSkills(sid)
  assignedUser = UserModel.getUser(seater["uid"])
  seater["isProjectAdmin"] = ProjectModel.isProjectAdmin(getCurrentUid(), project["pid"])

  return render_template(
    "seater-page.html",
    currentUser= getCurrentUser(),
    seater = seater,
    assignedUser = assignedUser
  )