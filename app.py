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
    try:
        posts = json.loads(Post.objects().exclude("id").to_json())
        return {"result": "success", "count": len(posts), "posts": posts}, 200
    except Exception as e:
        return {"result": "error", "message": f"{e}"}, 500


@app.route("/get_post/<postId>")
def get_post(postId):
    return json.loads(Post.objects(postId=postId).first().to_json())


@app.route("/get_posts/<userId>")
def get_posts_by_user(userId):
    posts = json.loads(Post.objects(userId=userId).exclude("id").to_json())
    return {"count": len(posts), "posts": posts}


# TODO: Create Edit Post Endpint
@app.route("/edit_post/<postId>", methods=["PUT"])
def edit_post(postId):
    prev_post = Post.objects(postId=postId).first()

    prev_post.userId = int(request.get_json().get("userId"))
    prev_post.title = request.get_json().get("title")
    prev_post.body = request.get_json().get("body")
    prev_post.save()
    return {"result": "success", "message": f'This post with postId = {postId} updated'}


# TODO: Create Delete Post Endpoint
@app.route('/delete_post/<postId>', methods=['DELETE'])
def delete_post(postId):
    get_post = Post.objects(postId=postId)
    get_post.delete()
    return {"result": "success", "message": f'This post with postId = {postId} deleted'}


# TODO: Create Add Post
@app.route("/add_post", methods=["POST"])
def add_post():
    newPost = Post()
    newPost.userId = int(request.get_json().get("userId"))
    newPost.postId = int(request.get_json().get("postId"))
    newPost.title = request.get_json().get("title")
    newPost.body = request.get_json().get("body")
    newPost.save()
    return f'new post with postId = {newPost.postId} created'


if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=5000)
