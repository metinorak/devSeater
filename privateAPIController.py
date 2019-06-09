from common import *
from datetime import datetime
import json
import os

class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat(sep = " ")

        return json.JSONEncoder.default(self, o)

#USER
@app.route("/private-api/user/is-logged-in")
def isLoggedIn():
    result = (getCurrentUid() != None)
    return json.dumps({"result" : result})

@app.route("/private-api/user")
@login_required
def getUser():
    if request.method == "GET":
        uid = request.args.get("uid")
        username = request.args.get("username")
        email = request.args.get("email")

        if uid != None:
            user = ModelObject["userModel"].getUser(uid)
        elif username != None:
            user = ModelObject["userModel"].getUserByUsername(username)
        elif email != None:
            user = ModelObject["userModel"].getUserByEmail(email)
        else:
            return render_template("private-api/unknown-request.html")
        try:
            user.pop("password")
        except:
            print("password field cannot be popped!")
            return
        return json.dumps(user, cls=DateTimeEncoder)

    return redirect(url_for("index"))


@app.route("/private-api/current-user")
@login_required
def currentUser():
    return json.dumps(getCurrentUser(), cls=DateTimeEncoder)


@app.route("/private-api/is-there-this-username/<string:username>")
@login_required
def isThereThisUsername(username):
    data = dict()
    if ModelObject["userModel"].isThereThisUsername(username):
        data["result"] = True
    else:
        data["result"] = False
    
    return json.dumps(data)

@app.route("/private-api/is-there-this-email/<string:email>")
@login_required
def isThereThisEmail(email):
    data = dict()
    if ModelObject["userModel"].isThereThisEmail(email):
        data["result"] = True
    else:
        data["result"] = False
    
    return json.dumps(data)

@app.route("/private-api/user/is-global-admin/<string:uid>")
@login_required
def isGlobalAdmin(uid):
    data = dict()
    if ModelObject["userModel"].isGlobalAdmin(uid):
        data["result"] = True
    else:
        data["result"] = False
    
    return json.dumps(data)

@app.route("/private-api/follow/<string:uid>")
@login_required
def follow(uid):
    ModelObject["userModel"].follow(getCurrentUid(), uid)

    return json.dumps({
        "result": "success"
    })

@app.route("/private-api/unfollow/<string:uid>")
@login_required
def unfollow(uid):
    ModelObject["userModel"].unFollow(getCurrentUid(), uid)

    return json.dumps({
        "result": "success"
    })

@app.route("/private-api/user-links", methods = ["GET", "POST", "PUT", "DELETE"])
@login_required
def userLinks():
    if request.method == "GET":
        uid = request.args.get("uid")
        if uid == None:
            uid = getCurrentUid()
        #Getting all user's links
        links = ModelObject["userModel"].getUserLinks(uid)
        return json.dumps(links, cls=DateTimeEncoder)
    elif request.method == "POST":
        #Stripping
        data = json.loads(request.data)
        data["name"] = data["name"].strip()
        data["link"] = data["link"].strip()

        #Adding new user link
        if data["name"] != "" and data["link"] != "":
            ulid = ModelObject["userModel"].addUserLink(getCurrentUid(), data["name"], data["link"])
            return json.dumps({
                "result" : "success",
                "ulid": ulid 
            })
        
    elif request.method == "PUT":
        #Updating a user link
        data = json.loads(request.data)
        ulid = request.args.get("ulid")
        link = ModelObject["userModel"].getUserLink(ulid)

        if link["uid"] == getCurrentUid():
            ModelObject["userModel"].updateUserLink(ulid, data["name"], data["link"])
            return json.dumps({"result" : "success"})
        else:
            return render_template("private-api/forbidden-request.html")

    else:
        #Delete a user link
        #DELETE request

        ulid = request.args.get("ulid")
        link = ModelObject["userModel"].getUserLink(ulid)

        if link["uid"] == getCurrentUid():
            ModelObject["userModel"].removeUserLink(ulid)
            return json.dumps({"result" : "success"})
        else:
            return render_template("private-api/forbidden-request.html")
    return render_template("private-api/unknown-request.html")



