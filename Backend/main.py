""" May the spaghetti begin """
from datetime import datetime, timedelta
from functools import wraps

import jwt
from database import Session, func
from flask import Flask, json, jsonify, request, session
from flask_socketio import SocketIO
from models import Boards
from models import Feedback as Feedbacks
from models import Groups, Permissions, Questions, Reaction, Users
from werkzeug.exceptions import HTTPException
from werkzeug.security import check_password_hash, generate_password_hash

SECRET_KEY = "Praeteritum-CHANGE-ME-TO-SOMETHING-RANDOM"


api = Flask(__name__)
api.secret_key = SECRET_KEY


socketio = SocketIO(api)
socketio.init_app(api, cors_allowed_origins="*")


session_instance = Session()


def make_dummy_data():
    q = session_instance.query(Users).filter_by(
        Email="admin@example.com").first()
    if q:
        return
    u1 = Users(Name="Admin Admin", Email="admin@example.com",
               Password="adminadmin")
    u2 = Users(Name="Script Inane",
               Email="script@example.com", Password="script")
    session_instance.add(u1)
    session_instance.add(u2)
    g1 = Groups(Group_Name="Class 2.I", Description="2023/2024")
    session_instance.add(g1)
    session_instance.commit()
    p1 = Permissions(Permission_Level=3, User_ID=u1.User_ID,
                     Group_ID=g1.Group_ID)
    p2 = Permissions(Permission_Level=1, User_ID=u2.User_ID,
                     Group_ID=g1.Group_ID)
    session_instance.add(p1)
    session_instance.add(p2)
    b1 = Boards(
        BoardName="Example",
        Group_ID=g1.Group_ID,
        Phase=0,
        RevealPosts=True,
        isLocked=False,
        isVotingLocked=False,
    )
    b2 = Boards(
        BoardName="My Board",
        Group_ID=g1.Group_ID,
        Phase=0,
        RevealPosts=True,
        isLocked=False,
        isVotingLocked=False,
    )
    b3 = Boards(
        BoardName="Another board",
        Group_ID=g1.Group_ID,
        Phase=0,
        RevealPosts=True,
        isLocked=False,
        isVotingLocked=False,
    )
    b4 = Boards(
        BoardName="and yet another board",
        Group_ID=g1.Group_ID,
        Phase=0,
        RevealPosts=True,
        isLocked=False,
        isVotingLocked=False,
    )
    session_instance.add(b1)
    session_instance.add(b2)
    session_instance.add(b3)
    session_instance.add(b4)
    session_instance.commit()
    q1 = Questions(
        Content="How do you rate your experience?",
        Columns="Positive,Negative",
        Board_ID=b1.Board_ID,
    )
    q2 = Questions(
        Content="Another example question",
        Columns="Positive,Neutral,Negative",
        Board_ID=b1.Board_ID,
        Mandantory=True
    )
    session_instance.add(q1)
    session_instance.add(q2)
    session_instance.commit()


make_dummy_data()


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
    response.headers["Access-Control-Allow-Headers"] = "content-type, authorization"
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
    return jsonify({"message": "This endpoint only supports POST requests!"})


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
        return jsonify({"message": "This endpoint only supports POST requests!"})


@api.route("/permission/get/", methods=["POST"])
def perm_get():
    """
    Retrieve permission information via a POST request.

    This function allows you to retrieve permission details based on the provided permission ID.

    :return: JSON response containing permission details if found, or an error message if the permission does not exist.
    """
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
        return jsonify({"message": "This endpoint only supports POST requests!"})


@api.route("/permission/create/", methods=["POST"])
def perm_create():
    """
    Create a new permission link via a POST request.

    This function allows you to create a new permission link, associating a user with a group and specifying the permission level.

    :return: JSON response indicating the status of the permission link creation or an error message if the operation fails.
    """
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
        return jsonify({"message": "This endpoint only supports POST requests!"})


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
        return jsonify({"message": "This endpoint only supports POST requests!"})


