from project.common import *
from datetime import datetime
import json
import os

# import required models
from project.model.contact import ContactModel
from project.model.message import MessageModel
from project.model.notification import NotificationModel
from project.model.project import ProjectModel
from project.model.projectPost import ProjectPostModel
from project.model.seater import SeaterModel
from project.model.skill import SkillModel
from project.model.user import UserModel
from project.model.userPost import UserPostModel

class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat(sep = " ")

        return json.JSONEncoder.default(self, o)

#USER
@app.route("/private-api/user/is-logged-in")
def isCurrentUserLoggedIn():
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
            user = UserModel.getUser(uid)
        elif username != None:
            user = UserModel.getUserByUsername(username)
        elif email != None:
            user = UserModel.getUserByEmail(email)
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
    if UserModel.isThereThisUsername(username):
        data["result"] = True
    else:
        data["result"] = False
    
    return json.dumps(data)

@app.route("/private-api/is-there-this-email/<string:email>")
@login_required
def isThereThisEmail(email):
    data = dict()
    if UserModel.isThereThisEmail(email):
        data["result"] = True
    else:
        data["result"] = False
    
    return json.dumps(data)

@app.route("/private-api/user/is-global-admin/<string:uid>")
@login_required
def isGlobalAdmin(uid):
    data = dict()
    if UserModel.isGlobalAdmin(uid):
        data["result"] = True
    else:
        data["result"] = False
    
    return json.dumps(data)

@app.route("/private-api/follow/<string:uid>")
@login_required
def follow(uid):
    UserModel.follow(getCurrentUid(), uid)

    return json.dumps({
        "result": "success"
    })

@app.route("/private-api/unfollow/<string:uid>")
@login_required
def unfollow(uid):
    UserModel.unFollow(getCurrentUid(), uid)

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
        links = UserModel.getUserLinks(uid)
        return json.dumps(links, cls=DateTimeEncoder)
    elif request.method == "POST":
        #Stripping
        data = json.loads(request.data)
        data["name"] = data["name"].strip()
        data["link"] = data["link"].strip()

        #Adding new user link
        if data["name"] != "" and data["link"] != "":
            ulid = UserModel.addUserLink(getCurrentUid(), data["name"], data["link"])
            return json.dumps({
                "result" : "success",
                "ulid": ulid 
            })
        
    elif request.method == "PUT":
        #Updating a user link
        data = json.loads(request.data)
        ulid = request.args.get("ulid")
        link = UserModel.getUserLink(ulid)

        if link["uid"] == getCurrentUid():
            UserModel.updateUserLink(ulid, data["name"], data["link"])
            return json.dumps({"result" : "success"})
        else:
            return render_template("private-api/forbidden-request.html")

    else:
        #Delete a user link
        #DELETE request

        ulid = request.args.get("ulid")
        link = UserModel.getUserLink(ulid)

        if link["uid"] == getCurrentUid():
            UserModel.removeUserLink(ulid)
            return json.dumps({"result" : "success"})
        else:
            return render_template("private-api/forbidden-request.html")
    return render_template("private-api/unknown-request.html")



#USER POSTS
@app.route("/private-api/user-posts", methods = ["GET", "POST", "PUT", "DELETE"])
def userPosts():
    if request.method == "GET":
        #Get last posts
        uid = request.args.get("uid")
        upid = request.args.get("upid")

        if uid == None:
            uid = getCurrentUid()
        
        if upid == None:
            posts = UserPostModel.getLastUserPosts(uid, 10, getCurrentUid())
        else:
            posts = UserPostModel.getPreviousUserPosts(uid, upid, 10, getCurrentUid())
        
        return json.dumps(posts, cls=DateTimeEncoder)

    elif request.method == "POST" and isLoggedIn():
        #Add user post
        data = json.loads(request.data)
        data["post"] = data["post"].strip()

        if data["post"] != "":
            UserPostModel.addUserPost(getCurrentUid(), data["post"])
            return json.dumps({"result" : "success"})
        else:
            return json.dumps({
                "result" : "fail",
                "msg": "The post cannot be empty!"
                })

    elif request.method == "PUT" and isLoggedIn():
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

        post = UserPostModel.getUserPost(["upid"])

        if post["uid"] == getCurrentUid():
            UserPostModel.updateUserPost(upid, data["post"])
            return json.dumps({"result" : "success"})
        else:
            return render_template("private-api/forbidden-request.html")

    else:
        #Delete a user post
        upid = request.args.get("upid")
        post = UserPostModel.getUserPost(upid)

        if post["uid"] == getCurrentUid() and isLoggedIn():
            UserPostModel.removeUserPost(upid)
            return json.dumps({"result": "success"})
        else:
            return render_template("private-api/forbidden-request.html")
    return render_template("private-api/unknown-request.html")