#USER POSTS
@app.route("/private-api/user-posts", methods = ["GET", "POST", "PUT", "DELETE"])
@login_required
def userPosts():
    if request.method == "GET":
        #Get last posts
        uid = request.args.get("uid")
        upid = request.args.get("upid")

        if uid == None:
            uid = getCurrentUid()
        
        if upid == None:
            posts = ModelObject["userPostModel"].getLastUserPosts(uid, 10, getCurrentUid())
        else:
            posts = ModelObject["userPostModel"].getPreviousUserPosts(uid, upid, 10, getCurrentUid())
        
        return json.dumps(posts, cls=DateTimeEncoder)

    elif request.method == "POST":
        #Add user post
        data = json.loads(request.data)
        data["post"] = data["post"].strip()

        if data["post"] != "":
            ModelObject["userPostModel"].addUserPost(getCurrentUid(), data["post"])
            return json.dumps({"result" : "success"})
        else:
            return json.dumps({
                "result" : "fail",
                "msg": "The post cannot be empty!"
                })

    elif request.method == "PUT":
        #Get user post id
        upid = request.args.get("upid")

        #Update user post
        data = json.loads(request.data)
        
        #Stripping
        data["post"] = data["post"].strip()

        if upid == "" or upid == None or data["post"] == "":
            return json.dumps({
                "result": "fail",
                "msg": "upid and post cannot be empty"
            })

        post = ModelObject["userPostModel"].getUserPost(["upid"])

        if post["uid"] == getCurrentUid():
            ModelObject["userPostModel"].updateUserPost(upid, data["post"])
            return json.dumps({"result" : "success"})
        else:
            return render_template("private-api/forbidden-request.html")

    else:
        #Delete a user post
        upid = request.args.get("upid")
        post = ModelObject["userPostModel"].getUserPost(upid)

        if post["uid"] == getCurrentUid():
            ModelObject["userPostModel"].removeUserPost(upid)
            return json.dumps({"result": "success"})
        else:
            return render_template("private-api/forbidden-request.html")
    return render_template("private-api/unknown-request.html")

@app.route("/private-api/previous-following-posts")
@login_required
def getPreviousFollowingPosts():
    upid = request.args.get("upid")
    
    if upid != None:
        posts = ModelObject["userPostModel"].getPreviousFollowingPosts(getCurrentUid(), upid, 10)
        return json.dumps(posts, cls=DateTimeEncoder)
    
    return render_template("private-api/unknown-request.html")

@app.route("/private-api/new-following-post-number")
@login_required
def getNewFollowingPostNumber():
    upid = request.args.get("upid")
    if upid != None:
        number = ModelObject["userPostModel"].getNewFollowingPostNumber(getCurrentUid(), upid)

        return json.dumps({
            "number" : number
        })
    return render_template("private-api/unknown-request.html")

@app.route("/private-api/new-following-posts")
@login_required
def getNewFollowingPosts():
    upid = request.args.get("upid")

    if upid != None:
        posts = ModelObject["userPostModel"].getNewFollowingPosts(getCurrentUid(), upid)
        return json.dumps(posts, cls=DateTimeEncoder)

    return render_template("private-api/unknown-request.html")

@app.route("/private-api/user-posts/<string:upid>/like")
@login_required
def likeUserPost(upid):

    ModelObject["userPostModel"].likeUserPost(getCurrentUid(), upid)
    return json.dumps({"result" : "success"})


@app.route("/private-api/user-posts/<string:upid>/unlike")
@login_required
def unlikeUserPost(upid):

    ModelObject["userPostModel"].unlikeUserPost(getCurrentUid(), upid)
    return json.dumps({"result" : "success"})

@app.route("/private-api/user-posts/<string:upid>/likes/number")
@login_required
def userPostLikeNumber(upid):
    number = ModelObject["userPostModel"].getUserPostLikeNumber(upid)
    return json.dumps({"number" : number})


@app.route("/private-api/user-posts/<string:upid>/comments/number")
@login_required
def userPostCommentNumber(upid):
    number = ModelObject["userPostModel"].getUserPostCommentNumber(upid)
    return json.dumps({"number" : number})




@app.route("/private-api/user-posts/<string:upid>/comments", methods = ["GET", "POST", "PUT", "DELETE"])
@login_required
def userPostComments(upid):
    if request.method == "GET":
        #Get last post comments
        upcid = request.args.get("upcid")
        number = request.args.get("number")

        try:
            number = int(number)
        except:
            number = 2

        if upcid == None:
            comments = ModelObject["userPostModel"].getLastUserPostComments(upid, number, getCurrentUid())
        else:
            comments = ModelObject["userPostModel"].getPreviousUserPostComments(upid, upcid, number, getCurrentUid())
        return json.dumps(comments, cls=DateTimeEncoder)

    elif request.method == "POST":
        #Add a new user post comment
        data = json.loads(request.data)
        ModelObject["userPostModel"].addUserPostComment(getCurrentUid(), upid, data["comment"])

        return json.dumps({"result" : "success"})
    elif request.method == "PUT":
        #Update user post comment
        upcid = request.args.get("upcid")
        data = json.loads(request.data)
        comment = ModelObject["userPostModel"].getUserPostComment(upcid)

        if comment["uid"] == getCurrentUid():
            ModelObject["userPostModel"].updateUserPostComment(upcid, data["comment"])
            return json.dumps({"result" : "success"})
        
        return render_template("private-api/forbidden-request.html")

    else:
        #Delete a user post comment
        upcid = request.args.get("upcid")
        comment = ModelObject["userPostModel"].getUserPostComment(upcid)

        if comment["uid"] == getCurrentUid():
            ModelObject["userPostModel"].removeUserPostComment(upcid)
            return json.dumps({"result": "success"})
        
        return render_template("private-api/forbidden-request.html")

    return render_template("private-api/unknown-request.html")


