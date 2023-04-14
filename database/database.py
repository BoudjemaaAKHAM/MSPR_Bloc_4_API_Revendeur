import sqlite3
import os


class Db:
    """
    Database class

    This class is used to manage the database
    - Create tables
    - Delete tables
    - Insert a user
    - Get a user by id
    - Get a user by email

    :param db_name: Database name
    :param clear: Clear database
    """

    def __init__(self, db_name, clear=False):
        if os.path.exists(db_name) and clear:
            os.remove(db_name)
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def create_tables(self):
        """
        Create tables
        :return:
        """
        query_users = '''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER,
                    email TEXT NOT NULL ,
                    token TEXT NOT NULL
                )'''
        self.cursor.execute(query_users)
        self.conn.commit()

    def delete_tables(self):
        """
        Delete tables
        :return:
        """
        query_users = '''DROP TABLE IF EXISTS users'''
        self.cursor.execute(query_users)
        self.conn.commit()

    def insert_user(self, user_id, email, token):
        """
        Insert a user
        :param user_id:
        :param email:
        :param token:
        :return:
        """
        query = '''INSERT INTO users (id, email, token) VALUES (?, ?, ?)'''
        self.cursor.execute(query, (user_id, email, token))
        self.conn.commit()

    def get_user(self, user_id):
        """
        Get a user by id
        :param user_id:
        :return:
        """
        query = '''SELECT * FROM users WHERE id = ?'''
        self.cursor.execute(query, (user_id,))
        return self.cursor.fetchone()

    def get_user_by_email(self, email):
        """
        Get a user by email
        :param email:
        :return:
        """
        query = '''SELECT * FROM users WHERE email = ?'''
        self.cursor.execute(query, (email,))
        return self.cursor.fetchone()