@app.route("/private-api/previous-following-posts")
@login_required
def getPreviousFollowingPosts():
    upid = request.args.get("upid")
    
    if upid != None:
        posts = UserPostModel.getPreviousFollowingPosts(getCurrentUid(), upid, 10)
        return json.dumps(posts, cls=DateTimeEncoder)
    
    return render_template("private-api/unknown-request.html")

@app.route("/private-api/new-following-post-number")
@login_required
def getNewFollowingPostNumber():
    upid = request.args.get("upid")
    if upid != None:
        number = UserPostModel.getNewFollowingPostNumber(getCurrentUid(), upid)

        return json.dumps({
            "number" : number
        })
    return render_template("private-api/unknown-request.html")

@app.route("/private-api/new-following-posts")
@login_required
def getNewFollowingPosts():
    upid = request.args.get("upid")

    if upid != None:
        posts = UserPostModel.getNewFollowingPosts(getCurrentUid(), upid)
        return json.dumps(posts, cls=DateTimeEncoder)

    return render_template("private-api/unknown-request.html")

@app.route("/private-api/user-posts/<string:upid>/like")
@login_required
def likeUserPost(upid):

    UserPostModel.likeUserPost(getCurrentUid(), upid)
    return json.dumps({"result" : "success"})


@app.route("/private-api/user-posts/<string:upid>/unlike")
@login_required
def unlikeUserPost(upid):

    UserPostModel.unlikeUserPost(getCurrentUid(), upid)
    return json.dumps({"result" : "success"})

@app.route("/private-api/user-posts/<string:upid>/likes/number")
@login_required
def userPostLikeNumber(upid):
    number = UserPostModel.getUserPostLikeNumber(upid)
    return json.dumps({"number" : number})


@app.route("/private-api/user-posts/<string:upid>/comments/number")
@login_required
def userPostCommentNumber(upid):
    number = UserPostModel.getUserPostCommentNumber(upid)
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
            comments = UserPostModel.getLastUserPostComments(upid, number, getCurrentUid())
        else:
            comments = UserPostModel.getPreviousUserPostComments(upid, upcid, number, getCurrentUid())
        return json.dumps(comments, cls=DateTimeEncoder)

    elif request.method == "POST":
        #Add a new user post comment
        data = json.loads(request.data)
        UserPostModel.addUserPostComment(getCurrentUid(), upid, data["comment"])

        return json.dumps({"result" : "success"})
    elif request.method == "PUT":
        #Update user post comment
        upcid = request.args.get("upcid")
        data = json.loads(request.data)
        comment = UserPostModel.getUserPostComment(upcid)

        if comment["uid"] == getCurrentUid():
            UserPostModel.updateUserPostComment(upcid, data["comment"])
            return json.dumps({"result" : "success"})
        
        return render_template("private-api/forbidden-request.html")

    else:
        #Delete a user post comment
        upcid = request.args.get("upcid")
        comment = UserPostModel.getUserPostComment(upcid)

        if comment["uid"] == getCurrentUid():
            UserPostModel.removeUserPostComment(upcid)
            return json.dumps({"result": "success"})
        
        return render_template("private-api/forbidden-request.html")

    return render_template("private-api/unknown-request.html")


@app.route("/private-api/user-posts/comments/<string:upcid>/like")
@login_required
def likeUserPostComment(upcid):
    UserPostModel.likeUserPostComment(getCurrentUid(), upcid)
    return json.dumps({"result": "success"})


@app.route("/private-api/user-posts/comments/<string:upcid>/unlike")
@login_required
def unlikeUserPostComment(upcid):
    UserPostModel.unlikeUserPostComment(getCurrentUid(), upcid)
    return json.dumps({"result": "success"})

@app.route("/private-api/user-posts/comments/<string:upcid>/like-number")
@login_required
def userPostCommentLikeNumber(upcid):
    number = UserPostModel.getUserPostCommentLikeNumber(upcid)
    return json.dumps({"number" : number})


