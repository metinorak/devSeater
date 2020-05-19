from project.common import *
from flask_restful import Resource, Api, fields, marshal_with, abort, reqparse
from flask_httpauth import HTTPTokenAuth
from .auth import login_required

# import required models
from project.model.user import UserModel

api = Api(app)

# Define fields
user_link_fields = {
    "name" : fields.String,
    "link" : fields.String
}

user_link_list_fields = {
    fields.List(fields.Nested(user_link_fields)),
}

parser = reqparse.RequestParser()
parser.add_argument("uid", type=int)
parser.add_argument("ulid", type=int)
parser.add_argument("name", type=str, location="json")
parser.add_argument("link", type=str, location="json")


class UserLinks(Resource):
    @marshal_with(user_link_fields)
    def get(self):
        args = parser.parse_args()
        uid = args["uid"]

        user_links = UserModel.getUserLinks(uid)
        return user_links

    @login_required
    def post(self):
        args = parser.parse_args()
        ulid = UserModel.addUserLink(getCurrentUid(), args["name"], args["link"])
        
        return {
            "ulid" : ulid,
            "name" : args["name"],
            "link" : args["link"]
        }

    @login_required
    def delete(self):
        args = parser.parse_args()
        ulid = args["ulid"]
        user_link = UserModel.getUserLink(ulid)

        if user_link["uid"] is not getCurrentUid():
            abort(401, message = "Unauthorized action!")

        if not user_link:
            abort(404, message = "There is no such a user link!")

        UserModel.removeUserLink(ulid)
        
        return {
            "message" : "The link was removed!"
        }

api.add_resource(UserLinks, '/api/user-links')
