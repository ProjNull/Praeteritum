from flask import Blueprint, request

example = Blueprint("Example API", __name__)

@example.route("/", methods=["GET", "POST"])
def example_route():
    return {"method": request.method, "message": "OK!"}