#USER PROFILE PHOTO
@app.route("/private-api/users/<string:uid>/photo", methods = ["POST", "DELETE"])
@login_required
def userPhoto(uid):
    try:
        uid = int(uid)
    except ValueError:
        uid = getCurrentUid()
    
    user = UserModel.getUser(uid)

    if request.method == "POST":
        size = len(request.data) / 1000000
        if size > 2:
            return json.dumps({
                "result": "fail",
                "msg": "File can not be more than 2 MB"
                })

        newFileName = str(uid) + "_" + generateCode(10) + ".jpg"

        with open(UPLOAD_FOLDER + "/users/up/" + newFileName, "wb") as fh:
            fh.write(request.data)
            UserModel.updateProfilePhoto(getCurrentUid(), newFileName)

            #Delete old uploaded file
            if user["photo"] != None:
                try:
                    os.remove(UPLOAD_FOLDER + "/users/up/" + user["photo"])
                except:
                    print("File couldn't be removed!")
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
            UserModel.updateFullname(getCurrentUid(), fullname)
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
        UserModel.updateBio(getCurrentUid(), bio)
        return json.dumps({"result": "success"})
    else:
        return json.dumps({"result": "fail"})


#UPDATE USERNAME
@app.route("/private-api/users/username", methods = ["PUT"])
@login_required
def updateUsername():
    data = json.loads(request.data)
    newUsername = data["username"]
    password = data["password"]

    if not UserModel.checkPassword(getCurrentUid(), password):
        return json.dumps({
            "result": "fail",
            "msg": "Password is not correct!"
        })

    if not isValidUsername(newUsername):
        return json.dumps({
            "result": "fail",
            "msg": "Username is not valid! It should be at least 1 character alpha-numeric and can contain '-', '_'"
        })

    if newUsername != None and newUsername != "":
        UserModel.updateUsername(getCurrentUid(), newUsername)
        return json.dumps({
            "result" : "success",
            "msg": "Username successfully updated!"
            })
    else:
        return json.dumps({
            "result": "fail",
            "msg": "You have to enter username to update it."
        })

#UPDATE EMAIL
@app.route("/private-api/users/email", methods = ["PUT"])
@login_required
def updateEmail():
    data = json.loads(request.data)
    newEmail = data["email"]
    password = data["password"]

    if not UserModel.checkPassword(getCurrentUid(), password):
        return json.dumps({
            "result": "fail",
            "msg": "Password is not correct!"
        })
    
    if not isValidEmail(newEmail):
        return json.dumps({
            "result": "fail",
            "msg": "Please enter a valid email!"
        })
    
    if getCurrentUser()["email"] == newEmail:
        return json.dumps({
            "result": "fail",
            "msg": "This is your current email!"
        })
    
    UserModel.updateEmail(getCurrentUid(), newEmail)
    return json.dumps({
        "result" : "success",
        "msg": "Email updated! You should activate your new email clicking the activation link we've sent you."
        })

#UPDATE PASSWORD
@app.route("/private-api/users/password", methods = ["PUT"])
@login_required
def updatePassword():
    data = json.loads(request.data)
    
    currentPassword = data["currentPassword"]
    newPassword = data["newPassword"]
    confirmNewPassword = data["confirmNewPassword"]

    if not UserModel.checkPassword(getCurrentUid(), currentPassword):
        return json.dumps({
            "result": "fail",
            "msg": "Current password is not correct!"
        })

    if newPassword != confirmNewPassword:
        return json.dumps({
            "result": "fail",
            "msg": "Passwords don't match!"
        })
    
    if not isValidPassword(newPassword):
        return json.dumps({
            "result": "fail",
            "msg": "Password is not valid! It must be at least 6 characters."
        })
    
    UserModel.updatePassword(getCurrentUid(), newPassword)
    return json.dumps({
        "result": "success",
        "msg": "Password has updated successfully!"
    })

#CHECK USERNAME AVAILABILIY
@app.route("/private-api/users/username/check-availability/<string:username>")
@login_required
def checkUsernameAvailability(username):
    return json.dumps({
        "result": not UserModel.isThereThisUsername(username)
    })

#USER SKILLS
@app.route("/private-api/user-skills", methods = ["GET", "POST", "DELETE"])
def userSkills():
    if request.method == "GET":
        uid = request.args.get("uid")

        if uid == None:
            uid = getCurrentUid()
        
        skills = SkillModel.getUserSkills(uid)

        return json.dumps(skills, cls=DateTimeEncoder)

    elif request.method == "POST" and isLoggedIn():
        skill = request.args.get("skill")
        if skill != None:
            skid = SkillModel.addUserSkill(getCurrentUid(), skill)
            return json.dumps({
                "result": "success",
                "skid": skid
            })

    else:
        #Delete a user skill
        skid = request.args.get("skid")

        if skid != None and isLoggedIn():
            SkillModel.removeUserSkill(getCurrentUid(), skid)
            return json.dumps({"result": "success"})
    
    return render_template("private-api/unknown-request.html")

