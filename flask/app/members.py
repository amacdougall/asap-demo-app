import json
import uuid
from datetime import datetime
import db

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

    db.insert_member(member)

    return str(member_id)

# Given a UUID object, return True if a member with that id exists.
def member_is_valid(member_id):
    member = db.find_member_by({"member_id": member_id})
    return member is not None
