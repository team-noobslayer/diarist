from flask import Flask, request, jsonify, abort
import bcrypt

app = Flask(__name__)

# Home route
#   GET returns all journal entries by a user
#   POST takes a new journal entry and adds it to database
@app.route("/diarist/", methods=['GET', 'POST'])
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
@app.route("/diarist/register", methods=['POST'])
def register():
    # TODO: Database model integration
    request_data = request.get_json()
    try:
        password = request_data['password'].encode()
        salt = bcrypt.gensalt()
        hashed_pw = bcrypt.hashpw(password, salt)
        return jsonify({
           "route": "/register/",
           "http-method": "POST",
           "password-hash": hashed_pw.decode(),
           "data-received": request_data
        }) 
    except:
        abort(400)

if __name__ == "__main__":
    app.run(debug=True)