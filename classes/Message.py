import time
import re
from collections import Counter
from classes.Database import Database
from classes.Comment import Comment
from classes.Reaction import Reaction


class Message:

    def __init__(self, id, name, message, likes, ts, is_user_authenticated):
        self.id = id
        self.name = name
        self.message = message
        self.likes = likes
        self.ts = ts,
        self.is_user_authenticated = is_user_authenticated
        self.comments = self.get_comments()
        self.reactions = self.get_reactions()
    
    def is_valid(self):
        if self.name == None:
            return { "error": "Name cannot be null" }

        if len(self.name) < 3:
            return { "error": "Name is too short" }

        if len(self.name) > 16:
            return { "error": "Name is too long" }

        if self.message == None:
            return { "error": "Message cannot be null" }

        if len(self.message) < 3:
            return { "error": "Message is too short" }

        if len(self.message) > 256:
            return { "error": "Message is too long" }
        
        return True

    def insert(self):
        try:
            Database.commit_bd(
                "INSERT INTO messages(name, message, ts, likes, is_user_authenticated) VALUES (?, ?, ?, 0, False)", 
                (self.name, self.message, int(round(time.time()*1000)))
            )
            return True
        except:
            return {"error": "An error occured while saving"}

    def save(self):
        try:
            Database.commit_bd(
                "UPDATE messages SET name = ?, message = ?, likes= ? WHERE rowid = ?", 
                (self.name, self.message, self.likes, self.id)
            )
            return True
        except:
            return {"error": "An error occured while saving"}

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "message": self.message,
            "likes": self.likes,
            "ts": self.ts[0],
            "is_user_authenticated": self.is_user_authenticated,
            "comments_count": len(self.comments),
            "reactions": self.reactions,
        }

    def add_like(self):
        self.likes = self.likes + 1
        return self.save()

    def remove_like(self):
        self.likes = self.likes - 1
        return self.save()

    def get_comments(self):
        comments = Comment.find(self.id)
        comments = [comment.to_json() for comment in comments]
        return comments

    def get_reactions(self):
        reactions = Database.query_db('SELECT * FROM reactions WHERE message_id = ?', (self.id,))
        reactions = {r['symbol']: r['count'] for r in reactions}
        return reactions


    @staticmethod
    def findOneById(id):
        messages = Database.query_db('SELECT rowid, * FROM messages WHERE rowid = ?', (id,))

        if len(messages) != 1:
            return {"error": "This message does not exists"}
        
        message = Message(
            messages[0]['rowid'], 
            messages[0]['name'], 
            messages[0]['message'], 
            messages[0]['likes'], 
            messages[0]['ts'], 
            messages[0]['is_user_authenticated']
        )

        return message   

    @staticmethod
    def getWords():
        messages = Database.query_db('SELECT message FROM messages')
        words = [message['message'].split(' ') for message in messages]
        words = [c for b in words for c in b]
        words = [word for word in words if len(word) > 3 and len(word) < 12 and re.match(r"[a-zA-Z0-9]+", word)]

        return dict(Counter(words))