#!/usr/bin/env python3
""" Basic flask app
"""
from flask import Flask, request, jsonify, abort, redirect
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'])
def welcomemsg() -> str:
    """ Return a json payload
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=['POST'], strict_slashes=False)
def users():
    """ if a user does not exist, register them
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if email is None or password is None:
        abort(400)

    try:
        user = AUTH.register_user(email=email, password=password)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400
    else:
        return jsonify({
            "email": f"{user.email}",
            "message": "user created"
        }), 200


@app.route("/sessions", methods=['POST'], strict_slashes=False)
def login():
    """ if login is correct create a session for a user,
    else abort 401
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if email is None or password is None:
        abort(400)

    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        response = jsonify({'email': email, 'message': 'logged in'})
        response.set_cookie('session_id', session_id)
        return response
    abort(401)


@app.route("/sessions", methods=['DELETE'], strict_slashes=False)
def logout():
    """Logs user out by destroying session and redirecting
        to get route /
    """
    session_id = request.cookies.get('session_id')
    if session_id is None:
        abort(403)
    user = AUTH.get_user_from_session_id(session_id=session_id)
    if user is None:
        abort(403)

    AUTH.destroy_session(user_id=user.id)
    return redirect('/')


@app.route("/profile", methods=['GET'], strict_slashes=False)
def profile():
    """ Find a user and return their profile details
    """
    session_id = request.cookies.get('session_id')
    if session_id is None:
        abort(403)
    user = AUTH.get_user_from_session_id(session_id=session_id)
    if user is None:
        abort(403)
    return jsonify({'email': user.email}), 200


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token():
    """ Reset the user password """
    email = request.form.get('email')

    if email is None:
        abort(401)

    try:
        reset_token = AUTH.get_reset_password_token(email=email)
    except ValueError:
        abort(403)
    else:
        return jsonify({
            "email": f"{email}",
            "reset_token": f"{reset_token}"
        }), 200


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password():
    """ route to update the user password """
    email = request.form.get('email')
    pwd = request.form.get('new_password')
    reset = request.form.get('reset_token')

    if email is None or pwd is None or reset is None:
        abort(401)
    try:
        AUTH.update_password(reset_token=reset, password=pwd)
    except ValueError:
        abort(403)
    else:
        return jsonify({"email": f"{email}", "message": "Password updated"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