@api.route("/permission/update/", methods=["POST"])
def perm_update():
    """
    Delete a permission link via a POST request.

    This function allows you to delete an existing permission link based on the provided permission ID.

    :return: JSON response indicating the status of the permission link deletion or an error message if the operation fails.
    """
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
        return jsonify({"message": "This endpoint only supports POST requests!"})


@api.route("/permission/users_in", methods=["POST"])
def perm_group_users():
    """
    Retrieve users in a specific group via a POST request.

    This function allows you to retrieve a list of users in a specified group with optional pagination.

    :return: JSON response containing the list of users in the group, or an error message if the group has no users or if the operation fails.
    """
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
        return jsonify({"message": "This endpoint only supports POST requests!"})


@api.route("/permission/groups_of", methods=["POST"])
def perm_user_groups():
    """
    Retrieve groups associated with a specific user via a POST request.

    This function allows you to retrieve a list of groups that a specified user belongs to with optional pagination.

    :return: JSON response containing the list of groups associated with the user, or an error message if the user is not in any groups or if the operation fails.
    """
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
        return jsonify({"message": "This endpoint only supports POST requests!"})


@api.route("/addGroup", methods=["post"])
def addGroup():
    """
    Create a new group via a POST request.

    This function allows you to create a new group by providing a group name and a description.

    :return: JSON response indicating the status of the group creation or an error message if the operation fails.
    """
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
    """
    Remove a group via a DELETE request.

    This function allows authorized users to delete an existing group based on the provided Group_ID. To be authorized,
    the user must have permission level 3 (typically indicating administrative privileges) for the group.

    :param u: The authorized user with appropriate permissions.
    :return: JSON response indicating the status of the group removal or an error message if the operation fails or if the user lacks the necessary permissions.
    """
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


@api.route("/listGroups", methods=["POST"])
def listGroups():
    """
    Retrieve a list of groups via a POST request.

    This function allows you to retrieve a list of all available groups.

    :return: JSON response containing a list of groups, where each group is represented as a list containing its Group_ID and Group_Name.
    """
    if request.method == "POST":
        group_obj = session_instance.query(Groups).all()
        groups = [
            {"id": group.Group_ID, "name": group.Group_Name, "desc": group.Description}
            for group in group_obj
        ]
        return groups


@api.route("/createBoard", methods=["POST"])
def board_create():
    if request.method == "POST":
        boardname = request.json.get("BoardName")
        description = request.json.get("Description")
        Group_ID = request.json.get("Group_ID")
        RevealPosts = request.json.get("Anon", False)
        if None in [boardname, description, Group_ID]:
            return jsonify(
                {
                    "message": "You must provide the required fields!",
                    "required_fields": ["BoardName", "Description", "Group_ID"],
                }
            )
        b = Boards(
            BoardName=boardname,
            Description=description,
            Group_ID=Group_ID,
            Phase=0,
            RevealPosts=RevealPosts,
            isLocked=False,
        )
        session_instance.add(b)
        session_instance.commit()
        return jsonify({"message": "Board created", "boardid": b.Board_ID})
    else:
        return jsonify({"message": "This endpoint only supports POST requests!"})


@api.route("/deleteBoard", methods=["POST"])
def board_delete():
    if request.method == "POST":
        board_id = request.json.get("Board_ID")
        if not board_id:
            return jsonify(
                {
                    "message": "You must provide the required fields!",
                    "required_fields": ["Board_ID"],
                }
            )
        b = session_instance.query(Boards).filter_by(Board_ID=board_id).first()
        if not b:
            return jsonify({"message": "A board with this ID does not exist!"})
        session_instance.delete(b)
        session_instance.commit()
        return jsonify({"message": "Board deleted"})
    else:
        return jsonify({"message": "This endpoint only supports POST requests!"})


