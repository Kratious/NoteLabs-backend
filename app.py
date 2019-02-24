from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_jwt_extended import (
    JWTManager
)


app = Flask(__name__, instance_relative_config=True)

POSTGRES = {
    'user': 'postgres',
    'pw': 'postgres',
    'db': 'project-nihilanth',
    'host': 'localhost',
    'port': '5432',
}

app.config['ENV'] = 'development'
app.config['DEBUG'] = True

CORS(app, supports_credentials=True)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Configure application to store JWTs in cookies. Whenever you make
# a request to a protected endpoint, you will need to send in the
# access or refresh JWT via a cookie.
app.config['JWT_TOKEN_LOCATION'] = ['cookies']

# Disable CSRF protection for this example. In almost every case,
# this is a bad idea. See examples/csrf_protection_with_cookies.py
# for how safely store JWTs in cookies
app.config['JWT_COOKIE_CSRF_PROTECT'] = False

app.config['JWT_ACCESS_COOKIE_PATH'] = '/api/example'
app.config['JWT_REFRESH_COOKIE_PATH'] = '/token/refresh'

# Set the secret key to sign the JWTs with
app.config['JWT_SECRET_KEY'] = 'super-secret'

jwt = JWTManager(app)

ma = Marshmallow(app)


import models, routes