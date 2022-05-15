from models import Post
from mongoengine import connect
from flask import Flask, request, jsonify, make_response
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


@app.route("/get_post/<postId>")
def get_post(postId):
    '''
    Fetches post with the postId in the path , return this post.
    '''
    try:
        post = json.loads(Post.objects(postId=postId).first().to_json())
        return {"result": "success", "post": post}, 200
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
@app.route("/edit_post/<postId>", methods=["PUT"])
def edit_post(postId):
    '''
    Fetches post with the postId in the path , return the updated post.
    '''
    prev_post = Post.objects(postId=postId).first()

    prev_post.userId = int(request.get_json().get(os.getenv("USER_ID")))
    prev_post.title = request.get_json().get(os.getenv("TITLE"))
    prev_post.body = request.get_json().get(os.getenv("BODY"))
    try:
        prev_post.save()
        return {"result": "success", "message": f'This post with postId = {postId} updated'}, 200
    except Exception as e:
        return {"result": "error", "message": f"{e}"}, 500


# TODO: Create Delete Post Endpoint
@app.route('/delete_post/<postId>', methods=['DELETE'])
def delete_post(postId):
    '''
    Fetches post with the postId in the path , return the deleted postId.
    '''
    get_post = Post.objects(postId=postId)
    try:
        get_post.delete()
        return {"result": "success", "message": f'This post with postId = {postId} deleted'}, 200
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


if __name__ == "__main__":
    app.run(debug=True, host=os.getenv("HOST"), port=int(os.getenv("PORT")))