@app.route("/private-api/user-posts/comments/<string:upcid>/like")
@login_required
def likeUserPostComment(upcid):
    ModelObject["userPostModel"].likeUserPostComment(getCurrentUid(), upcid)
    return json.dumps({"result": "success"})


@app.route("/private-api/user-posts/comments/<string:upcid>/unlike")
@login_required
def unlikeUserPostComment(upcid):
    ModelObject["userPostModel"].unlikeUserPostComment(getCurrentUid(), upcid)
    return json.dumps({"result": "success"})

@app.route("/private-api/user-posts/comments/<string:upcid>/like-number")
@login_required
def userPostCommentLikeNumber(upcid):
    number = ModelObject["userPostModel"].getUserPostCommentLikeNumber(upcid)
    return json.dumps({"number" : number})


#USER PROFILE PHOTO
@app.route("/private-api/users/<string:uid>/photo", methods = ["POST", "DELETE"])
@login_required
def userPhoto(uid):
    try:
        uid = int(uid)
    except ValueError:
        uid = getCurrentUid()
    
    user = ModelObject["userModel"].getUser(uid)

    if request.method == "POST":
        size = len(request.data) / 1000000
        if size > 2:
            return json.dumps({
                "result": "fail",
                "msg": "File can not be more than 2 MB"
                })
        #Delete old uploaded file
        if user["photo"] != None:
            try:
                os.remove(UPLOAD_FOLDER + "/users/up/" + user["photo"])
            except:
                print("File couldn't be removed!")

        newFileName = str(uid) + "_" + generateCode(10) + ".jpg"

        with open(UPLOAD_FOLDER + "/users/up/" + newFileName, "wb") as fh:
            fh.write(request.data)
            ModelObject["userModel"].updateProfilePhoto(getCurrentUid(), newFileName)
            return json.dumps({"result": "success"})
    return json.dumps({"result": "fail"})
    
#USER FULL NAME
@app.route("/private-api/users/full-name", methods = ["PUT"])
@login_required
def userFullName():
    fullname = request.args.get("full-name")
    if fullname != None:
        fullname.strip()
        if fullname != "":
            ModelObject["userModel"].updateFullname(getCurrentUid(), fullname)
            return json.dumps({"result": "success"})
    else:
        return json.dumps({"result": "fail"})

#USER BIO
@app.route("/private-api/users/bio", methods = ["PUT"])
@login_required
def userBio():
    bio = json.loads(request.data)["bio"]
    bio.strip()
    if bio != "":
        ModelObject["userModel"].updateBio(getCurrentUid(), bio)
        return json.dumps({"result": "success"})
    else:
        return json.dumps({"result": "fail"})



#USER SKILLS
@app.route("/private-api/user-skills", methods = ["GET", "POST", "DELETE"])
@login_required
def userSkills():
    if request.method == "GET":
        uid = request.args.get("uid")

        if uid == None:
            uid = getCurrentUid()
        
        skills = ModelObject["skillModel"].getUserSkills(uid)

        return json.dumps(skills, cls=DateTimeEncoder)

    elif request.method == "POST":
        skill = request.args.get("skill")
        if skill != None:
            skid = ModelObject["skillModel"].addUserSkill(getCurrentUid(), skill)
            return json.dumps({
                "result": "success",
                "skid": skid
            })

    else:
        #Delete a user skill
        skid = request.args.get("skid")

        if skid != None:
            ModelObject["skillModel"].removeUserSkill(getCurrentUid(), skid)
            return json.dumps({"result": "success"})
    
    return render_template("private-api/unknown-request.html")