#SEATER SKILLS
@app.route("/private-api/seater-skills", methods = ["GET", "POST", "DELETE"])
def seaterSkills():
    if request.method == "GET":
        #Get seater skills
        sid = request.args.get("sid")

        if sid != None:
            skills = SkillModel.getUserSkills(getCurrentUid)
            return json.dumps(skills, cls=DateTimeEncoder)
        return render_template("private-api/unknown-request.html")

    elif request.method == "POST" and isLoggedIn():
        #Add seater skill
        sid = request.args.get("sid")
        skill = request.args.get("skill")

        pid = SeaterModel.getSeater(sid)["pid"]

        if ProjectModel.isProjectAdmin(getCurrentUid(), pid):
            if skill != None:
                SkillModel.addSeaterSkill(sid, skill)
                return json.dumps({"result": "success"})

    else:
        #Delete a user skill
        skid = request.args.get("skid")

        if skid != None and isLoggedIn():
            skill = SkillModel.getUserSkill(skid)

            if skill["uid"] == getCurrentUid():
                SkillModel.removeUserSkill(skid)
                return json.dumps({"result": "success"})
            else:
                return render_template("private-api/forbidden-request.html")
        
    return render_template("private-api/unknown-request.html")


#SEATERS
@app.route("/private-api/projects/<string:pid>/seaters/all")
def projectSeaters(pid):
    seaters = SeaterModel.getAllProjectSeaters(pid)

    return json.dumps(seaters, cls=DateTimeEncoder)

@app.route("/private-api/projects/<string:pid>/seaters/empty")
def projectEmptySeaters(pid):
    seaters = SeaterModel.getEmptyProjectSeaters(pid)

    return json.dumps(seaters, cls=DateTimeEncoder)

@app.route("/private-api/projects/<string:pid>/seaters/filled")
def projectFilledSeaters(pid):
    seaters = SeaterModel.getFilledProjectSeaters(pid)

    return json.dumps(seaters, cls=DateTimeEncoder)

@app.route("/private-api/projects/<string:pid>/seaters/number")
def projectEmptySeaterNumber(pid):
    number = SeaterModel.getEmptyProjectSeaterNumber(pid)

    return json.dumps({"number" : number})

@app.route("/private-api/users/<string:uid>/seaters")
def userSeaters(uid):
    seaters = SeaterModel.getUserSeaters(uid)
    return json.dumps(seaters, cls=DateTimeEncoder)

@app.route("/private-api/users/<string:uid>/seaters/number")
def userSeaterNumber(uid):
    number = SeaterModel.getUserSeaterNumber(uid)
    return json.dumps({"number" : number})

@app.route("/private-api/seaters/<string:sid>")
def getSeater(sid):
    seater = SeaterModel.getSeater(sid)
    seater["skills"] = SkillModel.getSeaterSkills(sid)
    return json.dumps(seater, cls=DateTimeEncoder)

@app.route("/private-api/projects/<string:pid>/seaters", methods = ["POST"])
@login_required
def createSeater(pid):
    if ProjectModel.isProjectAdmin(getCurrentUid(), pid):
        seater = json.loads(request.data)
        seater["pid"] = pid
        sid = SeaterModel.createSeater(pid, seater)

        #Add skills
        for skill in seater["skills"]:
            SkillModel.addSeaterSkill(sid, skill)

        return json.dumps({
            "result": "success",
            "sid": sid
            })
    return render_template("private-api/forbidden-request.html")

@app.route("/private-api/seaters/<string:sid>", methods = ["DELETE"])
@login_required
def removeSeater(sid):
    seater = SeaterModel.getSeater(sid)
    if seater != None:
        if ProjectModel.isProjectAdmin(getCurrentUid(), seater["pid"]):
            SeaterModel.removeSeater(sid)
            return json.dumps({"result": "success"})
        else:
            return render_template("private-api/forbidden-request.html")
    return render_template("private-api/unknown-request.html")

@app.route("/private-api/seaters/<string:sid>/dismiss-user")
@login_required
def dismissUserFromSeater(sid):
    seater = SeaterModel.getSeater(sid)

    if seater != None:
        if ProjectModel.isProjectAdmin(getCurrentUid(), seater["pid"]) or (seater["uid"] == getCurrentUid()):
            SeaterModel.dismissUser(sid)
            SeaterModel.cancelAspirationToTheSeater(seater["uid"], sid)
            return json.dumps({"result": "success"})
        else:
            return render_template("private-api/forbidden-request.html")
    
    return render_template("private-api/unknown-request.html")