@api.route("/getBoard", methods=["POST"])
def board_get():
    if request.method == "POST":
        board_id = request.json.get("Board_ID")
        if not board_id:
            return jsonify(
                {
                    "message": "You must provide the required fields!",
                    "required_fields": ["Board_ID"],
                }
            )
        b = session_instance.query(Boards).filter_by(Board_ID=board_id).first()
        if not b:
            return jsonify({"message": "A board with this ID does not exist!"})
        return jsonify(
            {
                "message": "Board found!",
                "name": b.BoardName,
                "description": b.Description,
                "group": b.Group_ID,
                "phase": b.Phase,
                "revealPosts": b.RevealPosts,
                "isLocked": b.isLocked,
                "isVotingLocked": b.isVotingLocked,
            }
        )
    else:
        return jsonify({"message": "This endpoint only supports POST requests!"})


@api.route("/fetchBoards", methods=["POST"])
def board_fetch_many():
    if request.method == "POST":
        group_id = request.json.get("Group_ID")
        phase = request.json.get("Phase", 0)
        if None in [group_id, phase]:
            return jsonify(
                {
                    "message": "You must provide the required fields!",
                    "required_fields": ["Group_ID", "Phase"],
                }
            )
        b = (
            session_instance.query(Boards)
            .filter_by(Group_ID=group_id, Phase=phase)
            .all()
        )
        if not b:
            return jsonify({"message": "There are no boards in this group!"})
        boards = [
            {"id": bIns.Board_ID, "name": bIns.BoardName, "group": bIns.Group_ID}
            for bIns in b
        ]
        return jsonify({"message": f"{len(boards)} boards fetched!", "boards": boards})
    else:
        return jsonify({"message": "This endpoint only supports POST requests!"})


@api.route("/changePhase", methods=["POST"])
@requires_authorization
def changePhase(u: Users):
    """
    Change the phase of a board via a POST request.

    This function allows authorized users to change the phase of a board based on the provided Board_ID.
    It ensures that the user can't set the phase to the same phase, and that the new phase is 1, 2, or 3.

    :param u: The authorized user with appropriate permissions.
    :return: JSON response indicating the status of the phase change or an error message if the operation fails or if the user lacks the necessary permissions.
    """
    data = request.get_json()

    if "board_id" not in data or "new_phase" not in data:
        return (
            jsonify(
                {"error": "Missing 'board_id' or 'new_phase' in the request data."}
            ),
            400,
        )

    board_id = data["board_id"]
    new_phase = data["new_phase"]

    # Check if the board exists
    board = session_instance.query(Boards).filter(
        Boards.Board_ID == board_id).first()

    if board is None:
        return jsonify({"error": f"Board with ID {board_id} not found."}), 404

    # Check if the user has the required permissions for this group
    permissions = (
        session_instance.query(Permissions)
        .filter(
            Permissions.User_ID == u.User_ID,
            Permissions.Group_ID == board.Group_ID,
            Permissions.Permission_Level >= 2,  # Modify this level as needed
        )
        .first()
    )

    if not permissions:
        return (
            jsonify(
                {
                    "error": "You don't have the necessary permissions to change the phase of this board."
                }
            ),
            403,
        )

    # Verify that the new phase is different from the current phase
    if board.Phase == new_phase:
        return (
            jsonify({"error": "The new phase is the same as the current phase."}),
            400,
        )

    # Ensure that the new phase is 1, 2, or 3
    if new_phase not in [1, 2, 3]:
        return jsonify({"error": "Invalid phase. Phase must be 1, 2, or 3."}), 400

    # Update the board's phase
    board.Phase = new_phase
    session_instance.commit()

    return jsonify({"message": "Board phase changed successfully."}), 200


