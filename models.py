from enum import unique
from mongoengine import Document, IntField, StringField


class Post(Document):

    userId = IntField()
    postId = IntField(unique=True)
    title = StringField()
    body = StringField()