@app.route("/private-api/seaters/<string:sid>", methods = ["PUT"])
@login_required
def updateSeater(sid):
    seater = SeaterModel.getSeater(sid)

    if seater != None:
        if ProjectModel.isProjectAdmin(getCurrentUid(), seater["pid"]):
            seater = json.loads(request.data)
            SeaterModel.updateSeater(sid, seater["title"], seater["description"])
            return json.dumps({"result": "success"})
        else:
            return render_template("private-api/forbidden-request.html")
    
    return render_template("private-api/unknown-request.html")

@app.route("/private-api/seaters/<string:sid>/assign/<string:uid>")
@login_required
def assignUser(sid, uid):
    seater = SeaterModel.getSeater(sid)

    if seater != None:
        if ProjectModel.isProjectAdmin(getCurrentUid(), seater["pid"]):
            if SeaterModel.isThereSeaterAspiration(uid, sid):
                SeaterModel.assignUser(uid, sid)
                return json.dumps({"result": "success"})
        else:
            return render_template("private-api/forbidden-request.html")
    
    return render_template("private-api/unknown-request.html")

@app.route("/private-api/seaters/<string:sid>/aspire")
@login_required
def aspireSeater(sid):
    seater = SeaterModel.getSeater(sid)
    if ProjectModel.isProjectAdmin(getCurrentUid(), seater["pid"]):
        SeaterModel.assignUser(getCurrentUid(), sid)
    else:
        SeaterModel.aspireSeater(getCurrentUid(), sid)
    return json.dumps({"result": "success"})

@app.route("/private-api/seaters/<string:sid>/cancel-aspiration")
@login_required
def cancelSeaterAspiration(sid):
    if SeaterModel.isThereSeaterAspiration(getCurrentUid(), sid):
        SeaterModel.cancelAspirationToTheSeater(getCurrentUid(), sid)
        return json.dumps({"result": "success"})
    else:
        return render_template("private-api/forbidden-request.html")

@app.route("/private-api/seaters/<string:sid>/aspirations")
@login_required
def seaterAspirations(sid):
    seater = SeaterModel.getSeater(sid)
    if ProjectModel.isProjectAdmin(getCurrentUid(), seater["pid"]):
        aspirations = SeaterModel.getSeaterAspirations(sid)
        return json.dumps(aspirations, cls=DateTimeEncoder)
    return render_template("private-api/forbidden-request.html")

@app.route("/private-api/seaters/<string:sid>/aspirations/number")
def seaterAspirationNumber(sid):
    seater = SeaterModel.getSeater(sid)
    if ProjectModel.isProjectAdmin(getCurrentUid(), seater["pid"]):
        number = SeaterModel.getSeaterAspirationNumber(sid)
        return json.dumps({"number": number})
    return render_template("private-api/forbidden-request.html")

@app.route("/private-api/seaters/<string:sid>/reject/<string:uid>")
@login_required
def rejectSeaterAspiration(sid, uid):
    seater = SeaterModel.getSeater(sid)

    if seater != None and uid != None:
        if ProjectModel.isProjectAdmin(getCurrentUid(), seater["pid"]):
            SeaterModel.rejectSeaterAspiration(uid, sid)
            return json.dumps({"result": "success"})
        else:
            return render_template("private-api/forbidden-request.html")
    
    return render_template("private-api/unknown-request.html")


#PROJECT CONTROLLER
@app.route("/private-api/user/<string:uid>/projects")
def getUserProjects(uid):
    projects = ProjectModel.getUserProjects(uid)

    return json.dumps(projects, cls=DateTimeEncoder)

@app.route("/private-api/projects/<string:pid>")
def getProject(pid):
    project = ProjectModel.getProject(pid)

    return json.dumps(project, cls=DateTimeEncoder)

@app.route("/private-api/projects/<string:pid>/members")
def getProjectMembers(pid):
    members = ProjectModel.getMembers(pid, getCurrentUid())

    return json.dumps(members, cls=DateTimeEncoder)

@app.route("/private-api/projects/<string:pid>/members/number")
def getNumberOfMembers(pid):
    number = ProjectModel.getNumberOfMembers(pid)

    return json.dumps({"number" : number})