@api.route("/togglePostVisibility", methods=["POST"])
@requires_authorization
def togglePostVisibility(u: Users):
    """
    Toggle post visibility for a board via a POST request.

    This function allows authorized users (admin or manager) to toggle the visibility of posts for a board based on the provided Board_ID.

    :param u: The authorized user with appropriate permissions.
    :return: JSON response indicating the status of the post visibility toggle or an error message if the operation fails or if the user lacks the necessary permissions.
    """
    data = request.get_json()

    if "board_id" not in data:
        return jsonify({"error": "Missing 'board_id' in the request data."}), 400

    board_id = data["board_id"]

    # Check if the board exists
    board = session_instance.query(Boards).filter(
        Boards.Board_ID == board_id).first()

    if board is None:
        return jsonify({"error": f"Board with ID {board_id} not found."}), 404

    # Check if the user has the required permissions for this group
    permissions = (
        session_instance.query(Permissions)
        .filter(
            Permissions.User_ID == u.User_ID,
            Permissions.Group_ID == board.Group_ID,
            Permissions.Permission_Level >= 2,  # Modify this level as needed
        )
        .first()
    )

    if not permissions:
        return (
            jsonify(
                {
                    "error": "You don't have the necessary permissions to toggle post visibility for this board."
                }
            ),
            403,
        )

    # Toggle post visibility
    board.RevealPosts = not board.RevealPosts
    session_instance.commit()

    return (
        jsonify(
            {"message": f"Post visibility for board {board_id} has been toggled."}),
        200,
    )


@api.route("/getPostVisibility", methods=["POST"])
def getPostVisibility():
    """
    Retrieve the post visibility status for a board via a POST request.

    This function allows users to retrieve the current post visibility status for a board based on the provided Board_ID.

    :return: JSON response containing the current post visibility status for the board or an error message if the board is not found.
    """
    board_id = request.args.get("board_id")

    if not board_id:
        return jsonify({"error": "Missing 'board_id' in the query parameters."}), 400

    # Check if the board exists
    board = session_instance.query(Boards).filter(
        Boards.Board_ID == board_id).first()

    if board is None:
        return jsonify({"error": f"Board with ID {board_id} not found."}), 404

    return jsonify({"reveal_posts": board.RevealPosts}), 200


@api.route("/toggleBoardLock", methods=["POST"])
@requires_authorization
def toggleBoardLock(u: Users):
    """
    Toggle board locking for a board via a POST request.

    This function allows authorized users (admin or manager) to toggle the locking of a board based on the provided Board_ID.

    :param u: The authorized user with appropriate permissions.
    :return: JSON response indicating the status of the board locking toggle or an error message if the operation fails or if the user lacks the necessary permissions.
    """
    data = request.get_json()

    if "board_id" not in data:
        return jsonify({"error": "Missing 'board_id' in the request data."}), 400

    board_id = data["board_id"]

    # Check if the board exists
    board = session_instance.query(Boards).filter(
        Boards.Board_ID == board_id).first()

    if board is None:
        return jsonify({"error": f"Board with ID {board_id} not found."}), 404

    # Check if the user has the required permissions for this group
    permissions = (
        session_instance.query(Permissions)
        .filter(
            Permissions.User_ID == u.User_ID,
            Permissions.Group_ID == board.Group_ID,
            Permissions.Permission_Level >= 2,  # Modify this level as needed
        )
        .first()
    )

    if not permissions:
        return (
            jsonify(
                {
                    "error": "You don't have the necessary permissions to toggle board locking for this board."
                }
            ),
            403,
        )

    # Toggle board locking
    board.isLocked = not board.isLocked
    session_instance.commit()

    return (
        jsonify({"message": f"Board locking for board {board_id} has been toggled."}),
        200,
    )


@api.route("/getBoardLockStatus", methods=["POST"])
def getBoardLockStatus():
    """
    Retrieve the board locking status for a board via a POST request.

    This function allows users to retrieve the current board locking status for a board based on the provided Board_ID.

    :return: JSON response containing the current board locking status for the board or an error message if the board is not found.
    """
    board_id = request.args.get("board_id")

    if not board_id:
        return jsonify({"error": "Missing 'board_id' in the query parameters."}), 400

    # Check if the board exists
    board = session_instance.query(Boards).filter(
        Boards.Board_ID == board_id).first()

    if board is None:
        return jsonify({"error": f"Board with ID {board_id} not found."}), 404

    return jsonify({"is_locked": board.isLocked}), 200


