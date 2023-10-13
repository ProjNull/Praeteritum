from flask import jsonify, Flask, session, request

api = Flask(__name__)
api.secret_key = "Praeteritum"

DB = [] # TODO: Make DB

@api.route("/", methods=["GET", "POST"])
def root():
    testEndpoint = ["hello", "world!"]
    return jsonify(testEndpoint)

@api.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        passwordCheck = request.form.get('passwordCheck')
        
        if username and password and passwordCheck:
            if username not in DB and password == passwordCheck:
                # TODO: Commit data to DB
                return jsonify("Data is now in DB!")
            return jsonify("Data does not match")
        else:
            return jsonify("Please fill out all fields.")
    
    # If not POST
    return jsonify("This endpoint only supports POST requests for registration.")


if __name__ == "__main__":
    api.run(host="0.0.0.0", port=8002)