@app.route("/private-api/popular-projects/")
def getPopularProjects():
    howMany = request.args.get("how-many")

    if howMany == None:
        howMany = 4

    projects = ProjectModel.getPopularProjects(howMany)
    
    return json.dumps(projects, cls=DateTimeEncoder)

@app.route("/private-api/check-project-name/<string:name>")
def isThereThisProjectName(name):
    result = ProjectModel.isThereThisProjectName(name)

    return json.dumps({
        "result": result
    })
    

@app.route("/private-api/projects/<string:pid>/photo", methods = ["POST", "DELETE"])
@login_required
def projectPhoto(pid):
    project = ProjectModel.getProject(pid)
    if not ProjectModel.isProjectAdmin(getCurrentUid(), pid):
        return render_template("private-api/forbidden-request.html")

    if request.method == "POST":
        size = len(request.data) / 1000000
        if size > 2:
            return json.dumps({
                "result": "fail",
                "msg": "File can not be more than 2 MB"
                })

        newFileName = str(pid) + "_" + generateCode(10) + ".jpg"

        with open(UPLOAD_FOLDER + "/projects/pp/" + newFileName, "wb") as fh:
            fh.write(request.data)
            ProjectModel.updateProjectPhoto(pid, newFileName)

            #Delete old uploaded file
            if project["photo"] != None:
                try:
                    os.remove(UPLOAD_FOLDER + "/projects/pp/" + project["photo"])
                except:
                    print("File couldn't be uploaded.");

            return json.dumps({"result": "success"})
    return json.dumps({"result": "fail"})

@app.route("/private-api/projects/<string:pid>/name/<string:newName>", methods = ["PUT"])
@login_required
def updateProjectName(pid, newName):
    if not ProjectModel.isProjectAdmin(getCurrentUid(), pid):
        return render_template("private-api/forbidden-request.html")

    if not isValidProjectName(newName):
        return json.dumps({
            "result" : "fail",
            "msg" : "Project name is not valid"
        })
    
    ProjectModel.updateProjectName(pid, newName)
    return json.dumps({"result": "success"})

@app.route("/private-api/projects/<string:pid>/short-description", methods = ["PUT"])
@login_required
def updateProjectShortDescription(pid):
    if not ProjectModel.isProjectAdmin(getCurrentUid(), pid):
        return render_template("private-api/forbidden-request.html")
    
    description = json.loads(request.data)["description"]

    ProjectModel.updateShortDescription(pid, description)
    return json.dumps({"result": "success"})

@app.route("/private-api/projects/<string:pid>/full-description", methods = ["PUT"])
@login_required
def updateProjectFullDescription(pid):
    if not ProjectModel.isProjectAdmin(getCurrentUid(), pid):
        return render_template("private-api/forbidden-request.html")
    
    description = json.loads(request.data)["description"]

    ProjectModel.updateFullDescription(pid, description)
    return json.dumps({"result": "success"})

@app.route("/private-api/projects/<string:pid>/admins")
def getProjectAdmins(pid):
    admins = ProjectModel.getProjectAdmins(pid)
    return json.dumps(admins, cls=DateTimeEncoder)

@app.route("/private-api/projects/<string:pid>/links", methods = ["GET", "POST", "PUT", "DELETE"])
def projectLinks(pid):
    if request.method == "GET":
        #Getting all project's links
        links = ProjectModel.getProjectLinks(pid)
        return json.dumps(links, cls=DateTimeEncoder)
    elif request.method == "POST":
        #Stripping
        data = json.loads(request.data)
        data["name"] = data["name"].strip()
        data["link"] = data["link"].strip()

        #Adding new project link
        if data["name"] != "" and data["link"] != "":
            plid = ProjectModel.addProjectLink(pid, data["name"], data["link"])
            return json.dumps({
                "result" : "success",
                "plid": plid 
            })
        
    elif request.method == "PUT" and isLoggedIn():
        #Updating a user link
        data = json.loads(request.data)
        plid = request.args.get("plid")
        link = ProjectModel.getProjectLink(plid)

        if ProjectModel.isProjectAdmin(getCurrentUid(), pid):
            ProjectModel.updateProjectLink(plid, data["name"], data["link"])
            return json.dumps({"result" : "success"})
        else:
            return render_template("private-api/forbidden-request.html")

    else:
        #Delete a user link
        #DELETE request

        plid = request.args.get("plid")
        link = ProjectModel.getProjectLink(plid)

        if isLoggedIn() and ProjectModel.isProjectAdmin(getCurrentUid(), link["pid"]):
            ProjectModel.removeProjectLink(plid)
            return json.dumps({"result" : "success"})
        else:
            return render_template("private-api/forbidden-request.html")
    return render_template("private-api/unknown-request.html")



