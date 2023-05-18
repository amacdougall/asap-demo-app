import os
import json
import uuid
from datetime import datetime

from pymongo import MongoClient
from bson.binary import UuidRepresentation
import redis

MEMBER_CACHE_TIMEOUT = 30 # in seconds

MONGODB_URI = os.environ.get("MONGODB_URI")
REDIS_HOST = os.environ.get("REDIS_HOST")

mongo_client = MongoClient(MONGODB_URI,
                           connectTimeoutMS=30000,
                           uuidRepresentation='standard')

r = redis.Redis(host=REDIS_HOST, port=6379, db=0)

db = mongo_client["member-api"]

# Insert a member into the database. Returns the database id of the inserted
# record.
def insert_member(member):
    result = db.members.insert_one(member)
    return result.inserted_id

# Find a member by member_id. Returns the member record, or None.
# Caches results for MEMBER_CACHE_TIMEOUT seconds.
def find_member(member_id):
    cached_member = find_cached_member(member_id)
    if cached_member == 'invalid':
        return None
    elif cached_member is not None:
        return cached_member
    else:
        member = db.members.find_one({"member_id": member_id})
        cache_member(member_id, member)
        return member

# Stores a member in cache by member_id. If member is None, stores the special
# string 'invalid'.
def cache_member(member_id, member):
    if member is None:
        r.set(str(member_id), 'invalid', MEMBER_CACHE_TIMEOUT)
    else:
        r.set(str(member["member_id"]),
              member_to_json(member),
              MEMBER_CACHE_TIMEOUT)

def find_cached_member(member_id):
    return json_to_member(r.get(str(member_id)))

# Converts member to a JSON string, serializing member_id and dob.
def member_to_json(member):
    return json.dumps({
        "member_id": str(member["member_id"]),
        "first_name": member["first_name"],
        "last_name": member["last_name"],
        "dob": datetime.strftime(member["dob"], "%m/%d/%Y"),
        "country": member["country"]
    })

def json_to_member(json_value):
    if json_value is None:
        return None
    elif json_value == 'invalid':
        return json_value
    member = json.loads(json_value)
    member["member_id"] = uuid.UUID(member["member_id"])
    member["dob"] = datetime.strptime(member["dob"], "%m/%d/%Y")
    return member
