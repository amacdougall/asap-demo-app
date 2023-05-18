import os
from pymongo import MongoClient
from bson.binary import UuidRepresentation

MONGODB_URI = os.environ.get("MONGODB_URI")

mongo_client = MongoClient(MONGODB_URI,
                           connectTimeoutMS=30000,
                           uuidRepresentation='standard')

db = mongo_client["member-api"]

# Insert a member into the database. Returns the database id of the inserted
# record.
def insert_member(member):
    result = db.members.insert_one(member)
    return result.inserted_id

# Find a member by an arbitrary property, supplied as a dict. Returns the
# member, or None.
#
# Example: find_member_by({"member_id": uuid.uuid5(...)})
def find_member_by(query):
    return db.members.find_one(query)
