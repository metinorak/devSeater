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

class Following(Resource):
    @marshal_with(resource_fields)
    @login_required
    def post(self, user_id):
        UserModel.follow(getCurrentUid(), user_id)
        return {"result" : True}

    @marshal_with(resource_fields)
    @login_required
    def delete(self, user_id):
        UserModel.unFollow(getCurrentUid(), user_id)
        return {"result" : True}    

api.add_resource(Following, '/api/following/<user_id>')
