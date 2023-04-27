from flask import Flask, request, send_file
from flask_cors import CORS
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
import sqlite3
import time
from  io import BytesIO
from classes.Database import Database
from classes.Message import Message
from classes.Comment import Comment
from classes.Reaction import Reaction
from classes.User import User
from classes.Avatar import Avatar

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

app.config["JWT_SECRET_KEY"] = "super-secret"
jwt = JWTManager(app)

@app.route("/", methods=['GET'])
def hello_world():
    return "<p>Bientôt il y aura une documentation...</p>"

@app.route("/list", methods=['GET'])
def list():
    ts = request.args.get('ts', 0)
    messages = Database.query_db('SELECT messages.rowid, * FROM messages WHERE messages.ts > ?', (ts,))

    messageObjs = [Message(
        message['rowid'], 
        message['name'], 
        message['message'], 
        message['likes'], 
        message['ts'], 
        message['is_user_authenticated']
    ).to_json() for message in messages]

    return {
        "ts": int(round(time.time()*100)),
        "messages": messageObjs
    }

@app.route("/get", methods=['GET'])
def get():
    id = request.args.get('id', None)
    message = Database.query_db('SELECT rowid, * FROM messages WHERE rowid = ?', (id,))

    if len(message) < 1:
        return {
            "error": "Id does not exist."
        }
    message = message[0]

    messageObj = Message(
        message['rowid'], 
        message['name'], 
        message['message'], 
        message['likes'], 
        message['ts'], 
        message['is_user_authenticated']
    )

    return {
        "success": True,
        "data": messageObj.to_json()
    }

@app.route("/influencers", methods=['GET'])
def influencers():
    count = request.args.get('count', 1)
    users = Database.query_db('SELECT name, COUNT(*) AS messages, (SELECT COUNT(*) FROM comments WHERE comments.name = messages.name) AS comments, COUNT(*) + (SELECT COUNT(*) FROM comments WHERE comments.name = messages.name) AS total FROM messages GROUP BY name UNION ALL SELECT name, 0 AS count_messages, COUNT(*) AS count_comments, COUNT(*) AS total_count FROM comments WHERE name NOT IN (SELECT name FROM messages) GROUP BY name LIMIT ?', (count,))

    users = {user['name']: { "messages": user['messages'],"comments": user['comments']} for user in users}
    
    return {
        "user_count": count,
        "influencers": users
    }

@app.route("/send", methods=['POST'])
def add_touit():
    name = request.form.get('name', None)
    message = request.form.get('message', None)

    touit = Message(None, name, message, 0, None, False)

    if not touit.is_valid():
        return touit.is_valid()

    if touit.insert():
        return {"success": True}
    
    return {
        "error": "Une erreur est survenue"
    }

@app.route("/likes/top", methods=['GET'])
def top_like():
    count = request.args.get('count', 1)
    messages = Database.query_db('SELECT rowid, * FROM messages ORDER BY likes DESC LIMIT ?', (count,))

    messageObjs = [Message(
        message['rowid'], 
        message['name'], 
        message['message'], 
        message['likes'], 
        message['ts'], 
        message['is_user_authenticated']
    ).to_json() for message in messages]

    return {
        "top": messageObjs
    }


@app.route("/likes/send", methods=['PUT'])
def add_like():
    id = request.form.get('message_id', None)

    message = Message.findOneById(id)

    if not isinstance(message, Message):
        return {
            "error": "Message not found"
        }
        
    result = message.add_like()
    if not result == True:
        return result

    return { "success": True }


@app.route("/likes/remove", methods=['DELETE'])
def remove_like():
    id = request.form.get('message_id', None)

    message = Message.findOneById(id)

    if not isinstance(message, Message):
        return {
            "error": "Message not found"
        }
        
    result = message.remove_like()
    if not result == True:
        return result

    return { "success": True }


@app.route("/comments/list", methods=['GET'])
def get_comments():
    message_id = request.args.get('message_id', None)
    comments = Comment.find(message_id)

    comments = [comment.to_json() for comment in comments]

    return {
        "comments": comments
    }  

@app.route("/comments/send", methods=['POST'])
def add_comment():
    message_id = request.form.get('message_id', None)
    name = request.form.get('name', None)
    comment = request.form.get('comment', None)

    comment = Comment(message_id, name, comment, None)

    if not comment.is_valid():
        return comment.is_valid()

    result = comment.insert()
    if not result == True:
        return result

    return { "success": True }


@app.route("/reactions/allowed", methods=['GET'])
def list_reactions():
    return Reaction.SYMBOLS

@app.route("/trending", methods=['GET'])
def trendings():
    return Message.getWords()

@app.route("/reactions/add", methods=['PUT'])
def add_reaction():
    message_id = request.form.get('message_id', None)
    symbol = request.form.get('symbol', None)
    
    reaction = Reaction.findOne(message_id, symbol)
    reaction.add()

    result = reaction.save()
    print(result)
    if not result == True:
        return result

    return { "success": True }


@app.route("/reactions/remove", methods=['DELETE'])
def remove_reaction():
    message_id = request.form.get('message_id', None)
    symbol = request.form.get('symbol', None)
    
    reaction = Reaction.findOne(message_id, symbol)
    reaction.remove()
    
    result = reaction.save()
    if not result == True:
        return result

    return { "success": True }

@app.route("/avatar/get", methods=['GET'])
def get_avatar():
    username = request.args.get('username', None)
    size = request.args.get('size', 850)

    image = Avatar(username, size).get()
    
    img_io = BytesIO()
    image.save(img_io, 'PNG', quality=70)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')

@app.route("/user/register", methods=['POST'])
def user_register():
    username = request.form.get('username', None)
    password = request.form.get('password', None)

    if User.findByName(username) == True:
        return {"error": "Username already exists"}

    password_validation = User.is_password_valid(password) 
    if password_validation != True:
        return password_validation

    user = User(username, User.hash_password(password))

    result = user.insert()
    if not result == True:
        return result

    return { "success": True }

@app.route("/user/login", methods=['POST'])
def user_login():
    username = request.form.get('username', None)
    password = request.form.get('password', None)

    user = User.findByName(username)
    if not isinstance(user, User):
        return user

    if not user.password == User.hash_password(password):
        return {"error": "Invalid password"}

    user = user.make_jwt()
    if not isinstance(user, User):
        return user

    return {
        "access_token": user.jwt
    }

@app.route("/user/me", methods=['GET'])
def user_me():
    token = request.headers.get('Authorization')
    token = token.replace('Bearer ', '')

    user = User.findByJwt(token)
    if not isinstance(user, User):
        return user

    return {
        "logged_in_as": {
            "name": user.username,
            "expiration": None
    }}

@app.errorhandler(404)
def not_found(error):
    return 'Error', 404