@api.route("/toggleVotingLock", methods=["POST"])
@requires_authorization
def toggleVotingLock(u: Users):
    """
    Toggle voting locking for a board via a POST request.

    This function allows authorized users (admin or manager) to toggle the locking of voting on a board based on the provided Board_ID.

    :param u: The authorized user with appropriate permissions.
    :return: JSON response indicating the status of the voting locking toggle or an error message if the operation fails or if the user lacks the necessary permissions.
    """
    data = request.get_json()

    if "board_id" not in data:
        return jsonify({"error": "Missing 'board_id' in the request data."}), 400

    board_id = data["board_id"]

    # Check if the board exists
    board = session_instance.query(Boards).filter(
        Boards.Board_ID == board_id).first()

    if board is None:
        return jsonify({"error": f"Board with ID {board_id} not found."}), 404

    # Check if the user has the required permissions for this group
    permissions = (
        session_instance.query(Permissions)
        .filter(
            Permissions.User_ID == u.User_ID,
            Permissions.Group_ID == board.Group_ID,
            Permissions.Permission_Level >= 2,  # Modify this level as needed
        )
        .first()
    )

    if not permissions:
        return (
            jsonify(
                {
                    "error": "You don't have the necessary permissions to toggle voting locking for this board."
                }
            ),
            403,
        )

    # Toggle voting locking
    board.isVotingLocked = not board.isVotingLocked
    session_instance.commit()

    return (
        jsonify(
            {"message": f"Voting locking for board {board_id} has been toggled."}),
        200,
    )


@api.route("/getVotingLockStatus", methods=["POST"])
def getVotingLockStatus():
    """
    Retrieve the voting locking status for a board via a POST request.

    This function allows users to retrieve the current voting locking status for a board based on the provided Board_ID.

    :return: JSON response containing the current voting locking status for the board or an error message if the board is not found.
    """
    board_id = request.args.get("board_id")

    if not board_id:
        return jsonify({"error": "Missing 'board_id' in the query parameters."}), 400

    # Check if the board exists
    board = session_instance.query(Boards).filter(
        Boards.Board_ID == board_id).first()

    if board is None:
        return jsonify({"error": f"Board with ID {board_id} not found."}), 404

    return jsonify({"is_voting_locked": board.isVotingLocked}), 200


@api.route("/sendFeedback", methods=["POST"])
@requires_authorization
def send_feedback(u: Users):
    """
    WARNING: This does not verify,
    whether the user has access to the board,
    to which the question belongs.
    """
    if request.method == "POST":
        content = request.json.get("Content")
        column = request.json.get("ColumnName")
        question_id = request.json.get("Question_ID")
        if None in [content, column, question_id]:
            return jsonify(
                {
                    "message": "You must provide the required fields!",
                    "required_fields": ["Content", "ColumnName", "Question_ID"],
                }
            )
        f = Feedbacks(
            User_ID=u.User_ID,
            Questions_ID=question_id,
            Content=content,
            ColumnName=column,
        )
        session_instance.add(f)
        session_instance.commit()
        return jsonify({"message": "Feedback created", "feedbackid": f.Feedback_ID})
    else:
        return jsonify({"message": "This endpoint only supports POST requests!"})


@api.route("/updateFeedback", methods=["POST"])
@requires_authorization
def update_feedback(u: Users):
    """
    WARNING: This does not verify,
    whether the user has access to
    modify the feedback.
    """
    if request.method == "POST":
        fid = request.json.get("Feedback_ID")
        content = request.json.get("Content")
        column = request.json.get("ColumnName")
        question_id = request.json.get("Question_ID")
        f = session_instance.query(Feedbacks).filter_by(Feedback_ID=fid)
        if not f:
            return jsonify({"message": "There is no such feedback!"})
        if question_id:
            f.Questions_ID = question_id
        if content:
            f.Content = content
        if column:
            f.ColumnName = column
        session_instance.add(f)
        session_instance.commit()
        return jsonify({"message": "Feedback created", "feedbackid": f.Feedback_ID})
    else:
        return jsonify({"message": "This endpoint only supports POST requests!"})


