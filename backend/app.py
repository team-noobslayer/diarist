from datetime import datetime, timedelta
from math import floor
from dotenv import load_dotenv
from cryptography.fernet import Fernet
from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
import bcrypt
import os
load_dotenv()

token_timeout = 24 # timeout period, in hours, for authentication tokens

token_crypto_secret = os.environ.get('SECRET').encode()
crypto = Fernet(token_crypto_secret)

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Optional, silences deprecation warning
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URI')

db = SQLAlchemy(app)

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    token = db.Column(db.BLOB, nullable=False)

class JournalEntry(db.Model):
    entry_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256))
    body = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    last_edited = db.Column(db.DateTime, default=datetime.now(), nullable=False)

# Uncomment the next line to create the required tables in a new database on program execution
# db.create_all()

# Home route
#   GET returns all journal entries by a user
#   POST takes a new journal entry and adds it to database
@app.route("/diarist", methods=['GET', 'POST'], strict_slashes=False)
def home():
    if request.method == 'GET':
        # TODO: authenticate, return list of all journal entries
        return jsonify({
            "route": "/",
            "http-method": "GET"
        })
    elif request.method == 'POST':
        # TODO: authenticate, verify request body, and add
        # journal entry to database
        return request.get_json()
    # else http method is not in methods parameter
    # flasks handles this automatically

# Delete route - deletes journal entry by ID
@app.route("/diarist/delete/<int:id>", methods=['DELETE'])
def delete(id):
    # TODO: authenticate, remove journal entry with provided ID
    return jsonify({
        "route": "/delete/<id>",
        "http-method": "DELETE"
    })

# Edit route - updates a journal entry associated with ID
@app.route("/diarist/edit/<int:id>", methods=['PUT'])
def edit(id):
    # TODO: authenticate, replace journal entry with provided
    #   ID with supplied data
    return jsonify({
        "route": "/edit/<id>",
        "http-method": "PUT"
    })

# Register route - registers a new user; returns auth token
@app.route("/diarist/register", methods=['POST'], strict_slashes=False)
def register():
    request_data = request.get_json()
    try:
        # hash password
        pwd = request_data['password'].encode()
        salt = bcrypt.gensalt()
        hashed_pw = bcrypt.hashpw(pwd, salt)

        # generate auth token
        token = generate_token(request_data['email'])

        # generate user and write to database
        user = User(
            username=request_data['username'], 
            email=request_data['email'], 
            password=hashed_pw, 
            token=token
        )
        db.session.add(user)
        db.session.commit()

        return jsonify({
            "status": "success",
            "token": token.decode()
        }) 
    except:
        abort(400)

# Login route - authenticates user based on supplied username and password; returns auth token
@app.route("/diarist/login", methods=['POST'], strict_slashes=False)
def login():
    request_data = request.get_json()
    try:
        token = authenticate_email_password(request_data['email'], request_data['password'])
        if token:
            return jsonify({
                "status": "success",
                "token": token.decode()
            })
        else:
            abort(401)
    except:
        abort(400)

# Validates supplied email and password and return auth token. If email and password are
# correct and token is expired, issue a new token and return.
def authenticate_email_password(email, password):
    user = User.query.filter_by(email=email).first()
    if user:
        stored_pw = user.password
        if bcrypt.checkpw(password.encode(), stored_pw.encode()):
            if authenticate_token(user.token.decode()):
                return user.token
            else:
                new_token = generate_token(user.email)
                user.token = new_token
                db.session.commit()
                return new_token
        else:
            return None
    else:
        return None

# Validates authentication token. Returns boolean representing token validity.
def authenticate_token(token, user=None):
    if not user:
        user = User.query.filter_by(token=token.encode()).first()
        if not user:
            return False
    plaintext = crypto.decrypt(token.encode())
    email = plaintext[0:len(plaintext) - 10]
    if user.email != email:
        return False
    timestamp = plaintext[-10::]
    if datetime.now() >= datetime.fromtimestamp(timestamp) + \
        timedelta(hours=token_timeout):
        return False
    return True

# Generate a new authentication token based on current timestamp
def generate_token(email):
    plaintext = (email + str(floor(datetime.now().timestamp()))).encode()
    return crypto.encrypt(plaintext)

if __name__ == "__main__":
    app.run(debug=True)