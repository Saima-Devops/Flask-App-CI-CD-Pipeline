import pytest
import mongomock
from bson.objectid import ObjectId
from flask_pymongo import PyMongo

# ✅ Patch MongoClient BEFORE importing app
import flask_pymongo

flask_pymongo.pymongo.MongoClient = mongomock.MongoClient

from app import app, mongo


@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["MONGO_URI"] = "mongodb://localhost:27017/testdb"

    client = app.test_client()

    # Setup test data
    with app.app_context():
        mongo.db.students.delete_many({})
        mongo.db.students.insert_one({
            "_id": ObjectId("66fddff25f4b5f6a0a123456"),
            "name": "Test Student",
            "email": "test@student.com",
            "course": "Flask"
        })

    yield client

    # Cleanup
    with app.app_context():
        mongo.db.students.delete_many({})