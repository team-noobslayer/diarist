from datetime import datetime
from dotenv import load_dotenv
from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
import bcrypt
import os

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Optional, silences deprecation warning
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URI')

db = SQLAlchemy(app)

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)

class JournalEntry(db.Model):
    entry_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    body = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    last_edited = db.Column(db.DateTime, default=datetime.now, nullable=False)

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

# Register route - registers a new user based on the provided
#   authentication information
@app.route("/diarist/register", methods=['POST'], strict_slashes=False)
def register():
    request_data = request.get_json()
    try:
        pwd = request_data['password'].encode()
        salt = bcrypt.gensalt()
        hashed_pw = bcrypt.hashpw(pwd, salt)
        user = User(username=request_data['username'], email=request_data['email'], password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        return jsonify({
            "status": "success"
        }) 
    except:
        abort(400)

# Authentication helper function - compares password parameter
#   to password stored for user with given ID
def authenticate(pwd, userID):
    # TODO: query DB for hashed password associated with UserID
    stored_pw = None # Replace with DB value
    if bcrypt.checkpw(pwd, stored_pw):
        return True
    else:
        return False

if __name__ == "__main__":
    app.run(debug=True)