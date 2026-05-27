from flask import Blueprint, request, jsonify
from models.db import users_collection
from utils.auth import hash_password, check_password, generate_token

auth = Blueprint("auth", __name__)

# Register API
@auth.route("/register", methods=["POST"])
def register():

    try:
        data = request.get_json()

        # Check if data exists
        if not data:
            return jsonify({
                "message": "No input data provided"
            }), 400

        username = data.get("username")
        password = data.get("password")

        # Validate fields
        if not username or not password:
            return jsonify({
                "message": "Username and password are required"
            }), 400

        # Check existing user
        existing_user = users_collection.find_one({
            "username": username
        })

        if existing_user:
            return jsonify({
                "message": "User already exists"
            }), 400

        # Hash password
        hashed_password = hash_password(password)

        # Insert user
        users_collection.insert_one({
            "username": username,
            "password": hashed_password
        })

        return jsonify({
            "message": "User registered successfully"
        }), 201

    except Exception as e:
        return jsonify({
            "message": "Internal server error",
            "error": str(e)
        }), 500


# Login
@auth.route("/login", methods=["POST"])
def login():

    try:

        data = request.get_json()

        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return jsonify({
                "message": "Username and password required"
            }), 400

        user = users_collection.find_one({
            "username": username
        })

        if not user:
            return jsonify({
                "message": "User not found"
            }), 404

        if not check_password(password, user["password"]):
            return jsonify({
                "message": "Invalid password"
            }), 401

        token = generate_token(username)

        return jsonify({
            "message": "Login successful",
            "token": token,
            "username": username
        }), 200

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500