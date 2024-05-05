Copy code
#!/usr/bin/env python3
""" Module of Users views
"""
import os
from api.v1.views import app_views
from models.user import User
from flask import jsonify, request, abort


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_auth():
    """Login endpoint to authenticate user and create session.

    Returns:
        JSON response:
            - User object JSON if login successful
            - Error messages and status codes for invalid credentials
    """
    # Retrieve email and password from form data
    email = request.form.get('email')
    password = request.form.get('password')

    # Validate email and password
    if email is None or email == '':
        return jsonify({"error": "email missing"}), 400
    if password is None or password == '':
        return jsonify({"error": "password missing"}), 400

    # Search for users with matching email
    users = User.search({"email": email})
    if not users or users == []:
        return jsonify({"error": "no user found for this email"}), 404

    # Check password validity for each matching user
    for user in users:
        if user.is_valid_password(password):
            # Create session and set session cookie
            from api.v1.app import auth
            session_id = auth.create_session(user.id)
            resp = jsonify(user.to_json())
            session_name = os.getenv('SESSION_NAME', 'session_id')
            resp.set_cookie(session_name, session_id)
            return resp

    # Return error for invalid password
    return jsonify({"error": "wrong password"}), 401


@app_views.route('/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def logout():
    """Logout endpoint to destroy user session.

    Returns:
        Empty JSON response with 200 status if logout successful,
        404 error if session cannot be destroyed
    """
    # Attempt to destroy session
    from api.v1.app import auth
    if auth.destroy_session(request):
        return jsonify({}), 200
    abort(404)  # Session not found
