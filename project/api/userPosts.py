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

user_post_comment_fields{
    "isLiked" : fields.Boolean,
    "likeNumber" : fields.Integer,
    "upcid" : fields.Integer,
    "upid" : fields.Integer,
    "comment" : fields.String,
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

class PreviousFollowingPosts(Resource):
    @login_required
    @marshal_with(user_post_fields)
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("upid", type=int, location="args", required=True)

        args = parser.parse_args()
        upid = args["upid"]

        posts = UserPostModel.getPreviousFollowingPosts(getCurrentUid(), upid, 10)

        return posts

class NewFollowingPosts(Resource):
    @login_required
    @marshal_with(user_post_fields)
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("upid", type=int, location="args", required=True)

        args = parser.parse_args()
        upid = args["upid"]  

        posts = UserPostModel.getNewFollowingPosts(getCurrentUid(), upid)

        return posts

class NewFollowingPostNumber(Resource):
    @login_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("upid", type=int, location="args", required=True)

        args = parser.parse_args()
        upid = args["upid"]

        number = UserPostModel.getNewFollowingPostNumber(getCurrentUid(), upid)

        return {
            "number" : number
        }

class UserPostLikes(Resource):
    @login_required
    def post(self, upid):
        UserPostModel.likeUserPost(getCurrentUid(), upid)

        return {
            "result" : "success"
        }

    @login_required
    def delete(self, upid):
        UserPostModel.unlikeUserPost(getCurrentUid(), upid)

        return {
            "result" : "success"
        }

class UserPostLikeNumber(Resource):
    def get(self, upid):
        number = UserPostModel.getUserPostLikeNumber(upid)

        return {
            "number" : number
        }

class UserPostComments(Resource):
    @marshal_with(user_post_comment_fields)
    def get(self, upid):
        parser = reqparse.RequestParser()
        parser.add_argument("upcid", type=int, location="args", required=True)

        args = parser.parse_args()
        upcid = args["upcid"]

        if not upcid:
            comments = UserPostModel.getLastUserPostComments(upid, 2, getCurrentUid())
        else:
            comments = UserPostModel.getPreviousUserPostComments(upid, upcid, 2, getCurrentUid())

        return comments

    @login_required
    @marshal_with(user_post_comment_fields)
    def post(self, upid):
        parser = reqparse.RequestParser()
        parser.add_argument("comment", type=str, location="json", required=True)

        args = parser.parse_args()
        comment = args["comment"]

        upcid = UserPostModel.addUserPostComment(getCurrentUid(), upid, comment)

        # Get the saved comment
        saved_comment = UserPostModel.getUserPostComment(upcid, getCurrentId())

        return saved_comment
    
    @login_required
    @marshal_with(user_post_comment_fields)
    def put(self, upid):
        parser = reqparse.RequestParser()
        parser.add_argument("upcid", type=int, location="json", required=True)
        parser.add_argument("comment", type=str, location="json", required=True)

        args = parser.parse_args()
        
        # Get the comment
        comment = UserPostModel.getUserPostComment(args["upcid"])

        if not comment:
            abort(404, message = "There is no such a comment!")
        
        if comment["uid"] is not getCurrentUid():
            abort(401, message = "Unauthorized action!")
        
        # Update the comment
        UserPostModel.updateUserPostComment(upcid, args["comment"])

        # Get updated comment
        updated_comment = UserPostModel.getUserPostComment(upcid, getCurrentUid())

        return updated_comment
    
    @login_required
    def delete(self, upid):
        parser = reqparse.RequestParser()
        parser.add_argument("upcid", type=int, location="args", required=True)

        args = parser.parse_args()

        # Get the comment
        comment = UserPostModel.getUserPostComment(args["upcid"])

        if not comment:
            abort(404, message = "There is no such a comment!")
        
        if comment["uid"] is not getCurrentUid():
            abort(401, message = "Unauthorized action!")
        
        # Delete the comment
        UserPostModel.removeUserPostComment(upcid)

        return {
            "result" : "success"
        }

class UserPostCommentNumber(Resource):
    def get(self, upid):
        number = UserPostModel.getUserPostCommentNumber(upid)

        return {
            "number" : number
        }

class UserPostCommentLikes(Resource):
    @login_required
    def post(self, upcid):
        # Get the comment
        comment = UserPostModel.getUserPostComment(upcid, getCurrentUid())

        if not comment:
            abort(404, message = "There is no such a comment!")

        UserPostModel.likeUserPostComment(getCurrentUid(), upcid)

        return {
            "result" : "success"
        }

    @login_required
    def delete(self, upcid):
        # Get the comment
        comment = UserPostModel.getUserPostComment(upcid, getCurrentUid())

        if not comment:
            abort(404, message = "There is no such a comment!")
            
        UserPostModel.unlikeUserPostComment(getCurrentUid(), upcid)

        return {
            "result" : "success"
        }

class UserPostCommentLikeNumber(Resource):
    def get(self, upcid):
        # Get the number
        number = UserPostModel.getUserPostCommentLikeNumber(upcid)

        return {
            "number" : number
        }

api.add_resource(UserPosts, "/api/user-posts")
api.add_resource(PreviousFollowingPosts, "/api/user-posts/previous-following")
api.add_resource(NewFollowingPosts, "/api/user-posts/new-following")
api.add_resource(NewFollowingPostNumber, "/api/user-posts/new-following/number")
api.add_resource(UserPostLikes, "/api/user-posts/<upid>/likes")
api.add_resource(UserPostLikeNumber, "/api/user-posts/<upid>/likes/number")
api.add_resource(UserPostComments, "/api/user-posts/<upid>/comments")
api.add_resource(UserPostCommentNumber, "/api/user-posts/<upid>/comments/number")
api.add_resource(UserPostCommentLikes, "/api/user-posts/comments/<upcid>/likes")
api.add_resource(UserPostCommentLikeNumber, "/api/user-posts/comments/<upcid>/likes/number")