@api.route("/getFeedback", methods=["POST"])
@requires_authorization
def get_feedback(u: Users):
    if request.method == "POST":
        fid = request.json.get("Feedback_ID")
        f = session_instance.query(Feedbacks).filter_by(
            Feedback_ID=fid).first()
        if not f:
            return jsonify({"message": "There is no such feedback!"})
        q = (
            session_instance.query(Questions)
            .filter_by(Question_ID=f.Question_ID)
            .first()
        )
        if not q:
            return jsonify(
                {"message": "There is no such question - Invalid feedback entry!"}
            )
        b = session_instance.query(Boards).filter_by(
            Board_ID=q.Board_ID).first()
        if not b:
            return jsonify(
                {
                    "message": "There is no such board - Invalid feedback and question entries!"
                }
            )
        return jsonify(
            {
                "message": "Found the specified feedback",
                "content": f.Content,
                "column": f.ColumnName,
                "question_id": f.Questions_ID,
                "author": f.User_ID if b.RevealPosts else None,
            }
        )
    else:
        return jsonify({"message": "This endpoint only supports POST requests!"})


@api.route("/fetchFeedbacks", methods=["POST"])
@requires_authorization
def get_many_feedbacks(u: Users):
    if request.method == "POST":
        question_id = request.json.get("Question_ID")
        if not question_id:
            return jsonify(
                {
                    "message": "You must provide the required fields!",
                    "required_fields": ["Question_ID"],
                }
            )
        f = session_instance.query(Feedbacks).filter_by(
            Question_ID=question_id).all()
        if not f:
            return jsonify({"message": "There are no feedbacks on this board!"})
        feedbacks = [{"id": fIns.Board_ID, "content": fIns.Content}
                     for fIns in f]
        return jsonify(
            {"message": f"{len(feedbacks)} feedbacks fetched!",
             "feedbacks": feedbacks}
        )
    else:
        return jsonify({"message": "This endpoint only supports POST requests!"})


@api.route("/deleteFeedback", methods=["POST"])
@requires_authorization
def delete_feedback(u: Users):
    if request.method == "POST":
        f_id = request.json.get("Feedback_ID")
        if not f_id:
            return jsonify(
                {
                    "message": "You must provide the required fields!",
                    "required_fields": ["Feedback_ID"],
                }
            )
        f = session_instance.query(Feedbacks).filter_by(
            Feedback_ID=f_id).first()
        if not f:
            return jsonify({"message": "There is no such feedback!"})
        session_instance.delete(f)
        session_instance.commit()
        return jsonify({"message": "Feedback deleted!"})
    else:
        return jsonify({"message": "This endpoint only supports POST requests!"})


@api.route("/upvote", methods=["POST"])
@requires_authorization
def upvote(u: Users):
    if request.method == "POST":
        fid = request.json.get("Feedback_ID")
        if fid:
            rc = (
                session_instance.query(Reaction)
                .filter_by(Feedback_ID=fid, User_ID=u.User_ID)
                .first()
            )
            if rc:
                return jsonify(
                    {
                        "message": "You have already posted your upvote on the specified feedback"
                    }
                )
            r_obj = Reaction(Feedback_ID=fid, User_ID=u.User_ID)
            session_instance.add(r_obj)
            session_instance.commit()
            return jsonify(
                {"message": "Successfully posted your upvote on the specified feedback"}
            )
        else:
            return jsonify(
                {
                    "message": "You must provide the required fields!",
                    "required_fields": ["Feedback_ID"],
                }
            )
    else:
        return jsonify({"message": "This endpoint only supports POST requests!"})


