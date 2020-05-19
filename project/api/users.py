from project.common import *
from flask_restful import Resource, Api, fields, marshal_with, abort
from flask_httpauth import HTTPTokenAuth
from .auth import login_required

# import required models
from project.model.user import UserModel

api = Api(app)

user_fields = {
    "username" : fields.String,
    "full_name" : fields.String,
    "bio" : fields.String,
    "isEmailVerified" : fields.Boolean,
    "photo" : fields.String,
    'registration_time': fields.DateTime(dt_format='iso8601'),
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

api.add_resource(Users, '/api/users/<user_id>')
api.add_resource(CurrentUser, '/api/users/current')