#SEATER SKILLS
@app.route("/private-api/seater-skills", methods = ["GET", "POST", "DELETE"])
def seaterSkills():
    if request.method == "GET":
        #Get seater skills
        sid = request.args.get("sid")

        if sid != None:
            skills = ModelObject["skillModel"].getUserSkills(uid)
            return json.dumps(skills, cls=DateTimeEncoder)
        return render_template("private-api/unknown-request.html")

    elif request.method == "POST":
        #Add seater skill
        sid = request.args.get("sid")
        skill = request.args.get("skill")

        pid = ModelObject["seaterModel"].getSeater(sid)["pid"]

        if ModelObject["projectModel"].isProjectAdmin(getCurrentUid(), pid):
            if skill != None:
                ModelObject["skillModel"].addSeaterSkill(sid, skill)
                return json.dumps({"result": "success"})

    else:
        #Delete a user skill
        skid = request.args.get("skid")

        if skid != None:
            skill = ModelObject["skillModel"].getUserSkill(skid)

            if skill["uid"] == getCurrentUid():
                ModelObject["skillModel"].removeUserSkill(skid)
                return json.dumps({"result": "success"})
            else:
                return render_template("private-api/forbidden-request.html")
        
    return render_template("private-api/unknown-request.html")


#SEATERS
@app.route("/private-api/projects/<string:pid>/seaters/all")
@login_required
def projectSeaters(pid):
    seaters = ModelObject["seaterModel"].getAllProjectSeaters(pid)

    return json.dumps(seaters, cls=DateTimeEncoder)

@app.route("/private-api/projects/<string:pid>/seaters/empty")
@login_required
def projectEmptySeaters(pid):
    seaters = ModelObject["seaterModel"].getEmptyProjectSeaters(pid)

    return json.dumps(seaters, cls=DateTimeEncoder)

@app.route("/private-api/projects/<string:pid>/seaters/filled")
@login_required
def projectFilledSeaters(pid):
    seaters = ModelObject["seaterModel"].getFilledProjectSeaters(pid)

    return json.dumps(seaters, cls=DateTimeEncoder)

@app.route("/private-api/projects/<string:pid>/seaters/number")
@login_required
def projectEmptySeaterNumber(pid):
    number = ModelObject["seaterModel"].getEmptyProjectSeaterNumber(pid)

    return json.dumps({"number" : number})

@app.route("/private-api/users/<string:uid>/seaters")
@login_required
def userSeaters(uid):
    seaters = ModelObject["seaterModel"].getUserSeaters(uid)
    return json.dumps(seaters, cls=DateTimeEncoder)

@app.route("/private-api/users/<string:uid>/seaters/number")
@login_required
def userSeaterNumber(uid):
    number = ModelObject["seaterModel"].getUserSeaterNumber(uid)
    return json.dumps({"number" : number})

@app.route("/private-api/seaters/<string:sid>")
def getSeater(sid):
    seater = ModelObject["seaterModel"].getSeater(sid)
    seater["skills"] = ModelObject["skillModel"].getSeaterSkills(sid)
    return json.dumps(seater, cls=DateTimeEncoder)

@app.route("/private-api/projects/<string:pid>/seaters", methods = ["POST"])
@login_required
def createSeater(pid):
    if ModelObject["projectModel"].isProjectAdmin(getCurrentUid(), pid):
        seater = json.loads(request.data)
        seater["pid"] = pid
        sid = ModelObject["seaterModel"].createSeater(pid, seater)

        #Add skills
        for skill in seater["skills"]:
            ModelObject["skillModel"].addSeaterSkill(sid, skill)

        return json.dumps({
            "result": "success",
            "sid": sid
            })
    return render_template("private-api/forbidden-request.html")

@app.route("/private-api/seaters/<string:sid>", methods = ["DELETE"])
@login_required
def removeSeater(sid):
    seater = ModelObject["seaterModel"].getSeater(sid)
    if seater != None:
        if ModelObject["projectModel"].isProjectAdmin(getCurrentUid(), seater["pid"]):
            ModelObject["seaterModel"].removeSeater(sid)
            return json.dumps({"result": "success"})
        else:
            return render_template("private-api/forbidden-request.html")
    return render_template("private-api/unknown-request.html")

@app.route("/private-api/seaters/<string:sid>/dismiss-user")
@login_required
def dismissUserFromSeater(sid):
    seater = ModelObject["seaterModel"].getSeater(sid)

    if seater != None:
        if ModelObject["projectModel"].isProjectAdmin(getCurrentUid(), seater["pid"]) or (seater["uid"] == getCurrentUid()):
            ModelObject["seaterModel"].dismissUser(sid)
            ModelObject["seaterModel"].cancelAspirationToTheSeater(seater["uid"], sid)
            return json.dumps({"result": "success"})
        else:
            return render_template("private-api/forbidden-request.html")
    
    return render_template("private-api/unknown-request.html")

