#!/usr/bin/env python3
""" Basic flask app
"""
from flask import Flask, request, jsonify, abort
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
