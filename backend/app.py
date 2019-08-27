from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_jwt_extended import JWTManager

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'some-secret-string'
db = SQLAlchemy(app)
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600
ma = Marshmallow(app)
jwt = JWTManager(app)
