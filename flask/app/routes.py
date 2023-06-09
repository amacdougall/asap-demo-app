import pymongo
import uuid
from flask import Blueprint, render_template, request, jsonify
from members import create_member, member_is_valid, MemberAlreadyExistsError

route_blueprint = Blueprint('route_blueprint', __name__)

@route_blueprint.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@route_blueprint.route("/hello_world", methods=["POST"])
def hello_world():
    # echo request JSON body
    return jsonify(request.json)

@route_blueprint.route("/member_id", methods=["POST"])
def member_id():
    try:
        # splat request JSON body into create_member function
        member_id = create_member(**request.json)
        if member_id:
            return jsonify({"member_id": member_id})
        else:
            return jsonify({"error": "Could not create member due to an unknown error"}), 500
    except MemberAlreadyExistsError:
        return jsonify({"error": "Member with this id already exists"}), 409
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except pymongo.errors.OperationFailure as e:
        return jsonify({
            "error": "Could not create member due to error: " + str(e)
        }), 500

@route_blueprint.route("/member_id/validate", methods=["GET", "POST"])
def validate_member_id():
    if request.method == "GET":
        return render_template("validate_member_id.html")
    else:
        member_id = request.form.get("member_id")
        errors = []
        if not member_id:
            errors.append("Missing member_id")

        try:
            member_id = uuid.UUID(member_id)
        except ValueError:
            errors.append("Invalid member_id format")

        if member_is_valid(member_id):
            return render_template("member_id_valid.html")
        else:
            errors.append("Member with this id does not exist")

        return render_template("member_is_invalid.html", errors=errors)
