import time
from classes.Database import Database

class Comment:

    def __init__(self, message_id, name, comment, ts):
        self.message_id = message_id
        self.name = name
        self.comment = comment
        self.ts = ts

    def is_valid(self):
        if self.message_id == None:
            return { "error": "Message cannot be null" }

        if self.name == None:
            return { "error": "Name cannot be null" }

        if len(self.name) < 3:
            return { "error": "Name is too short" }

        if len(self.name) > 16:
            return { "error": "Name is too long" }

        if self.comment == None:
            return { "error": "Message cannot be null" }

        if len(self.comment) < 3:
            return { "error": "Message is too short" }

        if len(self.comment) > 256:
            return { "error": "Message is too long" }

        return True


    def insert(self):
        try:
            Database.commit_bd(
                "INSERT INTO comments(message_id, name, comment, ts) VALUES (?, ?, ?, ?)", 
                (self.message_id, self.name, self.comment, int(round(time.time()*1000)))
            )
            return True
        except:
            return {"error": "An error occured while saving"}

    def to_json(self):
        return {
            "name": self.name,
            "comment": self.comment,
            "ts": self.ts
        }

    @staticmethod
    def find(id):
        comments = Database.query_db('SELECT * FROM comments WHERE message_id = ?', (id,))
        comments = [Comment(comment['message_id'],comment['name'], comment['comment'], comment['ts']) for comment in comments]
        

        return comments     