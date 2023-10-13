from flask import jsonify, Flask, session

api = Flask(__name__)
api.secret_key = "Praeteritum"

session_instance = session()

if __name__ == "__main__":
    api.run(host="0.0.0.0", port=8002)