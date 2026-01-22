from flask import Flask, request, jsonify, render_template_string, redirect, url_for
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

# ---------------- API ENDPOINTS ----------------

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")

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

@app.route("/profile/<username>")
def profile(username):
    users = load_users()

    if username not in users:
        return jsonify({"error": "User not found"}), 404

    return jsonify({"username": username, "status": "active"})

# ---------------- GUI PAGES ----------------

HOME_HTML = """
<h2>Authentication Service</h2>
<ul>
  <li><a href="/register-ui">Register</a></li>
  <li><a href="/login-ui">Login</a></li>
</ul>
"""

REGISTER_HTML = """
<h2>Register</h2>
<form method="post">
  Username: <input name="username" required><br><br>
  Password: <input type="password" name="password" required><br><br>
  <button type="submit">Register</button>
</form>
<p>{{msg}}</p>
<a href="/">Back</a>
"""

LOGIN_HTML = """
<h2>Login</h2>
<form method="post">
  Username: <input name="username" required><br><br>
  Password: <input type="password" name="password" required><br><br>
  <button type="submit">Login</button>
</form>
<p>{{msg}}</p>
<a href="/">Back</a>
"""

@app.route("/")
def home():
    return render_template_string(HOME_HTML)

@app.route("/register-ui", methods=["GET", "POST"])
def register_ui():
    msg = ""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        users = load_users()

        if username in users:
            msg = "User already exists"
        else:
            users[username] = password
            save_users(users)
            msg = "User registered successfully"

    return render_template_string(REGISTER_HTML, msg=msg)

@app.route("/login-ui", methods=["GET", "POST"])
def login_ui():
    msg = ""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        users = load_users()

        if users.get(username) == password:
            msg = "Login successful"
        else:
            msg = "Invalid credentials"

    return render_template_string(LOGIN_HTML, msg=msg)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
