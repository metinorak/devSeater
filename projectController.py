from common import *

@app.route("/create-a-project", methods = ["GET", "POST"])
@login_required
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
      ModelObject["projectModel"].createProject(project, session["uid"])

      #Add project links
      pid = ModelObject["projectModel"].getProjectByProjectName(projectName)["pid"]
      
      if pid != None:
        for link, name in zip(links, linkNames):
          ModelObject["projectModel"].addProjectLink(pid, name, link)

      return url_for("projectPage", projectName = projectName)
    else:
      return render_template("create-a-project.html", 
      currentUser = getCurrentUser(), 
      errorMessages = errorMessages, 
      form = request.form)

  else:
    return render_template("create-a-project.html", currentUser = getCurrentUser())