@api.route("/upvotes_on", methods=["POST"])
def get_votes(u: Users):
    if request.method == "POST":
        fid = request.json.get("Feedback_ID")
        if not fid:
            return jsonify(
                {
                    "message": "You must provide the required fields!",
                    "required_fields": ["Feedback_ID"],
                }
            )
        r = len(session_instance.query(
            Feedbacks).filter_by(Feedback_ID=fid).all())
        return jsonify({"message": f"Fetched upvotes for {fid}", "upvotes": r})
    else:
        return jsonify({"message": "This endpoint only supports POST requests!"})


@api.route("/unupvote", methods=["POST"])
@requires_authorization
def unupvote(u: Users):
    if request.method == "POST":
        fid = request.json.get("Feedback_ID")
        if fid:
            r = (
                session_instance.query(Reaction)
                .filter_by(Feedback_ID=fid, User_ID=u.User_ID)
                .first()
            )
            if not r:
                return jsonify(
                    {"message": "You do not have an upvote on the specified feedback"}
                )
            session_instance.delete(r)
            session_instance.commit()
            return jsonify(
                {"message": "You have voided your upvote on the specified feedback"}
            )
        else:
            return jsonify(
                {
                    "message": "You must provide the required fields!",
                    "required_fields": ["Feedback_ID"],
                }
            )
    else:
        return jsonify({"message": "This endpoint only supports POST requests!"})


@api.route("/profile/<int:userid>", methods=["GET"])
@requires_authorization
def get_profile(userid: int):
    u = session_instance.query(Users).filter_by(User_ID=userid).first()
    if not u:
        return jsonify({"message": "User not found!", "user": None})
    return jsonify(
        {
            "message": "User not found!",
            "user": {
                "userid": u.User_ID,
                "displayname": u.Name,
                "email": u.Email,
            },
        }
    )


@api.route("/question/add/<boardid>", methods=["POST"])
@requires_authorization
def add_question(u: Users, boardid: int):
    b = session_instance.query(Boards).filter_by(Board_ID=boardid).first()
    if not b:
        return {"message": f"Board with the ID {boardid} does not exist."}
    con = request.json.get("content")
    col = request.json.get("columns")
    req = request.json.get("required", False)
    if None in [con, col]:
        return {
            "message": "You must provide the required fields!",
            "required_fields": ["Feedback_ID"],
        }
    q = Questions(Content=con, Columns=col, Mandantory=req, Board_ID=boardid)
    session_instance.add(q)
    session_instance.commit()
    return {"message": f"Created question {q.Questions_ID}", "questionid": q.Questions_ID}


@api.route("/question/remove/<int:questionid>", methods=["POST"])
@requires_authorization
def rm_question(u: Users,questionid: int):
    qq = session_instance.query(Questions).filter_by(
            Questions_ID=questionid
            ).first()
    if not qq:
        return {"message": "Question does not exist!"}
    session_instance.delete(qq)
    session_instance.commit()
    return {"message": "Deleted specified question!"}


@api.route("/questions_for/<int:boardid>", methods=["GET"])
@requires_authorization
def get_questions(u: Users,boardid: int):
    b = session_instance.query(Boards).filter_by(Board_ID=boardid).first()
    if not b:
        return {"message": f"Board with the ID {boardid} does not exist."}
    qq = session_instance.query(Questions).filter_by(Board_ID=boardid).all()
    questions = [
            {
                "text": q.Content,
                "cols": q.Columns.split(","),
                "required": q.Mandantory
             } for q in qq
            ]
    return {
            "message": f"Found all questions for {boardid}",
            "questions": questions
            }


@api.route("/question/<int:n>/for/<int:boardid>", methods=["GET"])
@requires_authorization
def get_question_n(u: Users, n: int, boardid: int):
    b = session_instance.query(Boards).filter_by(Board_ID=boardid).first()
    if not b:
        return {"message": f"Board with the ID {boardid} does not exist."}
    qq = session_instance.query(Questions).filter_by(Board_ID=boardid).all()
    questions = [
            {
                "text": q.Content,
                "cols": q.Columns.split(","),
                "required": q.Mandantory
             } for q in qq
            ]
    return {
            "message": f"Found requested question from {boardid}",
            **questions[n % len(questions)]
            }


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
