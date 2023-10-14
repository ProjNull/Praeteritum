""" May the spaghetti begin """
from datetime import datetime, timedelta
from functools import wraps

import jwt
from database import Session, func
from flask import Flask, json, jsonify, request, session
from flask_socketio import SocketIO
from models import Groups, Permissions, Users
from werkzeug.exceptions import HTTPException
from werkzeug.security import check_password_hash, generate_password_hash

SECRET_KEY = "Praeteritum-CHANGE-ME-TO-SOMETHING-RANDOM"

api = Flask(__name__)
api.secret_key = SECRET_KEY

socketio = SocketIO(api)
socketio.init_app(api, cors_allowed_origins="*")

session_instance = Session()


@api.errorhandler(HTTPException)
def handle_exception(e):
    """
    Handle HTTP exceptions by returning JSON responses.

    :param e: The HTTPException to handle.
    """
    response = e.get_response()
    response.data = json.dumps(
        {
            "code": e.code,
            "name": e.name,
            "description": e.description,
        }
    )
    response.content_type = "application/json"
    return response


@api.after_request
def add_header(response):
    """
    Add an Access-Control-Allow-Origin header to the response.

    :param response: The Flask response object.
    """
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


def generate_jwt(payload):
    """
    Generate a JSON Web Token (JWT) with the given payload.

    :param payload: The data to include in the JWT payload.
    :return: The generated JWT token.
    """
    try:
        payload["exp"] = datetime.utcnow() + timedelta(days=1)
        payload["iat"] = datetime.utcnow()

        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        return token
    except Exception as e:
        return str(e)


def verify_jwt(token):
    """
    Verify and decode a JSON Web Token (JWT).

    :param token: The JWT token to verify and decode.
    :return: The decoded payload or an error message.
    """
    try:
        # Verify and decode the token
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return "Token has expired."
    except jwt.InvalidTokenError as e:
        return str(e)


def generateToken(ID):
    """
    Generate a JWT token with a user's ID as the payload.

    :param ID: The User_ID to include in the JWT payload.
    :return: The generated JWT token.
    """
    return generate_jwt(
        {
            "User_ID": ID,
        }
    )


