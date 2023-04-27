import time
from classes.Database import Database

class Reaction:

    SYMBOLS = ["😈", "👿", "👹", "👺", "🤡", "💩", "👻", "🦫", "🦦", "🦥", "😮‍💨", "😵‍💫", "😶‍🌫️", "❤️‍🔥", "❤️‍🩹", "🧔‍♀️"  ]

    def __init__(self, message_id, symbol, count, is_new = False):
        self.message_id = message_id
        self.symbol = symbol
        self.count = count
        self.is_new = is_new

    def to_json(self):
        return {
            self.symbol: self.count
        }

    def is_valid(self):
        if not self.message_id:
            return {"error": "Message_id cannot be null"}

        if self.symbol not in Reaction.SYMBOLS:
            return {"error": "Symbol not authorized"}

        return True

    def add(self):
        self.count = self.count + 1

    def remove(self):
        self.count = self.count - 1

    def save(self):
        if not self.is_valid() == True:
            return self.is_valid()

        if self.is_new:
            query = "INSERT INTO reactions(message_id, symbol, count) VALUES (?, ?, 1)"
            args = (self.message_id, self.symbol)
        else:
            query = "UPDATE reactions SET count = ? WHERE message_id = ? AND symbol = ?"
            args = (self.count + 1, self.message_id, self.symbol)
        
        try:
            Database.commit_bd(query, args)
            return True
        except:
            return {"error": "An error occured while saving"}

    @staticmethod
    def findOne(message_id, symbol):
        reactions = Database.query_db('SELECT rowid, * FROM reactions WHERE message_id = ? AND symbol = ?', (message_id, symbol))
        reactionObjs = [Reaction(
            reaction['message_id'], 
            reaction['symbol'], 
            reaction['count']
        ).to_json() for reaction in reactions]

        if len(reactionObjs) > 0:
            return reactionObjs[0]
        else:
            return Reaction(message_id, symbol, 0, True)

    @staticmethod
    def find(message_id, symbol):
        reactions = Database.query_db('SELECT * FROM reactions WHERE message_id = ? AND symbol = ?', (message_id, symbol))
        reactionObjs = [Reaction(
            reaction['message_id'], 
            reaction['symbol'], 
            reaction['count']
        ).to_json() for reaction in reactions]

        return reactionObjs