@app.route("/private-api/seaters/<string:sid>", methods = ["PUT"])
@login_required
def updateSeater(sid):
    seater = ModelObject["seaterModel"].getSeater(sid)

    if seater != None:
        if ModelObject["projectModel"].isProjectAdmin(getCurrentUid(), seater["pid"]):
            seater = json.loads(request.data)
            ModelObject["seaterModel"].updateSeater(sid, seater["title"], seater["description"])
            return json.dumps({"result": "success"})
        else:
            return render_template("private-api/forbidden-request.html")
    
    return render_template("private-api/unknown-request.html")

@app.route("/private-api/seaters/<string:sid>/assign/<string:uid>")
@login_required
def assignUser(sid, uid):
    seater = ModelObject["seaterModel"].getSeater(sid)

    if seater != None:
        if ModelObject["projectModel"].isProjectAdmin(getCurrentUid(), seater["pid"]):
            if ModelObject["seaterModel"].isThereSeaterAspiration(uid, sid):
                ModelObject["seaterModel"].assignUser(uid, sid)
                return json.dumps({"result": "success"})
        else:
            return render_template("private-api/forbidden-request.html")
    
    return render_template("private-api/unknown-request.html")

@app.route("/private-api/seaters/<string:sid>/aspire")
@login_required
def aspireSeater(sid):
    seater = ModelObject["seaterModel"].getSeater(sid)
    if ModelObject["projectModel"].isProjectAdmin(getCurrentUid(), seater["pid"]):
        ModelObject["seaterModel"].assignUser(getCurrentUid(), sid)
    else:
        ModelObject["seaterModel"].aspireSeater(getCurrentUid(), sid)
    return json.dumps({"result": "success"})

@app.route("/private-api/seaters/<string:sid>/cancel-aspiration")
@login_required
def cancelSeaterAspiration(sid):
    if ModelObject["seaterModel"].isThereSeaterAspiration(getCurrentUid(), sid):
        ModelObject["seaterModel"].cancelAspirationToTheSeater(getCurrentUid(), sid)
        return json.dumps({"result": "success"})
    else:
        return render_template("private-api/forbidden-request.html")

@app.route("/private-api/seaters/<string:sid>/aspirations")
@login_required
def seaterAspirations(sid):
    seater = ModelObject["seaterModel"].getSeater(sid)
    if ModelObject["projectModel"].isProjectAdmin(getCurrentUid(), seater["pid"]):
        aspirations = ModelObject["seaterModel"].getSeaterAspirations(sid)
        return json.dumps(aspirations, cls=DateTimeEncoder)
    return render_template("private-api/forbidden-request.html")

@app.route("/private-api/seaters/<string:sid>/aspirations/number")
@login_required
def seaterAspirationNumber(sid):
    seater = ModelObject["seaterModel"].getSeater(sid)
    if ModelObject["projectModel"].isProjectAdmin(getCurrentUid(), seater["pid"]):
        number = ModelObject["seaterModel"].getSeaterAspirationNumber(sid)
        return json.dumps({"number": number})
    return render_template("private-api/forbidden-request.html")

@app.route("/private-api/seaters/<string:sid>/reject/<string:uid>")
@login_required
def rejectSeaterAspiration(sid, uid):
    seater = ModelObject["seaterModel"].getSeater(sid)

    if seater != None and uid != None:
        if ModelObject["projectModel"].isProjectAdmin(getCurrentUid(), seater["pid"]):
            ModelObject["seaterModel"].rejectSeaterAspiration(uid, sid)
            return json.dumps({"result": "success"})
        else:
            return render_template("private-api/forbidden-request.html")
    
    return render_template("private-api/unknown-request.html")


#PROJECT CONTROLLER
@app.route("/private-api/user/<string:uid>/projects")
@login_required
def getUserProjects(uid):
    projects = ModelObject["projectModel"].getUserProjects(uid)

    return json.dumps(projects, cls=DateTimeEncoder)

@app.route("/private-api/projects/<string:pid>")
@login_required
def getProject(pid):
    project = ModelObject["projectModel"].getProject(pid)

    return json.dumps(project, cls=DateTimeEncoder)

@app.route("/private-api/projects/<string:pid>/members")
@login_required
def getProjectMembers(pid):
    members = ModelObject["projectModel"].getMembers(pid, getCurrentUid())

    return json.dumps(members, cls=DateTimeEncoder)

@app.route("/private-api/projects/<string:pid>/members/number")
def getNumberOfMembers(pid):
    number = ModelObject["projectModel"].getNumberOfMembers(pid)

    return json.dumps({"number" : number})

@app.route("/private-api/popular-projects/")
@login_required
def getPopularProjects():
    howMany = request.args.get("how-many")

    if howMany == None:
        howMany = 4

    projects = ModelObject["projectModel"].getPopularProjects(howMany)
    
    return json.dumps(projects, cls=DateTimeEncoder)

