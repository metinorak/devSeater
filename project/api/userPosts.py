from project.common import *
from flask_restful import Resource, Api, fields, marshal_with, abort, reqparse
from flask_httpauth import HTTPTokenAuth
from .auth import login_required

# import required models
from project.model.userPost import UserPostModel

api = Api(app)

# Define fields
user_post_fields = {
    "isLiked" : fields.Boolean,
    "likeNumber" : fields.Integer,
    "commentNumber" : fields.Integer,
    "upid" : fields.Integer,
    "post" : fields.String,
    "username" : fields.String,
    "full_name" : fields.String,
    "photo" : fields.String,
    "time" : fields.DateTime(dt_format="iso8601")
}

class UserPosts(Resource):
    @marshal_with(user_post_fields)
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("uid", type=int, location="args", required=True)
        parser.add_argument("upid", type=int, location="args")

        args = parser.parse_args()
        uid = args["uid"]
        upid = args["upid"]

        user_posts = None

        if not upid:
            # Last posts
            user_posts = UserPostModel.getLastUserPosts(uid, 10, getCurrentUid())
        else:
            # Previous posts before the upid
            user_posts = UserPostModel.getPreviousUserPosts(uid, upid, 10, getCurrentUid())

        return user_posts

    @login_required
    @marshal_with(user_post_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("post", type=str, location="json", required=True)

        args = parser.parse_args()
        post = args["post"]

        upid = UserPostModel.addUserPost(getCurrentUid(), post)

        # Get saved post
        user_post = UserPostModel.getUserPost(upid, getCurrentUid())
        
        return user_post

    @login_required
    @marshal_with(user_post_fields)
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument("upid", type=int, location="json", required=True)
        parser.add_argument("post", type=str, location="json", required=True)

        args = parser.parse_args()
        upid = args["upid"]
        post = args["post"]

        # Get the post
        user_post = UserPostModel.getUserPost(upid, getCurrentUid())

        if not user_post:
            abort(404, message = "There is no such a user!")
        
        if user_post["uid"] is not getCurrentUid():
            abort(401, message = "Unauthorized action!")

        # Update the post
        UserPostModel.updateUserPost(upid, post)
    
        # Get saved post
        user_post = UserPostModel.getUserPost(upid, getCurrentUid())

        return user_post 

    @login_required
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument("upid", type=int, location="args", required=True)

        args = parser.parse_args()
        upid = args["upid"]
        
        user_post = UserPostModel.getUserPost(upid, getCurrentUid())

        if not user_post:
            abort(404, message = "There is no such a user post!")

        if user_post["uid"] is not getCurrentUid():
            abort(401, message = "Unauthorized action!")

        UserPostModel.removeUserPost(upid)
        
        return {
            "message" : "The post was removed!"
        }

api.add_resource(UserPosts, '/api/user-posts')
