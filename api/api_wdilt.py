"""
 REST API implementation using Flask, Flask RESTful and SQLAlchemy
 for the app WDILT.

 This API handles the comunication with the MySQL database that holds
 the app's data.

 Dependencies:
    pip install flask flask_restful flask_cors
                flask_sqlalchemy configparser mysql-connector-python-rf
                pyjwt
"""
# Imports
from flask import Flask, make_response, jsonify, json
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import datetime
import configparser
import hashlib, uuid
import jwt
import os

# Flask initialization.
app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
api = Api(app)

# Read config database info from the config file.
Config = configparser.ConfigParser()
Config.read("./config.ini")

# Establishing a MySQL connection
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username=Config.get('DEFAULT', 'username'),
    password=Config.get('DEFAULT', 'password'),
    hostname=Config.get('DEFAULT', 'hostname'),
    databasename=Config.get('DEFAULT', 'databasename'),
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Get JWT secret key, stored as an enviroment variable.
JWT_KEY = os.environ.get('TERM')


class Post(db.Model):
    """ Represents the table post in the database.

    Attributes:
        content: A string with the content of the post written by the user.
        username: A string with the username who publishes the posts.
        tags: A string of tags, words or sentences, split with a semicolon. For example: each;of;this;is a;tag;
    """
    __tablename__ = 'post'

    id = db.Column('id', db.Integer, primary_key=True)
    timestamp = db.Column('timestamp', db.DateTime)
    content = db.Column('content', db.String(256))
    username = db.Column('username', db.String(20))
    tags = db.Column('tags', db.String(256))

    def __init__(self, content, username, tags):
        """ Initialices intance of the class so that instance can be used
        to interact with the database table.
        """
        self.content = content
        self.username = username
        self.tags = tags
        self.timestamp = datetime.datetime.now()


class User(db.Model):
    """ Represents the table user in the database.

    Attributes:
        username: A string with the username.
        password: A string of the hashed user password.
        salt: A string generated for salting the password.
    """
    __tablename__ = 'user'

    username = db.Column('username', db.Integer, primary_key=True)
    password = db.Column('password', db.String(256))
    salt = db.Column('salt', db.String(256))

    def __init__(self, username, password, salt):
        """ Initialices intance of the class so that instance can be used
        to interact with the database table.
        """
        self.username = username
        self.password = password
        self.salt = salt


@app.route('/')
def index():
    #api.add_resource(Post, "/api/post/")
    output = '<p>API is running yay</p>'
    return output


@api.resource('/api/post/')
class PostRes(Resource):

    def get(self):
        """ TODO: Describe.
        """

        # Parse request arguments.
        parser = reqparse.RequestParser()
        parser.add_argument("token")
        args = parser.parse_args()

        # Check arguments have been sent.
        if args["token"] == None:
            return simpleResponse("failure", "Authorization token missing"), 400

        # Check validity of the auth token.
        validity, username = validateToken(args["token"])

        if validity == False:
            return simpleResponse("failure", "Invalid authorization token"), 401

        # Query the resource.
        query = Post.query.filter_by(username=username)

        # Format the result and send back the response.
        res = []
        for post in query:
            item = {
                "id": post.id,
                "timestamp": post.timestamp.strftime("%d %b, %Y"),
                "username": post.username,
                "content": post.content,
                "tags": post.tags
            }
            res.append(item)

        return res, 200

    def post(self):
        """ TODO: Describe.
        """

        # Parse request arguments.
        parser = reqparse.RequestParser()
        parser.add_argument("token")
        parser.add_argument("content")
        parser.add_argument("tags")
        args = parser.parse_args()

        # Check arguments have been sent.
        if args["token"] == None:
            return simpleResponse("failure", "Authorization token missing"), 400

        elif args["content"] == None:
            return simpleResponse("failure", "Post content can't be empty"), 400

        # Check validity of the auth token.
        validity, username = validateToken(args["token"])

        if validity == False:
            return simpleResponse("failure", "Invalid authorization token"), 401

        # Create the new post and store it on the database.
        new = Post(args["content"], username, args["tags"])
        db.session.add(new)
        db.session.flush()

        db.session.refresh(new)

        # Format response and reply
        response = {
            "id": new.id,
            "timestamp": new.timestamp.strftime("%d %b, %Y"),
            "username": new.username,
            "content": new.content,
            "tags": new.tags
        }

        db.session.commit()

        return response, 201


@api.resource("/api/post/<string:id>/")
class DelPostRes(Resource):
    def delete(self, id):

        # Parse request arguments.
        parser = reqparse.RequestParser()
        parser.add_argument("token")
        args = parser.parse_args()

        # Check arguments have been sent.
        if args["token"] == None:
            return simpleResponse("failure", "Authorization token missing"), 400

        # Check validity of the auth token.
        validity, username = validateToken(args["token"])

        if validity == False:
            return simpleResponse("failure", "Invalid authorization token"), 401

        # Execute database query
        query = db.engine.execute('DELETE FROM post WHERE id={};'.format(id))

        # TODO: Check query success. Instead of assuming.
        return simpleResponse("success", "Post deleted"), 200


@api.resource('/api/user/')
class UserResource(Resource):

    def get(self):
        # Parse body arguments.
        parser = reqparse.RequestParser()
        parser.add_argument("username")
        parser.add_argument("password")
        args = parser.parse_args()

        query = User.query.filter_by(username=args["username"]).first()

        if query == None:
            return simpleResponse("failure", "User does not exist"), 404

        hashed_password = hashlib.sha512(args["password"].encode('utf-8') \
                                + query.salt.encode('utf-8')).hexdigest()

        if hashed_password != query.password:
            response = {"Failure": "Bad user and password combination."}
            return response, 400

        token = jwt.encode({'username': args["username"]}, JWT_KEY, algorithm='HS256')

        responseObject = {
            'status': 'success',
            'message': 'Successfully logged in.',
            'token': token.decode()
        }
        return responseObject, 200

    def post(self):
        # Parse body arguments.
        parser = reqparse.RequestParser()
        parser.add_argument("username")
        parser.add_argument("password")
        args = parser.parse_args()

        # Check required body argument have been received
        if args["username"] == "":
            # TODO: Add error msg
            return 400

        if args["password"] == "":
            # TODO: Add error msg
            return 400

        # Hash and salt password

        salt = uuid.uuid4().hex
        hashed_password = hashlib.sha512(args["password"].encode('utf-8') \
                                + salt.encode('utf-8')).hexdigest()

        # Create a new user and store it in the database.
        new = User(args["username"], hashed_password, salt)
        db.session.add(new)
        db.session.commit()

        # Generate possitive response and reply.
        response = {"Success": "User was created. You can log in now."}

        return response, 201


def validateToken(token):
    """Decodes and validates a JWT token

    Args:
        token: A JWT to check.

    Returns:
        A boolean type indicating if the token is valid and the username decoded
        from the token if this infact was valid.
    """
    try:
        # The 'decode' method checks the validity of the code and raises an
        # exception if not.
        decoded = jwt.decode(token, JWT_KEY, algorithms=['HS256'])

        return True, decoded["username"]

    except:
        return False, None

def simpleResponse(status, msg):
    """ Creates a simple dictionary to respond to a request.

    Attr:
        status: A string indicating if the request was a success or a failure.
        msg: A string explaining how the operation went.
    """
    response = {
        'status': status,
        'message': msg
    }

    return response

if __name__ == '__main__':
    app.run()