@app.route("/private-api/check-project-name/<string:name>")
@login_required
def isThereThisProjectName(name):
    result = ModelObject["projectModel"].isThereThisProjectName(name)

    return json.dumps({
        "result": result
    })
    

@app.route("/private-api/projects/<string:pid>/photo", methods = ["POST", "DELETE"])
@login_required
def projectPhoto(pid):
    project = ModelObject["projectModel"].getProject(pid)
    if not ModelObject["projectModel"].isProjectAdmin(getCurrentUid(), pid):
        return render_template("private-api/forbidden-request.html")

    if request.method == "POST":
        size = len(request.data) / 1000000
        if size > 2:
            return json.dumps({
                "result": "fail",
                "msg": "File can not be more than 2 MB"
                })
        #Delete old uploaded file
        if project["photo"] != None:
            os.remove(UPLOAD_FOLDER + "/projects/pp/" + project["photo"])

        newFileName = str(pid) + "_" + generateCode(10) + ".jpg"

        with open(UPLOAD_FOLDER + "/projects/pp/" + newFileName, "wb") as fh:
            fh.write(request.data)
            ModelObject["projectModel"].updateProjectPhoto(pid, newFileName)
            return json.dumps({"result": "success"})
    return json.dumps({"result": "fail"})

@app.route("/private-api/projects/<string:pid>/name/<string:newName>", methods = ["PUT"])
@login_required
def updateProjectName(pid, newName):
    if not ModelObject["projectModel"].isProjectAdmin(getCurrentUid(), pid):
        return render_template("private-api/forbidden-request.html")

    if not isValidProjectName(newName):
        return json.dumps({
            "result" : "fail",
            "msg" : "Project name is not valid"
        })
    
    ModelObject["projectModel"].updateProjectName(pid, newName)
    return json.dumps({"result": "success"})

@app.route("/private-api/projects/<string:pid>/short-description", methods = ["PUT"])
@login_required
def updateProjectShortDescription(pid):
    if not ModelObject["projectModel"].isProjectAdmin(getCurrentUid(), pid):
        return render_template("private-api/forbidden-request.html")
    
    description = json.loads(request.data)["description"]

    ModelObject["projectModel"].updateShortDescription(pid, description)
    return json.dumps({"result": "success"})

@app.route("/private-api/projects/<string:pid>/full-description", methods = ["PUT"])
@login_required
def updateProjectFullDescription(pid):
    if not ModelObject["projectModel"].isProjectAdmin(getCurrentUid(), pid):
        return render_template("private-api/forbidden-request.html")
    
    description = json.loads(request.data)["description"]

    ModelObject["projectModel"].updateFullDescription(pid, description)
    return json.dumps({"result": "success"})

@app.route("/private-api/projects/<string:pid>/admins")
@login_required
def getProjectAdmins(pid):
    admins = ModelObject["projectModel"].getProjectAdmins(pid)
    return json.dumps(admins, cls=DateTimeEncoder)

@app.route("/private-api/projects/<string:pid>/links", methods = ["GET", "POST", "PUT", "DELETE"])
@login_required
def projectLinks(pid):
    if request.method == "GET":
        #Getting all project's links
        links = ModelObject["projectModel"].getProjectLinks(pid)
        return json.dumps(links, cls=DateTimeEncoder)
    elif request.method == "POST":
        #Stripping
        data = json.loads(request.data)
        data["name"] = data["name"].strip()
        data["link"] = data["link"].strip()

        #Adding new project link
        if data["name"] != "" and data["link"] != "":
            plid = ModelObject["projectModel"].addProjectLink(pid, data["name"], data["link"])
            return json.dumps({
                "result" : "success",
                "plid": plid 
            })
        
    elif request.method == "PUT":
        #Updating a user link
        data = json.loads(request.data)
        plid = request.args.get("plid")
        link = ModelObject["projectModel"].getProjectLink(plid)

        if ModelObject["projectModel"].isProjectAdmin(getCurrentUid(), pid):
            ModelObject["projectModel"].updateProjectLink(plid, data["name"], data["link"])
            return json.dumps({"result" : "success"})
        else:
            return render_template("private-api/forbidden-request.html")

    else:
        #Delete a user link
        #DELETE request

        plid = request.args.get("plid")
        link = ModelObject["projectModel"].getProjectLink(plid)

        if ModelObject["projectModel"].isProjectAdmin(getCurrentUid(), link["pid"]):
            ModelObject["projectModel"].removeProjectLink(plid)
            return json.dumps({"result" : "success"})
        else:
            return render_template("private-api/forbidden-request.html")
    return render_template("private-api/unknown-request.html")