# decorator for verifying the JWT
def requires_authorization(f):
    """
    Decorator function for verifying JWT tokens.
    Requires your function to have a variable of type Users as the first argument.

    :param f: The function to decorate.
    :return: The decorated function.
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            # return 401 if token is not passed
        if not token:
            return jsonify({"message": "Token wasn't provided"}), 401

        try:
            # decoding the payload to fetch the stored details
            data = verify_jwt(token)
            current_user = (
                session_instance.query(Users).filter_by(
                    User_ID=data["User_ID"]).first()
            )
        except:
            return (
                jsonify({"message": "Token evaluation unsuccessfull"}),
                401,
            )
        # returns the current logged in users context to the routes
        return f(current_user, *args, **kwargs)

    return decorated


@api.route("/register", methods=["POST"])
def register():
    """
    Handle user registration via a POST request.

    :return: JSON response indicating the registration status.
    """
    if request.method == "POST":
        name = request.json.get("displayname")
        password = request.json.get("password")
        email = request.json.get("email")

        if email and password:
            if not name:
                name = email.split("@")[0]
            q = session_instance.query(Users).filter_by(Email=email).first()
            if not q:
                usr = Users(
                    Name=name,
                    Password=password,  # generate_password_hash(password),
                    Email=email,
                )
                session_instance.add(usr)
                session_instance.commit()

                return jsonify(
                    {"User_ID": usr.User_ID, "message": "Registration successfull!"}
                )
            return jsonify({"message": "Email already taken!"})
        else:
            return jsonify(
                {
                    "message": "Missing one or more of the required fields!",
                    "required_fields": ["displayname", "password", "email"],
                }
            )
    # If not POST
    return jsonify(
        {"message": "This endpoint only supports POST requests for registration."}
    )


@api.route("/login", methods=["POST"])
def login():
    """
    Handle user login via a POST request.

    :return: JSON response containing a JWT token on successful login.
    """
    if request.method == "POST":
        email = request.json["email"]
        password = request.json["password"]

        user_obj = session_instance.query(Users).filter_by(Email=email).first()

        if (
            user_obj and password == user_obj.Password
        ):  # check_password_hash(user_obj.Password, password):
            session_instance.close()

            return jsonify(
                {
                    "token": generate_jwt({"User_ID": user_obj.User_ID}),
                    "message": "Sign in successfull",
                }
            )
        else:
            session_instance.close()
            return jsonify({"message": "Incorrect email or password!"})
    else:
        return jsonify(
            {"message": "This endpoint only supports POST requests for registration."}
        )


@api.route("/permission/get/", methods=["POST"])
def perm_get():
    if request.method == "POST":
        permid = request.json.get("permid")
        if not permid:
            return jsonify(
                {
                    "message": "You must provide the required fields!",
                    "required_fields": ["permid"],
                }
            )
        p = session_instance.query(Permissions).filter_by(
            Permission_ID=permid).first()
        if not p:
            return jsonify({"message": "A permission with this ID does not exist!"})
        return jsonify(
            {
                "message": "Found a permission entry!",
                "userid": p.User_ID,
                "groupid": p.Group_ID,
                "level": p.Permission_Level,
            }
        )
    else:
        return jsonify(
            {"message": "This endpoint only supports POST requests for registration."}
        )


@api.route("/permission/create/", methods=["POST"])
def perm_create():
    if request.method == "POST":
        userid = request.json.get("userid")
        groupid = request.json.get("groupid")
        level = request.json.get("level")
        if None in [userid, groupid, level]:
            return jsonify(
                {
                    "message": "You must provide the required fields!",
                    "required_fields": ["userid", "groupid", "level"],
                }
            )
        if level >= 3 or level < 0:
            return jsonify({"message": "Level must be in the interval <0;3)"})
        q_link_exists = (
            session_instance.query(Permissions)
            .filter_by(User_ID=userid, Group_ID=groupid)
            .first()
        )
        if q_link_exists:
            return jsonify(
                {
                    "message": "This user is already linked to the specified group! Use update instead!"
                }
            )
        r = Permissions(Permission_Level=level,
                        Group_ID=groupid, User_ID=userid)
        session_instance.add(r)
        session_instance.commit()
        return jsonify(
            {"message": "Created a new permission link", "permid": r.Permission_ID}
        )
    else:
        return jsonify(
            {"message": "This endpoint only supports POST requests for registration."}
        )


@api.route("/permission/delete/", methods=["POST"])
def perm_delete():
    if request.method == "POST":
        permid = request.json.get("permid")
        if not permid:
            return jsonify(
                {
                    "message": "You must provide the required fields!",
                    "required_fields": ["permid"],
                }
            )
        q = session_instance.query(Permissions).filter_by(
            Permission_ID=permid).first()
        if not q:
            return jsonify({"message": "Permission link with this ID does not exist"})
        session_instance.delete(q)
        return jsonify({"message": "Permission link destroyed"})
    else:
        return jsonify(
            {"message": "This endpoint only supports POST requests for registration."}
        )


@api.route("/permission/update/", methods=["POST"])
def perm_update():
    if request.method == "POST":
        permid = request.json.get("permid")
        level = request.json.get("level")
        if None in [permid, level]:
            return jsonify(
                {
                    "message": "You must provide the required fields!",
                    "required_fields": ["permid", "level"],
                }
            )
        if level >= 3 or level < 0:
            return jsonify({"message": "Level must be in the interval <0;3)"})
        q = session_instance.query(Permissions).filter_by(
            Permission_ID=permid).first()
        if not q:
            return jsonify({"message": "Permission link with this ID does not exist"})
        q.Permission_Level = level
        session_instance.add(q)
        session_instance.commit()
        return jsonify(
            {"message": "Permission link updated with the new permission level."}
        )
    else:
        return jsonify(
            {"message": "This endpoint only supports POST requests for registration."}
        )


@api.route("/permission/users_in", methods=["POST"])
def perm_group_users():
    if request.method == "POST":
        groupid = request.json.get("groupid")
        limit = request.json.get("limit")
        offset = request.json.get("offset", 0)
        if None in [groupid, limit, offset]:
            return jsonify(
                {
                    "message": "You must provide the required fields!",
                    "required_fields": ["groupid", "limit", "offset"],
                }
            )
        q = [
            i.User_ID
            for i in (
                session_instance.query(Permissions)
                .filter_by(Group_ID=groupid)
                .limit(limit)
                .offset(offset * limit)
            )
        ]
        if not q:
            return jsonify({"message": "This group does not have any users in it"})
        return jsonify(
            {
                "message": f"Found all users ({limit} per page, page {offset+1}) in the specified group",
                "users": q,
            }
        )
    else:
        return jsonify(
            {"message": "This endpoint only supports POST requests for registration."}
        )


@api.route("/permission/groups_of", methods=["POST"])
def perm_user_groups():
    if request.method == "POST":
        userid = request.json.get("userid")
        limit = request.json.get("limit")
        offset = request.json.get("offset", 0)
        if None in [userid, limit, offset]:
            return jsonify(
                {
                    "message": "You must provide the required fields!",
                    "required_fields": ["userid", "limit", "offset"],
                }
            )
        q = [
            i.User_ID
            for i in (
                session_instance.query(Permissions)
                .filter_by(User_ID=userid)
                .limit(limit)
                .offset(offset * limit)
            )
        ]
        if not q:
            return jsonify({"message": "This user is not in any groups"})
        return jsonify(
            {
                "message": f"Found all groups ({limit} per page, page {offset+1}) for the specified user",
                "groups": q,
            }
        )
    else:
        return jsonify(
            {"message": "This endpoint only supports POST requests for registration."}
        )


@api.route("/addGroup", methods=["post"])
def addGroup():
    if request.method == "POST":
        Group_Name = request.json["Group_Name"]
        Description = request.json["Description"]

        GroupToCommit = Groups(Group_Name=Group_Name, Description=Description)
        session_instance.add(GroupToCommit)

        session_instance.commit()
        return jsonify("Group created")
    return jsonify("Wrong request")


@api.route("/removeGroup", methods=["DELETE"])
@requires_authorization
def removeGroup(u: Users):
    if request.method == "DELETE":
        groupToDelete = request.json.get("Group_ID")
        perms = session_instance.query(Permissions).filter_by(
            User_ID=u.User_ID, Group_ID=groupToDelete, Permissions_Level=3
        )
        if not perms:
            return jsonify("Fuck off")
        group_obj = session_instance.query(
            Groups).filter_by(Group_ID=groupToDelete)
        session_instance.delete(group_obj)
        session_instance.commit()
        return jsonify("Group deleted")
    return jsonify("Wrong request")


@api.route("/listGroups", methods=["GET"])
def listGroups():
    if request.method == "GET":
        group_obj = session_instance.query(Groups).all()
        groups = [[group.Group_ID, group.Group_Name] for group in group_obj]
        return groups


@socketio.on("my_event")
def handle_my_event(data):
    """
    Handle a socket.io event.

    :param data: Data received from the client.
    """
    print("Data received from the client:", data)
    message = "fuck you"
    socketio.emit("my_response", {"data": f"Received: {message}"})


if __name__ == "__main__":
    socketio.run(api, debug=True, host="0.0.0.0", port="8002")
