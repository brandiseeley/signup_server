from flask import Flask, request, abort
from flask_cors import CORS

import random
import time
import os

app = Flask(__name__)
CORS(app, origins='*', methods=['GET', 'POST'], allow_headers=["Content-Type"])

users = {
    "admin": {"email": "admin@someplace.com"},
    "elphaba": {"email": "elphaba@thropp.com"},
    "glinda": {"email": "the@good.com"},
    "oz": {"email": "hoax@emeraldcity.com"},
}

emails = [data['email'] for data in users.values()]


def is_valid_password(password):
    if len(password) < 8:
        return False
    if not any(char.isdigit() for char in password):
        return False
    if not any(char.isupper() for char in password):
        return False
    return True

@app.route('/')
def index():
    with open("templates/index.html", "r") as file:
        return file.read()


@app.route('/user_exists')
def user_exists():
    time.sleep(0.8)
    username = request.args.get('username')
    if username is None:
        return {"error": "Missing 'username' parameter"}, 400
    
    exists = username in users
    return { "username": username, "exists": exists }


@app.route('/user_exists_unreliable')
def user_exists_unreliable():
    time.sleep(0.5)
    random_value = random.random()
    
    if random_value < 0.5:
        abort(500)
    
    return user_exists()


@app.route('/email_registered')
def email_exists():
    time.sleep(0.5)
    email = request.args.get('email')
    if email is None:
        return {"error": "Missing 'email' parameter"}, 400
    
    exists = email in emails
    return { "email": email, "exists": exists }


@app.route('/valid_password', methods=['POST'])
def valid_password():
    time.sleep(0.4)
    data = request.get_json()
    password = data.get('password')

    if is_valid_password(password):
        return {"valid": True, "message": "Password is valid."}
    else:
        return {"valid": False, "message": "Password does not meet criteria."}


if __name__ == '__main__':
    if os.environ.get('FLASK_ENV') == 'production':
            app.run(debug=False)
        else:
            app.run(debug=True, port=5003)