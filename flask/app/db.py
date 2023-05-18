import os
import uuid
import json
from datetime import datetime
from pymongo import MongoClient
from bson.binary import UuidRepresentation

MONGODB_URI = os.environ.get("MONGODB_URI")

client = MongoClient(MONGODB_URI,
                     connectTimeoutMS=30000,
                     uuidRepresentation='standard')
db = client["member-api"]

class MemberAlreadyExistsError(Exception):
    pass

def create_member(first_name=None, last_name=None, dob=None, country=None):
    member = {
        "first_name": first_name,
        "last_name": last_name,
        "dob": dob,
        "country": country
    }

    # build UUIDv5 from hash of JSON string of member variable
    member_id = uuid.uuid5(uuid.NAMESPACE_DNS, json.dumps(member))

    if member_is_valid(member_id):
        raise MemberAlreadyExistsError

    member["member_id"] = member_id
    # MongoDB converts datetime objects to ISODate objects
    member["dob"] = datetime.strptime(dob, "%m/%d/%Y")
    document = db.members.insert_one(member)
    return str(member_id)

# Given a UUID object, return True if a member with that id exists.
def member_is_valid(member_id):
    member = db.members.find_one({"member_id": member_id})
    return member is not None
