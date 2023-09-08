#!/usr/bin/env python3
"""
processes routes for session authentification
"""

from os import getenv
from flask import jsonify, request
from api.v1.views import app_views
from models.user import User

@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_login() -> str:
    """ POST /api/v1/auth/session/login
        JSON body:
        - email
        - password
    Return:
        - User instance based on email
        - 400 if email or password is missing
    """

    user_email = request.form.get('email', None)
    user_password = request.form.get('password', None)

    if user_email is None or user_email == "":
        return jsonify({"error": "email missing"}), 400
    if user_password is None or user_password == "":
        return jsonify({"error": "password missing"}), 400

    is_valid_user = User.search({'email': user_email})

    if not is_valid_user:
        return jsonify({"error": "no user found for this email"}), 404

    user_validated = is_valid_user[0]

    if not user_validated.is_valid_password(user_password):
        return jsonify({"error", "wrong password"}), 401

    from api.v1.app import auth
    session_id = auth.create_session(user_validated.id)
    cookie = getenv('SESSION_NAME')
    user = jsonify(user_validated.to_json())

    user.set_cookie(cookie, session_id)
    return user
