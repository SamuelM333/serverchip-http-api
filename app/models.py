from datetime import datetime

from bson import ObjectId
from flask_mongoengine import MongoEngine
from flask_security import UserMixin

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
    created = db.DateTimeField(default=datetime.utcnow)
    _updated = db.DateTimeField(default=datetime.utcnow)


class Microchip(db.Document):
    _id = db.ObjectIdField(primary_key=True, default=lambda: ObjectId())
    name = db.StringField(max_length=60, required=True)
    description = db.StringField(max_length=120)
    ip = db.StringField(max_length=120, required=True)  # TODO Regex here
    owner = db.ObjectIdField(required=True, db_field='user')
    _etag = db.StringField(max_length=120, required=True)
    created = db.DateTimeField(default=datetime.utcnow)
    _updated = db.DateTimeField(default=datetime.utcnow)


class Task(db.Document):
    _id = db.ObjectIdField(primary_key=True, default=lambda: ObjectId())
    name = db.StringField(max_length=60)
    description = db.StringField(max_length=120)
    microchip = db.ObjectIdField(required=True)
    output_port = db.EmbeddedDocumentField(Port)
    conditions = db.EmbeddedDocumentListField(Condition)
    _etag = db.StringField(max_length=120, required=True)
    created = db.DateTimeField(default=datetime.utcnow)
    _updated = db.DateTimeField(default=datetime.utcnow)


class ReportStatus(db.EmbeddedDocument):
    code = db.StringField(required=True, max_length=60)  # TODO Change to numbers or a code
    reason = db.StringField(required=True, max_length=120)
    user = db.ObjectIdField(required=True)  # TODO Needed?


class ReportDetails(db.EmbeddedDocument):
    task = db.ObjectIdField(required=True)
    status = db.EmbeddedDocumentField(ReportStatus, required=True)


class Report(db.Document):
    microchip = db.ObjectIdField(required=True)
    details = db.EmbeddedDocumentField(ReportDetails, required=True)
    created = db.DateTimeField(default=datetime.utcnow)
    _updated = db.DateTimeField(default=datetime.utcnow)