#PROJECT POST CONTROLLER
@app.route("/private-api/projects/<string:pid>/posts", methods = ["GET", "POST", "PUT", "DELETE"])
def projectPosts(pid):
    if request.method == "GET":
        #Get last posts
        ppid = request.args.get("ppid")
        if ppid == None:
            posts = ProjectPostModel.getLastProjectPosts(pid, 10, getCurrentUid())
        else:
            posts = ProjectPostModel.getPreviousProjectPosts(pid, ppid, 10, getCurrentUid())

        return json.dumps(posts, cls=DateTimeEncoder)

    elif request.method == "POST" and isLoggedIn():
        if not ProjectModel.isProjectMember(getCurrentUid(), pid):
            return render_template("private-api/forbidden-request.html")

        #Stripping
        data = json.loads(request.data)
        data["post"] = data["post"].strip()

        if data["post"] != "":
            #Add project post
            ProjectPostModel.addProjectPost(getCurrentUid(), pid, data["post"])
            return json.dumps({"result" : "success"})
        else:
            return json.dumps({
                "result": "fail",
                "msg": "post cannot be empty"
            })

    elif request.method == "PUT" and isLoggedIn():
        if not ProjectModel.isProjectMember(getCurrentUid(), pid):
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

        post = ProjectPostModel.getProjectPost(ppid)

        if post["uid"] == getCurrentUid():
            ProjectPostModel.updateProjectPost(ppid, data["post"])
            return json.dumps({"result" : "success"})
        else:
            return render_template("private-api/forbidden-request.html")

    else:
        #Delete a project post
        ppid = request.args.get("ppid")
        post = ProjectPostModel.getProjectPost(ppid, getCurrentUid())

        if post["uid"] == getCurrentUid() and isLoggedIn():
            ProjectPostModel.removeProjectPost(ppid)
            return json.dumps({"result": "success"})
        else:
            return render_template("private-api/forbidden-request.html")
    return render_template("private-api/unknown-request.html")

@app.route("/private-api/projects/<string:pid>/members/check/<string:uid>")
@login_required
def isProjectMember(pid, uid):
    result = ProjectModel.isProjectMember(uid, pid)
    return json.dumps({"result": result})

@app.route("/private-api/projects/<string:pid>/admins/check/<string:uid>")
@login_required
def isProjectAdmin(pid, uid):
    result = ProjectModel.isProjectAdmin(uid, pid)
    return json.dumps({"result": result})

@app.route("/private-api/project-posts/<string:ppid>/like")
@login_required
def likeProjectPost(ppid):
    ProjectPostModel.likeProjectPost(getCurrentUid(), ppid)
    return json.dumps({"result" : "success"})


@app.route("/private-api/project-posts/<string:ppid>/unlike")
@login_required
def unlikeProjectPost(ppid):
    ProjectPostModel.unlikeProjectPost(getCurrentUid(), ppid)
    return json.dumps({"result" : "success"})

@app.route("/private-api/project-posts/<string:ppid>/likes/number")
@login_required
def projectPostLikeNumber(ppid):
    number = ProjectPostModel.getProjectPostLikeNumber(ppid)
    return json.dumps({"number" : number})


@app.route("/private-api/project-posts/<string:ppid>/comments/number")
@login_required
def projectPostCommentNumber(ppid):
    number = ProjectPostModel.getProjectPostCommentNumber(ppid)
    return json.dumps({"number" : number})


@app.route("/private-api/project-posts/<string:ppid>/comments", methods = ["GET", "POST", "PUT", "DELETE"])
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
            comments = ProjectPostModel.getLastProjectPostComments(ppid, number, getCurrentUid())
        else:
            comments = ProjectPostModel.getPreviousProjectPostComments(ppid, ppcid, number, getCurrentUid())
        return json.dumps(comments, cls=DateTimeEncoder)
    elif request.method == "POST" and isLoggedIn():
        #Add a new user post comment
        data = json.loads(request.data)
        ProjectPostModel.addProjectPostComment(getCurrentUid(), ppid, data["comment"])

        return json.dumps({"result" : "success"})
    elif request.method == "PUT" and isLoggedIn():
        #Update user post comment
        data = json.loads(request.data)
        ppcid = request.args.get("ppcid")
        comment = ProjectPostModel.getProjectPostComment(ppcid, getCurrentUid())

        if comment["uid"] == getCurrentUid():
            ProjectPostModel.updateProjectPostComment(ppcid, data["comment"])
            return json.dumps({"result" : "success"})
        
        return render_template("private-api/forbidden-request.html")

    else:
        #Delete a user post comment
        ppcid = request.args.get("ppcid")
        comment = ProjectPostModel.getProjectPostComment(ppcid, getCurrentUid())

        if isLoggedIn() and comment["uid"] == getCurrentUid():
            ProjectPostModel.removeProjectPostComment(ppcid)
            return json.dumps({"result": "success"})
        
        return render_template("private-api/forbidden-request.html")

    return render_template("private-api/unknown-request.html")


