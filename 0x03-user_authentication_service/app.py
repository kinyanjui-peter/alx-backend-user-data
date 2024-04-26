#!/usr/bin/env python3
""" flask app """
from flask import Flask, jsonify
from auth import Auth
# flask instance
app = Flask(__name__)

AUTH = Auth()
# root for root URL ("/")
@app.route('/')
def Get_payload():
    """a function that returns a json message"""
    return jsonify('message: Bienvenue')

@app.route('/users/', methods=['POST'])
def register_users():
    """endpoint to register a user"""
    try:
        email = extract.form.get('email')
        password = extract.form.get('Password')
        
        # check if user exist inthe database
        existing_user = AUTH._db.find_user_by(email=email)
        
        # if user unregistered
        if existing_user is None:
            # register user
            new_user = AUTH.register_user(email=email, password=Password)
            # return success message
            return jsonify(email=email, message="user created"), 200

        # if user is registered already   
        return jsonify(message="email already registered"), 400
    
    except Exception as e:
        return jsonify(message="User could not be registered"), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
