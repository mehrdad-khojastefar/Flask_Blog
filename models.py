from enum import unique
from tkinter.tix import Tree
from mongoengine import Document, IntField, StringField, BooleanField, EmailField
from pkg_resources import require


class Post(Document):

    userId = IntField(require=True)
    postId = IntField(unique=True)
    title = StringField()
    body = StringField()

    def get_userId(self):
        return self.userId


class User(Document):
    username = StringField(require=True)
    password = StringField(require=True)
    userId = IntField(require=True, unique=True)
    userEmail = EmailField(unique=True)
    isAdmin = BooleanField(required=True)
