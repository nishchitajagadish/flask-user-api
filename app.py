from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory storage
users = {}
next_id = 1

# Get all users
@app.route("/users", methods=["GET"])
def get_users():
    return jsonify(users), 200

# Get single user
@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = users.get(user_id)
    if user:
        return jsonify(user), 200
    return jsonify({"error": "User not found"}), 404

# Add new user
@app.route("/users", methods=["POST"])
def add_user():
    global next_id
    data = request.json
    if not data or "name" not in data:
        return jsonify({"error": "Name is required"}), 400
    users[next_id] = {"id": next_id, "name": data["name"]}
    next_id += 1
    return jsonify(users[next_id - 1]), 201

# Update user
@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.json
    if user_id in users:
        users[user_id]["name"] = data.get("name", users[user_id]["name"])
        return jsonify(users[user_id]), 200
    return jsonify({"error": "User not found"}), 404

# Delete user
@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    if user_id in users:
        deleted = users.pop(user_id)
        return jsonify(deleted), 200
    return jsonify({"error": "User not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
