from project.common import *
from flask_restful import Resource, Api, fields, marshal_with, abort
from flask_httpauth import HTTPTokenAuth
from .auth import login_required

# import required models
from project.model.user import UserModel

api = Api(app)

resource_fields = {
    "result" : fields.Boolean,
}

class EmailControl(Resource):
    @marshal_with(resource_fields)
    def get(self, email):
        if not UserModel.getUserByEmail(email, getCurrentUid()):
            return {"result" : False}
        else:
            return {"result" : True}

class UsernameControl(Resource):
    @marshal_with(resource_fields)
    def get(self, username):
        if not UserModel.getUserByUsername(username, getCurrentUid()):
            return {"result" : False}
        else:
            return {"result" : True}

api.add_resource(EmailControl, '/api/controls/email/<email>')
api.add_resource(UsernameControl, '/api/controls/username/<username>')
