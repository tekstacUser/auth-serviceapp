from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

DATA_FILE = "users.json"

def load_users():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(DATA_FILE, "w") as f:
        json.dump(users, f)

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    users = load_users()

    if username in users:
        return jsonify({"error": "User already exists"}), 400

    users[username] = password
    save_users(users)

    return jsonify({"message": "User registered successfully"})

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    users = load_users()

    if users.get(username) == password:
        return jsonify({"message": "Login successful"})
    else:
        return jsonify({"error": "Invalid credentials"}), 401

@app.route("/profile/<username>", methods=["GET"])
def profile(username):
    users = load_users()

    if username not in users:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "username": username,
        "status": "active"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