#PROJECT POST CONTROLLER
@app.route("/private-api/projects/<string:pid>/posts", methods = ["GET", "POST", "PUT", "DELETE"])
@login_required
def projectPosts(pid):
    if request.method == "GET":
        #Get last posts
        ppid = request.args.get("ppid")
        if ppid == None:
            posts = ModelObject["projectPostModel"].getLastProjectPosts(pid, 10, getCurrentUid())
        else:
            posts = ModelObject["projectPostModel"].getPreviousProjectPosts(pid, ppid, 10, getCurrentUid())

        return json.dumps(posts, cls=DateTimeEncoder)

    elif request.method == "POST":
        if not ModelObject["projectModel"].isProjectMember(getCurrentUid(), pid):
            return render_template("private-api/forbidden-request.html")

        #Stripping
        data = json.loads(request.data)
        data["post"] = data["post"].strip()

        if data["post"] != "":
            #Add project post
            ModelObject["projectPostModel"].addProjectPost(getCurrentUid(), pid, data["post"])
            return json.dumps({"result" : "success"})
        else:
            return json.dumps({
                "result": "fail",
                "msg": "post cannot be empty"
            })

    elif request.method == "PUT":
        if not ModelObject["projectModel"].isProjectMember(getCurrentUid(), pid):
            return render_template("private-api/forbidden-request.html")

        #Stripping
        data = json.loads(request.data)
        data["post"] = data["post"].strip()

        #Update project post
        ppid = request.args.get("ppid")

        #Validate
        if data["post"] == "" or ppid == None:
            return json.dumps({
                "result": "fail",
                "msg": "ppid and post cannot be empty"
            })

        post = ModelObject["projectPostModel"].getProjectPost(ppid)

        if post["uid"] == getCurrentUid():
            ModelObject["projectPostModel"].updateProjectPost(ppid, data["post"])
            return json.dumps({"result" : "success"})
        else:
            return render_template("private-api/forbidden-request.html")

    else:
        #Delete a project post
        ppid = request.args.get("ppid")
        post = ModelObject["projectPostModel"].getProjectPost(ppid, getCurrentUid())

        if post["uid"] == getCurrentUid():
            ModelObject["projectPostModel"].removeProjectPost(ppid)
            return json.dumps({"result": "success"})
        else:
            return render_template("private-api/forbidden-request.html")
    return render_template("private-api/unknown-request.html")

@app.route("/private-api/projects/<string:pid>/members/check/<string:uid>")
@login_required
def isProjectMember(pid, uid):
    result = ModelObject["projectModel"].isProjectMember(uid, pid)
    return json.dumps({"result": result})

@app.route("/private-api/projects/<string:pid>/admins/check/<string:uid>")
@login_required
def isProjectAdmin(pid, uid):
    result = ModelObject["projectModel"].isProjectAdmin(uid, pid)
    return json.dumps({"result": result})

@app.route("/private-api/project-posts/<string:ppid>/like")
@login_required
def likeProjectPost(ppid):
    ModelObject["projectPostModel"].likeProjectPost(getCurrentUid(), ppid)
    return json.dumps({"result" : "success"})


@app.route("/private-api/project-posts/<string:ppid>/unlike")
@login_required
def unlikeProjectPost(ppid):
    ModelObject["projectPostModel"].unlikeProjectPost(getCurrentUid(), ppid)
    return json.dumps({"result" : "success"})

@app.route("/private-api/project-posts/<string:ppid>/likes/number")
@login_required
def projectPostLikeNumber(ppid):
    number = ModelObject["projectPostModel"].getProjectPostLikeNumber(ppid)
    return json.dumps({"number" : number})


@app.route("/private-api/project-posts/<string:ppid>/comments/number")
@login_required
def projectPostCommentNumber(ppid):
    number = ModelObject["projectPostModel"].getProjectPostCommentNumber(ppid)
    return json.dumps({"number" : number})


