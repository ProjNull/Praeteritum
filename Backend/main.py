""" May the spaghetti begin """


from flask import jsonify, Flask, request, session, json
from flask_socketio import SocketIO

from database import func
from database import Session
from models import Users

from werkzeug.security import generate_password_hash, check_password_hash

from functools import wraps

from datetime import datetime, timedelta

import jwt

SECRET_KEY = "Praeteritum-CHANGE-ME-TO-SOMETHING-RANDOM"

api = Flask(__name__)
api.secret_key = SECRET_KEY

socketio = SocketIO(api)

socketio.init_app(api, cors_allowed_origins="*")

session_instance = Session()


def commit_data():
    """
    Commit sample user data to the database.
    """
    name = "pes"
    email = "email@email.email"
    password = "passwordE"

    usr = Users(Name=name, Password=password, Email=email)

    session_instance.add(usr)
    session_instance.commit()


commit_data()

from werkzeug.exceptions import HTTPException


@api.errorhandler(HTTPException)
def handle_exception(e):
    """
    Handle HTTP exceptions by returning JSON responses.

    :param e: The HTTPException to handle.
    """
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
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
def token_required(f):
    """
    Decorator function for verifying JWT tokens.

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
                session_instance.query(Users).filter_by(User_ID=data["User_ID"]).first()
            )
        except Exception as e:
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
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")

        if username and password:
            q = session_instance.query(Users).filter_by(Email=email).first()
            if not q:
                usr = Users(Name=username, Password=generate_password_hash(password), Email=email)
                session_instance.add(usr)
                session_instance.commit()

                return jsonify("Data is now in DB!")
            return jsonify("Data does not match")
        else:
            return jsonify("Please fill out all fields.")
    # If not POST
    return jsonify("This endpoint only supports POST requests for registration.")


@api.route("/login", methods=["POST"])
def login():
    """
    Handle user login via a POST request.

    :return: JSON response containing a JWT token on successful login.
    """
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user_obj = session_instance.query(Users).filter_by(Email=email).first()

        if user_obj and check_password_hash(user_obj.Password, password):
            session_instance.close()

            return jsonify({"token": generateToken(user_obj.User_ID)})
        else:
            session_instance.close()
            return "Wrong name or password"
    else:
        return jsonify("Method was not POST")


@api.route("/securedPing")
@token_required
def ping(current_user):
    """
    A secured route that requires a valid JWT token for access.

    :param current_user: The user context provided by the token_required decorator.
    :return: JSON response indicating the user who provided the token.
    """
    return jsonify("A valid token provided by " + current_user.Name)


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
