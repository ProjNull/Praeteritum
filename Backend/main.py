""" May the spaghetti begin """
from datetime import datetime, timedelta
from functools import wraps

import jwt
from database import Session, func
from flask import Flask, json, jsonify, request, session
from flask_socketio import SocketIO
from models import Users, Groups, Boards, Permissions, Questions, Feedback, Reaction
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
    response.headers["Access-Control-Allow-Headers"] = "content-type"
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
                    Password=generate_password_hash(password),
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

        if user_obj and check_password_hash(user_obj.Password, password):
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


@api.route("/addGroup", methods=["post"])
def addGroup():
    if request.method == "POST":
        GroupName = request.json["GroupName"]
        Description = request.json["Description"]

        Group_obj = session_instance.query(Groups).filter_by(GroupName=GroupName)

        if GroupName not in Group_obj:
            GroupToCommit = Groups(
                GroupName=GroupName, 
                Description=Description
            )
            session_instance.add(GroupToCommit)
            return jsonify("Group created")
        return jsonify("You shouldn't get this response")
    return jsonify("Wrong request")


@api.route("/removeGroup", methods=["DELETE"])
@requires_authorization
def removeGroup(u: Users):
    if request.method == "DELETE":
        groupToDelete = request.json.get("Group_ID")
        perms = session_instance.query(Permissions).filter_by(User_ID=u.User_ID, Group_ID=groupToDelete, Permissions_Level=3)
        if not perms:
            return jsonify("Fuck off")
        group_obj = session_instance.query(Groups).filter_by(Group_ID=groupToDelete)
        session_instance.delete(group_obj)
        return jsonify("Group deleted")
    return jsonify("Wrong request")


@api.route("/listGroups", methods=["GET"])
def listGroups():
    if request.method == "GET":
        group_obj = session_instance.query(Groups).all()
        i = []
        for group in group_obj.filter_by(Group_ID=group):
            item = [group.Group_ID, group.Group_Name]
            i.append(item)
        return i


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
