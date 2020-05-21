from project.common import *
from flask_restful import Resource, Api, fields, marshal_with, abort, reqparse
from flask_httpauth import HTTPTokenAuth
from .auth import login_required

# import required models
from project.model.user import UserModel
from project.model.skill import SkillModel
from project.model.seater import SeaterModel

api = Api(app)

user_fields = {
    "username" : fields.String,
    "full_name" : fields.String,
    "bio" : fields.String,
    "isEmailVerified" : fields.Boolean,
    "photo" : fields.String,
    'registration_time': fields.DateTime(dt_format='iso8601'),
}

skill_fields = {
    "skid" : fields.Integer,
    "name" : fields.String
}

seater_fields = {
    "project_name" : fields.String,
    "short_description" : fields.String,
    "full_description" : fields.String,
    "title" : fields.String,
    "time" : fields.DateTime(dt_format='iso8601')
}

class Users(Resource):
    @marshal_with(user_fields)
    def get(self, user_id):
        user = UserModel.getUser(user_id, getCurrentUid())
        if not user:
            abort(404, "User does not exist!")
        return user
        
class CurrentUser(Resource):
    @marshal_with(user_fields)
    @login_required
    def get(self):
        return getCurrentUser()

class CurrentUserPhoto(Resource):
    @login_required
    def put(self):
        size = len(request.data) / 1000000
        if size > 2:
            abort(400, message = "The file cannot be higher than 2MB")

        newFileName = str(uid) + "_" + generateCode(10) + ".jpg"

        with open(UPLOAD_FOLDER + "/users/up/" + newFileName, "wb") as fh:
            fh.write(request.data)
            UserModel.updateProfilePhoto(getCurrentUid(), newFileName)

            #Delete old uploaded file
            if user["photo"] != None:
                try:
                    os.remove(UPLOAD_FOLDER + "/users/up/" + user["photo"])
                except:
                    print("File couldn't be removed: " + UPLOAD_FOLDER + "/users/up/" + user["photo"])
                    abort(500, message = "File couldn't be removed")
        return {
            "result" : "success"
        }

class CurrentUserFullName(Resource):
    @login_required
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument("full-name", type=str, location="json", required=True)
        args = parser.parse_args()

        full_name = args["full-name"]

        if not isValidFullName(full_name):
            abort(400, message = "Full name should be at least one character.")

        # Update the full name
        UserModel.updateFullname(getCurrentUid(), full_name)

        return {
            "result" : "success"
        }

class CurrentUserBio(Resource):
    @login_required
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument("bio", type=str, location="json", required=True)
        args = parser.parse_args()

        bio = args["bio"]

        # Update the bio
        UserModel.updateBio(getCurrentUid(), bio)

        return {
            "result" : "success"
        }

class CurrentUserUsername(Resource):
    @login_required
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument("username", type=str, location="json", required=True)
        parser.add_argument("password", type=str, location="json", required=True)
        args = parser.parse_args()

        username = args["username"]
        password = args["password"]

        if not UserModel.checkPassword(getCurrentUid(), password):
            abort(401, message = "Unauthorized action! Password is not correct.")
        
        if not isValidUsername(username):
            abort(
                400,
                message = "Username is not valid! It should be at least 1 character alpha-numeric and can contain '-', '_'"
            )

        # Update the username
        UserModel.updateUsername(getCurrentUid(), username)

        return {
            "result" : "success"
        }

class CurrentUserEmail(Resource):
    @login_required
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument("email", type=str, location="json", required=True)
        parser.add_argument("password", type=str, location="json", required=True)
        args = parser.parse_args()

        email = args["email"]
        password = args["password"]

        if not UserModel.checkPassword(getCurrentUid(), password):
            abort(401, message = "Unauthorized action! Password is not correct.")
        
        if not isValidEmail(email):
            abort(
                400,
                message = "The email is not valid!"
            )

        # Update the email
        UserModel.updateEmail(getCurrentUid(), email)

        return {
            "result" : "success"
        }

class CurrentUserPassword(Resource):
    @login_required
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument("current-password", type=str, location="json", required=True)
        parser.add_argument("new-password", type=str, location="json", required=True)
        parser.add_argument("confirm-new-password", type=str, location="json", required=True)
        args = parser.parse_args()

        current_password = args["current-password"]
        new_password = args["new-password"]
        confirm_new_password = args["confirm-new-password"]

        if not UserModel.checkPassword(getCurrentUid(), current_password):
            abort(401, message = "Unauthorized action! Current password is not correct.")
        
        if new_password is not confirm_new_password:
            abort(401, message = "Passwords don't match!")

        if not isValidPassword(new_password):
            abort(401, message = "Password is not valid! It must be at least 6 characters.")
        
        # Update the password
        UserModel.updatePassword(getCurrentUid(), newPassword)

        return {
            "result": "success"
        }

class CurrentUserSkills(Resource):
    def get(self):
        # Get the skills
        skills = SkillModel.getUserSkills(getCurrentUid())

        return skills
    
    @login_required
    @marshal_with(skill_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("skill", type=str, location="json", required=True)
        args = parser.parse_args()
        skill_name = args["skill"]

        if len(skill_name) == 0:
            abort(400, message = "Skill cannot be empty!")

        # Strip and uppercase first letters
        skill_name = skill_name.strip().title()

        # Save the skill
        skid = SkillModel.addUserSkill(getCurrentUid(), skill_name)

        return {
            "skid" : skid,
            "name" : args["skill"]
        }

class CurrentUserSingleSkill(Resource):
    @login_required
    def delete(self, skid):
        # Get the skill
        skill = SkillModel.getUserSkill(args["skid"])

        if not skill:
            abort(400, message = "There is no such a skill")

        # Delete the skill
        SkillModel.removeUserSkill(getCurrentUid(), args["skid"])

        return {
            "result" : "success"
        }

class UserSeaters(Resource):
    @marshal_with(seater_fields)
    def get(self, user_id):
        # Get the user
        user = UserModel.getUser(user_id, getCurrentUid())

        if not user:
            abort(404, message = "There is no such a user!")

        # Get the seaters
        seaters = SeaterModel.getUserSeaters(user_id)

        return seaters

class UserSeaterNumber(Resource):
    def get(self, user_id):
        # Get the user
        user = UserModel.getUser(user_id, getCurrentUid())

        if not user:
            abort(404, message = "There is no such a user!")

        # Get the number
        number = SeaterModel.getUserSeaterNumber(user_id)

        return number

api.add_resource(Users, "/api/users/<user_id>")
api.add_resource(CurrentUser, "/api/users/current")
api.add_resource(CurrentUserPhoto, "/api/users/current/photo")
api.add_resource(CurrentUserFullName, "/api/users/current/full-name")
api.add_resource(CurrentUserBio, "/api/users/current/bio")
api.add_resource(CurrentUserUsername, "/api/users/current/username")
api.add_resource(CurrentUserEmail, "/api/users/current/email")
api.add_resource(CurrentUserPassword, "/api/users/current/password")
api.add_resource(CurrentUserSkills, "/api/users/current/skills")
api.add_resource(CurrentUserSingleSkill, "/api/users/current/skills/<skid>")
api.add_resource(UserSeaters, "/api/users/<user_id>/seaters")
api.add_resource(UserSeaterNumber, "/api/users/<user_id>/seaters/number")