from flask_jwt_extended import create_access_token
from classes.Database import Database
import hashlib

class User:

    SALT = "5gz"

    def __init__(self, username, password, jwt=None, id=None):
        self.username = username
        self.password = password
        self.jwt = jwt
        self.id = id

    def is_valid(self):
        if self.username == None:
            return {"error": "Username cannot be null"}

        if len(self.username) < 3:
            return {"error": "Username is too short"}

        if len(self.username) > 16:
            return {"error": "Username is too long"}

        return True

    def to_json(self):
        pass

    def insert(self):
        try:
            Database.commit_bd(
                "INSERT INTO users(username, password, jwt) VALUES (?, ?, ?)", 
                (self.username, self.password, None)
            )
            return True
        except:
            return {"error": "An error occured while saving"}

    def save(self):
        try:
            Database.commit_bd(
                "UPDATE users SET username = ?, password = ?, jwt= ? WHERE rowid = ?", 
                (self.username, self.password, self.jwt, self.id)
            )
            return True
        except:
            return {"error": "An error occured while saving"}

    def make_jwt(self):
        self.jwt = create_access_token(identity=self.username)
        save = self.save()

        if not save == True:
            return save

        return self


    @staticmethod
    def is_password_valid(password):
        if len(password) < 8:
            return {"error": "Password is too short"}

        return True

    @staticmethod
    def hash_password(password):
        password = password + User.SALT
        hashed = hashlib.md5(password.encode())
        return hashed.hexdigest()

    @staticmethod
    def findByName(username):
        users = Database.query_db('SELECT rowid, * FROM users WHERE username = ?', (username,))

        if len(users) < 1:
            return {"error": "Username does not exist"}

        user = User(users[0]['username'], users[0]['password'], users[0]['jwt'], users[0]['rowid'])

        return user

    @staticmethod
    def findByJwt(jwt):
        print(jwt)
        users = Database.query_db('SELECT rowid, * FROM users WHERE jwt = ?', (jwt,))
        print(users)
        if len(users) < 1:
            return {"error": "JWT is not valid"}

        user = User(users[0]['username'], users[0]['password'], users[0]['jwt'], users[0]['rowid'])

        return user    
