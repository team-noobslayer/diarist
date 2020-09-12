from datetime import datetime, timedelta
from math import floor
from dotenv import load_dotenv
from cryptography.fernet import Fernet
from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import bcrypt
import os

# Uncomment the following code block to instruct the program to generate a sqlite database. 
#   Setting will be stored in .env and database will be stored in db.sqlite3
#
# with open('.env', 'a') as file:
#     file.write('\nDATABASE_URL = "sqlite:///db.sqlite3"')

# Uncomment the following code block to generate a secret for encryption, to be stored in .env
#   NOTE: Only do this once! Generating a new secret may render previously encrypted
#         data unreadable.
#
# with open('.env', 'a') as file:
#     file.write(f'\nSECRET = "{ Fernet.generate_key().decode() }"')

load_dotenv()
token_crypto_secret = os.environ.get('SECRET')
crypto = Fernet(token_crypto_secret)
token_timeout = 24  # timeout period, in hours, for authentication tokens

app = Flask(__name__)

# Optional, silences deprecation warning
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URI')
db = SQLAlchemy(app)

CORS(app)

class User(db.Model):
    __tablename__ = 'diarist_user'
    email = db.Column(db.String(128), nullable=False, primary_key=True)
    username = db.Column(db.String(32), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    token = db.Column(db.String(256), nullable=False)
    journal_entries = db.relationship('JournalEntry', backref='owner')

class JournalEntry(db.Model):
    __tablename__ = 'diarist_journal_entry'
    entry_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256))
    body = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    last_edited = db.Column(
        db.DateTime, default=datetime.now(), nullable=False)
    author = db.Column(db.String(128), db.ForeignKey('diarist_user.email'))

# Uncomment the next line to create the required tables in a new database on program execution
# db.create_all()

# Home route
#   GET returns all journal entries by a user
#   POST takes a new journal entry and adds it to database
@app.route("/diarist", methods=['GET', 'POST'], strict_slashes=False)
def home():
    request_data = request.get_json()
    if not authenticate_token(request_data['token']):
        abort(401)
    if request.method == 'GET':
        email = get_email_from_token(request_data['token'])
        journal_entry_objects = JournalEntry.query.filter_by(
            author=email).all()
        journal_entries = []
        for entry in journal_entry_objects:
            journal_entries.append({
                'id': entry.entry_id,
                'title': entry.title,
                'body': entry.body,
                'created_at': entry.created_at,
                'last_edited': entry.last_edited,
                'author': entry.author
            })
        return jsonify(
            journal_entries
        )
    elif request.method == 'POST':
        email = get_email_from_token(request_data['token'])
        entry = JournalEntry(
            title=request_data['title'],
            body=request_data['body'],
            author=email
        )
        db.session.add(entry)
        db.session.commit()
        return request.get_json()

# Delete route - deletes journal entry by ID
@app.route("/diarist/delete/<int:entry_id>", methods=['DELETE'])
def delete(entry_id):
    request_data = request.get_json()
    if not authenticate_token(request_data['token']):
        abort(401)
    else:
        entry = JournalEntry.query.get_or_404(entry_id)
        if get_email_from_token(request_data['token']) != entry.author:
            abort(401)
        db.session.delete(entry)
        db.session.commit()
        return request_data

# Edit route - updates a journal entry associated with ID
@app.route("/diarist/edit/<int:entry_id>", methods=['PUT'])
def edit(entry_id):
    request_data = request.get_json()
    if not authenticate_token(request_data['token']):
        abort(401)
    else:
        entry = JournalEntry.query.get_or_404(entry_id)
        if get_email_from_token(request_data['token']) != entry.author:
            abort(401)
        entry.title = request_data['title']
        entry.body = request_data['body']
        entry.last_edited = datetime.now()
        db.session.commit()
        return request_data

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
            password=hashed_pw.decode(),
            token=token
        )
        db.session.add(user)
        db.session.commit()

        return jsonify({
            "status": "success",
            "token": token
        })
    except:
        abort(400)

# Login route - authenticates user based on supplied username and password; returns auth token
@app.route("/diarist/login", methods=['POST'], strict_slashes=False)
def login():
    request_data = request.get_json()
    try:
        token = authenticate_email_password(
            request_data['email'], request_data['password'])
        if token:
            return jsonify({
                "status": "success",
                "token": token
            })
        else:
            abort(401)
    except:
        abort(400)


def generate_token(email):
    plaintext = (email + str(floor(datetime.now().timestamp()))).encode()
    return crypto.encrypt(plaintext).decode()


def get_email_from_token(token):
    plaintext = crypto.decrypt(token.encode()).decode()
    return plaintext[0:len(plaintext)-10]


def get_timestamp_from_token(token):
    plaintext = crypto.decrypt(token.encode()).decode()
    return int(plaintext[-10::])


# Validates supplied email and password and return auth token. If email and password are
# correct and token is expired, issue a new token and return.
def authenticate_email_password(email, password):
    user = User.query.filter_by(email=email).first()
    if user:
        stored_pw = user.password
        if bcrypt.checkpw(password.encode(), stored_pw.encode()):
            if authenticate_token(user.token, user):
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
        user = User.query.filter_by(token=token).first()
        if not user:
            return False
    if user.token != token:
        return False
    email = get_email_from_token(token)
    if user.email != email:
        return False
    timestamp = get_timestamp_from_token(token)
    if datetime.now() >= datetime.fromtimestamp(timestamp) + \
            timedelta(hours=token_timeout):
        return False
    return True


if __name__ == "__main__":
    app.run()
