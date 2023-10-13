""" May the spaghetti begin """
from flask import jsonify, Flask, request, session, json
from database import func
from models import Users
from database import Session
from flask_socketio import SocketIO
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from datetime import datetime, timedelta

api = Flask(__name__)
api.secret_key = "Praeteritum"

socketio = SocketIO(api)

socketio.init_app(
    api,
    cors_allowed_origins="*"
)
    
session_instance = Session()

def commit_data():
    name = "pes"
    email = "email@email.email"
    password = "passwordE"

    usr = Users(
            Name=name,
            Password=password,
            Email = email
        )
    
    session_instance.add(usr)
    session_instance.commit()
commit_data()

from werkzeug.exceptions import HTTPException

@api.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response

@api.after_request
def add_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

def generateToken(ID):
    Token = jwt.encode({
        'User_ID': ID,
        'exp' : datetime.utcnow() + timedelta(hours = 2)
    }, api.config['SECRET_KEY'])
    return Token

# decorator for verifying the JWT
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
            # return 401 if token is not passed
        if not token:
            return jsonify({'message' : 'Token is missing !!'}), 401

        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, api.secret_key)
            current_user = Users.query.filter_by(User_ID = data['User_ID']).first()
        except:
            return jsonify({
            'message' : 'Token is invalid !!'
        }),             401
        # returns the current logged in users context to the routes
        return f(current_user, *args, **kwargs)

    return decorated

@api.route("/register", methods=["POST"])
def register():
    """
    Handle user registration.

    This function handles user registration by processing POST requests and checking the provided data.
    It ensures that all required fields are filled, the username is not already in the database,
    and that the provided password and password confirmation match before storing the data in the database.

    Args:
        None

    Returns:
        If the registration is successful, it returns a JSON response indicating that the data is stored in the database.
        If the provided data does not match the criteria, it returns a JSON response indicating a mismatch or missing fields.
        If the endpoint is accessed using a non-POST request, it returns a JSON response indicating that only POST requests are supported.
    """
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')

        if username and password:
            if username not in Users:
                usr = Users(
                    Name=username,
                    Password=password,
                    Email = email
                )
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
    Handle user login.

    This function handles user login by checking the provided username and password against a database.
    If the login is successful, it stores the username in a session.

    Args:
        None

    Returns:
        If the login is successful, it returns an empty JSON response.
        If the login fails, it returns a string message indicating that the name or password is incorrect.
    """
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        user_obj = session_instance.query(Users).filter_by(Name=username).first()

        if user_obj and user_obj.Password == password:  
            session["username"] = username
            session_instance.close()

            return jsonify({
                "token": generateToken(user_obj.User_ID)
            })
        else:
            session_instance.close()
            return "Wrong name or password"
    else:
        return jsonify("Method was not POST")

@api.route("/securedPing")
@token_required
def ping():
    return jsonify("I love men")

@socketio.on('my_event')
def handle_my_event(data):
    print("Data received from the client:", data)
    message = "fuck you"
    socketio.emit('my_response', {'data': f'Received: {message}'})


if __name__ == "__main__":
    socketio.run(api, debug=True, host="172.21.112.249", port="8002")