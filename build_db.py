import sqlite3
con = sqlite3.connect("datas/touiteur.db")
cur = con.cursor()
cur.execute("CREATE TABLE messages (name VARCHAR(16) NOT NULL, message VARCHAR(255) NOT NULL, likes INT DEFAULT 0, ts INT, is_user_authenticated BOOLEAN DEFAULT false)")

cur.execute("CREATE TABLE comments (message_id INT, name VARCHAR(16) NOT NULL, comment VARCHAR(255) NOT NULL, ts INT, CONSTRAINT `fk_message_id` FOREIGN KEY(`message_id`) REFERENCES `messages`(`id`))")

cur.execute("CREATE TABLE reactions (message_id INT, symbol VARCHAR(5) NOT NULL, count INT DEFAULT 0, CONSTRAINT `fk_message_id` FOREIGN KEY(`message_id`) REFERENCES `messages`(`id`))")
