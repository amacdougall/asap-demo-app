import json
import uuid
from datetime import datetime
import db

class MemberAlreadyExistsError(Exception):
    pass

# Creates a member by inserting it into the database. Generates a member_id
# UUIDv5 from the hash of the JSON string of the member object, so that the same
# member will always have the same member_id.
#
# Returns the member_id of the inserted member.
#
# Raises ValueError if any of the required properties are missing.
# Raises MemberAlreadyExistsError if the member already exists.
#
def create_member(first_name=None, last_name=None, dob=None, country=None):
    missing_properties = []

    if first_name is None:
        missing_properties.append("first_name")
    if last_name is None:
        missing_properties.append("last_name")
    if dob is None:
        missing_properties.append("dob")
    if country is None:
        missing_properties.append("country")

    if missing_properties:
        raise ValueError("Missing properties: {}".format(missing_properties))

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

    # use UUID and datetime objects instead of strings; trust the data layer to
    # store these values
    member["member_id"] = member_id
    member["dob"] = datetime.strptime(dob, "%m/%d/%Y")

    db.insert_member(member)

    return str(member_id)

# Given a UUID object, return True if a member with that id exists.
def member_is_valid(member_id):
    member = db.find_member(member_id)
    return member is not None