@app.route("/private-api/project-posts/comments/<string:ppcid>/like")
@login_required
def likeProjectPostComment(ppcid):
    ProjectPostModel.likeProjectPostComment(getCurrentUid(), ppcid)
    return json.dumps({"result": "success"})


@app.route("/private-api/project-posts/comments/<string:ppcid>/unlike")
@login_required
def unlikeProjectPostComment(ppcid):
    ProjectPostModel.unlikeProjectPostComment(getCurrentUid(), ppcid)
    return json.dumps({"result": "success"})

@app.route("/private-api/project-posts/comments/<string:ppcid>/likes/number")
def projectPostCommentLikeNumber(ppcid):
    number = ProjectPostModel.getProjectPostCommentLikeNumber(ppcid)
    return json.dumps({"number": number})

#NOTIFICATION CONTROLLER
@app.route("/private-api/notifications/new")
@login_required
def getNewNotifications():
    notifications = NotificationModel.getNewNotifications(getCurrentUid(), 10)
    return json.dumps(notifications, cls=DateTimeEncoder)

@app.route("/private-api/notifications/new/number")
@login_required
def getNewNotificationNumber():
    number = NotificationModel.getNewNotificationNumber(getCurrentUid())
    return json.dumps({
        "number" : number
    })

@app.route("/private-api/notifications/last")
@login_required
def getLastNotifications():
    notifications = NotificationModel.getNotifications(getCurrentUid(), 20)
    return json.dumps(notifications, cls=DateTimeEncoder)


#MESSAGE CONTROLLER
@app.route("/private-api/messages/send", methods = ["POST"])
@login_required
def sendMessage():
    message = json.loads(request.data)
    mid = MessageModel.sendMessage(getCurrentUid(), message["receiver_id"], message["text"])
    return json.dumps({
        "result": "success",
        "mid": mid
        })

@app.route("/private-api/messages/delete/<string:mid>")
@login_required
def deleteMessage(mid):
    if not MessageModel.isTheUserMessageOwner(getCurrentUid(), mid):
        return render_template("private-api/forbidden-request.html")

    MessageModel.deleteMessage(getCurrentUid(), mid)
    return json.dumps({"result": "success"})

@app.route("/private-api/messages/new-dialog-number")
@login_required
def newDialogNumber():
    number = MessageModel.getNewMessageDialogNumber(getCurrentUid())
    return json.dumps({
        "number" : number
    })

@app.route("/private-api/messages/dialogs")
@login_required
def getDialogList():
    dialogList = MessageModel.getDialogList(getCurrentUid())

    return json.dumps({
        "dialogList" : dialogList
    }, cls=DateTimeEncoder)


@app.route("/private-api/messages/dialogs/<string:uid>")
@login_required
def getDialog(uid):
    mid = request.args.get("mid")
    if mid == None:
        msgList = MessageModel.getDialogLastMessages(getCurrentUid(), uid, 10)
    else:
        msgList = MessageModel.getDialogPreviousMessages(getCurrentUid(), uid, mid, 10)

    return json.dumps({
        "msgList" : msgList
    }, cls=DateTimeEncoder)

@app.route("/private-api/messages/dialogs/<string:uid>", methods = ["DELETE"])
@login_required
def deleteDialog(uid):
    MessageModel.deleteDialog(getCurrentUid(), uid)
    return json.dumps({"result" : "success"})


#SEARCH CONTROLLER
@app.route("/private-api/q/<string:query>")
def generalSearch(query):
    userResults = UserModel.searchUsers(query, 5)
    projectResults = ProjectModel.searchProjects(query, 5)

    return json.dumps({
        "userResults" : userResults,
        "projectResults" : projectResults
    }, cls=DateTimeEncoder)

@app.route("/private-api/q/skills/<string:query>")
@login_required
def skillSearch(query):
    skills = SkillModel.searchSkills(query, 5)

    return json.dumps(skills, cls=DateTimeEncoder)