@app.route("/private-api/project-posts/<string:ppid>/comments", methods = ["GET", "POST", "PUT", "DELETE"])
@login_required
def projectPostComments(ppid):
    if request.method == "GET":
        #Get last post comments
        ppcid = request.args.get("ppcid")
        number = request.args.get("number")
        try:
            number = int(number)
        except:
            number = 2

        if ppcid == None:
            comments = ModelObject["projectPostModel"].getLastProjectPostComments(ppid, number, getCurrentUid())
        else:
            comments = ModelObject["projectPostModel"].getPreviousProjectPostComments(ppid, ppcid, number, getCurrentUid())
        return json.dumps(comments, cls=DateTimeEncoder)
    elif request.method == "POST":
        #Add a new user post comment
        data = json.loads(request.data)
        ModelObject["projectPostModel"].addProjectPostComment(getCurrentUid(), ppid, data["comment"])

        return json.dumps({"result" : "success"})
    elif request.method == "PUT":
        #Update user post comment
        data = json.loads(request.data)
        ppcid = request.args.get("ppcid")
        comment = ModelObject["projectPostModel"].getProjectPostComment(ppcid, getCurrentUid())

        if comment["uid"] == getCurrentUid():
            ModelObject["projectPostModel"].updateProjectPostComment(ppcid, data["comment"])
            return json.dumps({"result" : "success"})
        
        return render_template("private-api/forbidden-request.html")

    else:
        #Delete a user post comment
        ppcid = request.args.get("ppcid")
        comment = ModelObject["projectPostModel"].getProjectPostComment(ppcid, getCurrentUid())

        if comment["uid"] == getCurrentUid():
            ModelObject["projectPostModel"].removeProjectPostComment(ppcid)
            return json.dumps({"result": "success"})
        
        return render_template("private-api/forbidden-request.html")

    return render_template("private-api/unknown-request.html")


@app.route("/private-api/project-posts/comments/<string:ppcid>/like")
@login_required
def likeProjectPostComment(ppcid):
    ModelObject["projectPostModel"].likeProjectPostComment(getCurrentUid(), ppcid)
    return json.dumps({"result": "success"})


@app.route("/private-api/project-posts/comments/<string:ppcid>/unlike")
@login_required
def unlikeProjectPostComment(ppcid):
    ModelObject["projectPostModel"].unlikeProjectPostComment(getCurrentUid(), ppcid)
    return json.dumps({"result": "success"})

@app.route("/private-api/project-posts/comments/<string:ppcid>/likes/number")
@login_required
def projectPostCommentLikeNumber(upcid):
    number = ModelObject["projectPostModel"].getProjectPostCommentLikeNumber(ppcid)
    return json.dumps({"number": number})


#NOTIFICATION CONTROLLER
@app.route("/private-api/notifications/new")
@login_required
def getNewNotifications():
    notifications = ModelObject["notificationModel"].getNewNotifications(getCurrentUid(), 10)
    return json.dumps(notifications, cls=DateTimeEncoder)

@app.route("/private-api/notifications/new/number")
@login_required
def getNewNotificationNumber():
    number = ModelObject["notificationModel"].getNewNotificationNumber(getCurrentUid())
    return json.dumps({
        "number" : number
    })

@app.route("/private-api/notifications/last")
@login_required
def getLastNotifications():
    notifications = ModelObject["notificationModel"].getNotifications(getCurrentUid(), 20)
    return json.dumps(notifications, cls=DateTimeEncoder)


#MESSAGE CONTROLLER
@app.route("/private-api/messages/send")
@login_required
def sendMessage():
    message = json.loads(request.data)
    ModelObject["messageModel"].sendMessage(getCurrentUid(), message["receiver_id"], message["text"])
    return json.dumps({"result": "success"})

@app.route("/private-api/messages/delete/<string:mid>")
@login_required
def deleteMessage(mid):
    if not ModelObject["messageModel"].isTheUserMessageOwner(getCurrentUid(), mid):
        return render_template("private-api/forbidden-request.html")

    ModelObject["messageModel"].deleteMessage(getCurrentUid(), mid)
    return json.dumps({"result": "success"})

@app.route("/private-api/messages/new-dialog-number")
@login_required
def newDialogNumber():
    number = ModelObject["messageModel"].getNewMessageDialogNumber(getCurrentUid())
    return json.dumps({
        "number" : number
    })

@app.route("/private-api/messages/dialogs")
@login_required
def getDialogList():
    dialogList = ModelObject["messageModel"].getDialogList(getCurrentUid())

    return json.dumps({
        "dialogList" : dialogList
    }, cls=DateTimeEncoder)


@app.route("/private-api/messages/dialogs/<string:uid>")
@login_required
def getDialog(uid):
    page = request.args.get("page")

    if page == None:
        page = 1
    
    msgList = ModelObject["messageModel"].getDialog(getCurrentUid(), uid, page, 10)

    return json.dumps({
        "msgList" : msgList
    }, cls=DateTimeEncoder)



#SEARCH CONTROLLER
@app.route("/private-api/q/<string:query>")
def generalSearch(query):
    userResults = ModelObject["userModel"].searchUsers(query, 5)
    projectResults = ModelObject["projectModel"].searchProjects(query, 5)

    return json.dumps({
        "userResults" : userResults,
        "projectResults" : projectResults
    }, cls=DateTimeEncoder)

@app.route("/private-api/q/skills/<string:query>")
@login_required
def skillSearch(query):
    skills = ModelObject["skillModel"].searchSkills(query, 5)

    return json.dumps(skills, cls=DateTimeEncoder)