from models import Post, User
from mongoengine import connect
from flask import Flask,  render_template, request, jsonify, make_response
import json
import os
from dotenv import load_dotenv

# loading env vars
load_dotenv()

# importing models

app = Flask(__name__)

# connect to mongodb
db = connect(db=os.getenv("DB_NAME"),
             username=os.getenv("DB_USERNAME"),
             password=os.getenv("DB_PASSWORD"),
             host=os.getenv("DB_HOST"),
             port=int(os.getenv("DB_PORT")))


@app.route("/add_user", methods=["POST"])
def add_user():
    '''
    Create new user with request body , add this user to the database.
    '''
    newUser = User()
    newUser.userId = int(request.get_json().get(os.getenv("USER_ID")))
    newUser.username = str(request.get_json().get(os.getenv("USER_NAME")))
    newUser.password = str(request.get_json().get(os.getenv("PASSWORD")))
    newUser.isAdmin = bool(request.get_json().get(os.getenv("IS_ADMIN")))
    newUser.userEmail = request.get_json().get(os.getenv("USER_EMAIL"))
    try:
        newUser.save()
        return {"result": "success", "message": f'new user with userId = {newUser.userId} created'}, 201
    except Exception as e:
        return {"result": "error", "message": f"{e}"}, 500


@app.route("/get_user/<userId>", methods=["GET"])
def get_user(userId):
    '''
    Fetches user with the id of user in the path , return this user.
    '''
    try:
        user = json.loads(User.objects(userId=userId).first().to_json())
        return {"result": "success", "user": user}, 200
    except Exception as e:
        return {"result": "error", "message": f"{e}"}, 500


@app.route("/get_posts")
def get_posts():
    """
    Fetches all posts from database , return all posts.
    """
    try:
        posts = json.loads(Post.objects().exclude("id").to_json())
        return {"result": "success", "count": len(posts), "posts": posts}, 200
    except Exception as e:
        return {"result": "error", "message": f"{e}"}, 500


@app.route("/get_post", methods=['POST'])
def get_post():
    '''
    Fetches post with the postId in the path , return this post.
    '''
    try:
        data = request.get_json()
        post: Post = Post.objects(
            postId=data[os.getenv("POST_ID")]).exclude("id").first()
        if post.get_userId() == data[os.getenv("USER_ID")]:
            return {"result": "success", "post": json.loads(post.to_json())}, 200
        return {"result": "error", "message": "This user doesn't have access to this post"}, 403
    except Exception as e:
        return {"result": "error", "message": f"{e}"}, 500


@app.route("/get_posts/<userId>")
def get_posts_by_user(userId):
    '''
    Fetches all post with the userId in the path , return all the same userId.
    '''
    try:
        posts = json.loads(Post.objects(userId=userId).exclude("id").to_json())
        return {"result": "error", "count": len(posts), "posts": posts}, 200
    except Exception as e:
        return {"result": "error", "message": f"{e}"}, 500


# TODO: Create Edit Post Endpint
@app.route("/edit_post/<postId>", methods=["PUT", "POST"])
def edit_post(postId):
    '''
    Fetch a post from the user's posts with postId in the path ,
    return the updated post if the post is intended for its real user.
    '''
    data = request.get_json()
    post: Post = Post.objects(postId=data[os.getenv("POST_ID")]).first()
    try:
        if post.get_userId() == data[os.getenv("USER_ID")]:
            post.title = data.get(os.getenv("TITLE"))
            post.body = data.get(os.getenv("BODY"))
            post.save()
            return {"result": "success", "message": f'This post with postId = {postId} for user {post.get_userId()} updated'}, 200
        return {"result": "error", "message": "This user doesn't have access to this post"}, 403
    except Exception as e:
        return {"result": "error", "message": f"{e}"}, 500


# TODO: Create Delete Post Endpoint
@app.route('/delete_post/<postId>', methods=['DELETE'])
def delete_post(postId):
    '''
    Fetch a post from the user's posts with postId in the path ,
    return the deleted post if the post is intended for its real user.
    '''
    data = request.get_json()
    post: Post = Post.objects(postId=data[os.getenv("POST_ID")]).first()
    try:
        if post.get_userId() == data[os.getenv("USER_ID")]:
            post.delete()
            return {"result": "success", "message": f'This post with postId = {postId} for user {post.get_userId()} deleted'}, 200
        return {"result": "error", "message": "This user doesn't have access to this post"}, 403
    except Exception as e:
        return {"result": "error", "message": f"{e}"}, 500


# TODO: Create Add Post
@app.route("/add_post", methods=["POST"])
def add_post():
    '''
    Create new post with request body , add this post to the database.
    '''
    newPost = Post()
    newPost.userId = int(request.get_json().get(os.getenv("USER_ID")))
    newPost.postId = int(request.get_json().get(os.getenv("POST_ID")))
    newPost.title = request.get_json().get(os.getenv("TITLE"))
    newPost.body = request.get_json().get(os.getenv("BODY"))
    try:
        newPost.save()
        return {"result": "success", "message": f'new post with postId = {newPost.postId} created'}, 201
    except Exception as e:
        return {"result": "error", "message": f"{e}"}, 500


@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(code=404, error=str(e)), 404


@app.errorhandler(500)
def resource_not_found(e):
    return jsonify(code=500, error=str(e)), 500


if __name__ == "__main__":
    app.run(debug=True, host=os.getenv("HOST"), port=int(os.getenv("PORT")))
