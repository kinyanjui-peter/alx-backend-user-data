#!/usr/bin/env python3
""" Flask app """
from flask import Flask, jsonify, request
from auth import Auth

# Flask instance
app = Flask(__name__)

# Instantiate Auth object
AUTH = Auth()


@app.route('/')
def Get_payload():
    """Endpoint for the root URL ("/")"""
    return jsonify(message="Bienvenue")


@app.route('/users/', methods=['POST'])
def users() -> str:
    """Endpoint to register a user"""
    try:
        email = request.form.get('email')
        password = request.form.get('password')
        # Corrected to lowercase 'password'

        # Check if user exists in the database
        existing_user = AUTH._db.find_user_by(email=email)

        # If user is not registered
        if existing_user is None:
            # Register the user
            new_user = AUTH.register_user(email=email, password=password)
            # Corrected 'password'
            # Return success message
            return jsonify(email=new_user.email, message="user created"), 201

        # If user is already registered
        return jsonify(message="email already registered"), 400

    except Exception as e:
        return jsonify(message="User could not be registered"), 500


@app.route('/sessions', methods=['POST'])
def login() -> str:
    """_summary_

    Returns:
        str: _description_
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not (AUTH.valid_login(email, password)):
        abort(401)
    else:
        # create a new session
        session_id = AUTH.create_session(email)
        response = jsonify({"email": email, "message": "logged in"})
        response.set_cookie('session_id', session_id)

    return response


@app.route('/sessions', methods=['DELETE'])
def logout() -> str:
    """_summary_
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect('/')


@app.route('/profile', methods=['GET'])
def profile() -> str:
    """_summary_
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": user.email}), 200
    else:
        abort(403)


@app.route('/reset_password', methods=['POST'])
def get_reset_password_token() -> str:
    """_summary_

    Returns:
        str: _description_
    """
    email = request.form.get('email')
    try:
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": reset_token}), 200
    except Exception:
        abort(403)


@app.route('/reset_password', methods=['PUT'])
def update_password() -> str:
    """_summary_

    Returns:
        str: _description_
    """
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')
    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"}), 200
    except Exception:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
