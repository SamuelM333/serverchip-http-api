from bson import ObjectId
from flask_mongoengine import MongoEngine
from flask_security import UserMixin

# from mongoengine import Document, EmbeddedDocument

db = MongoEngine()


class Port(db.EmbeddedDocument):
    number = db.IntField(required=True)
    state = db.BooleanField(required=True)


class Hour(db.EmbeddedDocument):
    start = db.StringField(max_length=60, required=True)  # TODO Regex here
    end = db.StringField(max_length=60, required=True)  # TODO Regex here


class DayHour(db.EmbeddedDocument):
    hour = db.EmbeddedDocumentField(Hour)
    days = db.StringField(max_length=60, required=True)


class Condition(db.EmbeddedDocument):
    name = db.StringField(required=True)
    day_hour = db.EmbeddedDocumentField(DayHour)
    input_port = db.EmbeddedDocumentField(Port)


class User(db.Document, UserMixin):
    _id = db.ObjectIdField(primary_key=True, default=lambda: ObjectId())
    name = db.StringField(max_length=120, required=True)
    last_name = db.StringField(max_length=120)
    email = db.EmailField(unique=True, required=True)
    password = db.StringField(min_length=8, max_length=255, required=True)
    role = db.StringField(max_length=120, required=True)
    _etag = db.StringField(max_length=120, required=True)
    created = db.DateTimeField()
    _updated = db.DateTimeField()


class Microchip(db.Document):
    _id = db.ObjectIdField(primary_key=True, default=lambda: ObjectId())
    name = db.StringField(max_length=60, required=True)
    description = db.StringField(max_length=120)
    ip = db.StringField(max_length=120, required=True)  # TODO Regex here
    owner = db.ObjectIdField(required=True, db_field='user')
    _etag = db.StringField(max_length=120, required=True)
    created = db.DateTimeField()
    _updated = db.DateTimeField()


class Task(db.Document):
    _id = db.ObjectIdField(primary_key=True, default=lambda: ObjectId())
    name = db.StringField(max_length=60)
    description = db.StringField(max_length=120)
    microchip = db.ObjectIdField(required=True)  # db_field?
    output_port = db.EmbeddedDocumentField(Port)
    conditions = db.EmbeddedDocumentListField(Condition)
    _etag = db.StringField(max_length=120, required=True)
    created = db.DateTimeField()
    _updated = db.DateTimeField()
