from flask import request, jsonify, Blueprint
from flask_jwt_extended import get_jwt_identity, set_access_cookies, get_jwt, unset_jwt_cookies
from datetime import datetime, timedelta
from app.models.auth_user import AuthUser


auth_blueprint = Blueprint("auth", __name__)


@auth_blueprint.after_app_request
def refresh(response):
    """Check JWT status. If token expiration imminent, refresh token."""
    try:
        expiry = get_jwt()["exp"]
        now = datetime.now()
        timestamp = datetime.timestamp(now + timedelta(seconds=8))
        if timestamp > expiry:
            access_token = AuthUser.refresh_jwt_token(get_jwt_identity)
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        return response


@auth_blueprint.route("/api/auth/register", methods=["POST"])
def register():
    """Register a new auth user"""

    data = request.json
    try:
        email = data["email"]
        password = data["password"]

        user = AuthUser(email=email, password=password)

        db_insertion_attempt = user.add_user()
        if db_insertion_attempt:
            token = user.create_jwt_token()

            success_msg = "Registration successful"
            resp = jsonify(msg=success_msg, status=201)
            set_access_cookies(resp, token)

            return resp, 201
        else:
            error_msg = "Something went wrong."
            return jsonify(msg=error_msg, status=400), 400
    except KeyError:
        error_msg = "Please provide both an email and a password."
        return jsonify(msg=error_msg, status=400), 400


@auth_blueprint.route("/api/auth/login", methods=["POST"])
def login():
    """Logs an authenticated user into the API."""

    data = request.json
    try:
        email = data["email"]
        password = data["password"]

        user = AuthUser(email, password)
        retrieved_auth_user = user.get_user(password)

        if isinstance(retrieved_auth_user, AuthUser):
            token = user.create_jwt_token()
            success_msg = "Login successful."
            resp = jsonify(msg=success_msg, status=200)

            set_access_cookies(resp, token)
            return resp, 200
        elif retrieved_auth_user == "not found":
            error_msg = "Email not found. Please try again."
            return jsonify(msg=error_msg, status=400)

        else:
            error_msg = "Incorrect password. Please try again."
            return jsonify(msg=error_msg, status=400)

    except KeyError:
        error_msg = "Please provide both an email and a password."
        return jsonify(msg=error_msg, status=400)
