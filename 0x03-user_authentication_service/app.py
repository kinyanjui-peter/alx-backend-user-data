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
def register_users():
    """Endpoint to register a user"""
    try:
        email = request.form.get('email')
        password = request.form.get('password')  # Corrected to lowercase 'password'
        
        # Check if user exists in the database
        existing_user = AUTH._db.find_user_by(email=email)
        
        # If user is not registered
        if existing_user is None:
            # Register the user
            new_user = AUTH.register_user(email=email, password=password)  # Corrected 'password'
            # Return success message
            return jsonify(email=new_user.email, message="user created"), 201

        # If user is already registered
        return jsonify(message="email already registered"), 400
    
    except Exception as e:
        return jsonify(message="User could not be registered"), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")