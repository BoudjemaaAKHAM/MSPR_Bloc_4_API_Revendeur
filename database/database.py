import sqlite3
import os


class Db:
    def __init__(self, db_name, clear=False):
        if os.path.exists(db_name) and clear:
            os.remove(db_name)
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def create_tables(self):
        query_users = '''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER,
                    email TEXT NOT NULL ,
                    token TEXT NOT NULL
                )'''
        self.cursor.execute(query_users)
        self.conn.commit()

    def delete_tables(self):
        query_users = '''DROP TABLE IF EXISTS users'''
        self.cursor.execute(query_users)
        self.conn.commit()

    def insert_user(self, user_id, email, token):
        query = '''INSERT INTO users (id, email, token) VALUES (?, ?, ?)'''
        self.cursor.execute(query, (user_id, email, token))
        self.conn.commit()

    def get_user(self, user_id):
        query = '''SELECT * FROM users WHERE id = ?'''
        self.cursor.execute(query, (user_id,))
        return self.cursor.fetchone()

    def get_user_by_email(self, email):
        query = '''SELECT * FROM users WHERE email = ?'''
        self.cursor.execute(query, (email,))
        return self.cursor.fetchone()


db = Db("../data/database", clear=True)
db.create_tables()

db.insert_user(1, "test@test.com", "token")
print(db.get_user(1))
print(db.get_user_by_email("test@test.com"))



