from app import app, db
from flask import request, json, jsonify
from flask_cors import CORS, cross_origin
from flask_jwt_extended import (
    jwt_required, create_access_token,
    jwt_refresh_token_required, create_refresh_token,
    get_jwt_identity, set_access_cookies,
    set_refresh_cookies, unset_jwt_cookies
)
from models import User, Notebook, Note, UserSchema, NoteSchema
from error import InvalidUsage

@app.route("/auth/login", methods=['POST'])
def authenticate_user():
    if not request.json:
        raise InvalidUsage(
            'Something went wrong, please try again.', status_code=400)

    req_data = request.json

    if not req_data['email']:
        raise InvalidUsage('Email field is empty.', status_code=400)

    if not req_data['password']:
        raise InvalidUsage('Password field is empty.', status_code=400)

    user = User.get_user_by_email(req_data['email'])

    #u = User(email='john@email.com')
    #u.set_password('pass')

    if user is None or not user.check_password(req_data['password']):
        raise InvalidUsage('Invalid email or password.', status_code=401)

    # Create the tokens we will be sending back to the user
    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)

    # Set the JWT cookies in the response
    resp = jsonify({'login': True})
    set_access_cookies(resp, access_token)
    set_refresh_cookies(resp, refresh_token)
    return resp, 200

# Same thing as login here, except we are only setting a new cookie
# for the access token.


@app.route('/token/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
        # Create the new access token
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)

    # Set the JWT access cookie in the response
    resp = jsonify({'refresh': True})
    set_access_cookies(resp, access_token)
    return resp, 200

# Because the JWTs are stored in an httponly cookie now, we cannot
# log the user out by simply deleting the cookie in the frontend.
# We need the backend to send us a response to delete the cookies
# in order to logout. unset_jwt_cookies is a helper function to
# do just that.


@app.route('/token/remove', methods=['POST'])
def logout():
    resp = jsonify({'logout': True})
    unset_jwt_cookies(resp)
    return resp, 200

# We do not need to make any changes to our protected endpoints. They
# will all still function the exact same as they do when sending the
# JWT in via a header instead of a cookie

@app.route('/api/example', methods=['GET'])
@jwt_required
def protected():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    user_schema = UserSchema()

    notebooks = user_schema.dump(user).data['notebooks']
    numOfNotes = 0
    for notebook in Notebook.query.filter_by(user_id=user.id):
        numOfNotes += Note.query.filter_by(notebook_id=notebook.id).count()

    resp = jsonify({'notebooks': notebooks, 'numOfNotes': numOfNotes})
    return resp, 200


@app.route('/tasks', methods=['GET'])
@cross_origin()
def get_tasks():
    return jsonify({'tasks': tasks})
