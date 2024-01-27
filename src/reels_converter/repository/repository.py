import sqlite3
import json
import unittest
import logging

logger = logging.getLogger(__name__)

class Repository():
    def __init__(self, db_file_name='statistics.db') -> None:
        self.connection = sqlite3.connect(db_file_name)
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        logger.debug("Creating tables")
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Users (
                id INTEGER PRIMARY KEY,
                username TEXT NOT NULL,
                first_name TEXT,
                last_name TEXT
                );
            ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Videos (
                id LONG INTEGER PRIMARY KEY,
                size INTEGER,
                chat_id INTEGER,
                date INTEGER,
                FOREIGN KEY(chat_id) REFERENCES Users(id)
                );
            ''')
        self.connection.commit()
    
    def _post_row(self, tablename, rec):
        keys = ','.join(rec.keys())
        question_marks = ','.join(list('?'*len(rec)))
        values = tuple(rec.values())
        query = 'INSERT INTO '+tablename+' ('+keys+') VALUES ('+question_marks+')'
        logger.debug(f"Post row query: {query}")
        self.cursor.execute(query, values)
        self.connection.commit()

    def add_user(self, user_data):
        logger.debug(f"Add user to db: {user_data}")
        self._post_row("Users", user_data)
    
    def add_video(self, video_data):
        logger.debug(f"Add video to db: {video_data}")
        self._post_row("Videos", video_data)
    
    def is_person_exist(self, chat_id):
        logger.debug(f"Check user: {chat_id}")
        self.cursor.execute(f'SELECT *  FROM Users WHERE id={chat_id}')
        results = self.cursor.fetchall()
        if len(results) > 0:
            return True
        return False
    
    def get_users(self):
        logger.debug(f"Get all users")
        self.cursor.execute(f'SELECT *  FROM Users')
        results = self.cursor.fetchall()
        logger.debug(f"Users from db: {results}")
        return results

    def get_videos(self, user_id):
        logger.debug(f"Get all videos: {user_id}")
        self.cursor.execute(f'SELECT *  FROM Videos WHERE chat_id={user_id}')
        results = self.cursor.fetchall()
        logger.debug(f"All videos: {results}")
        return results
    
    def get_sum_video_size(self, user_id):
        logger.debug(f"Get all videos size: {user_id}")
        self.cursor.execute(f'SELECT SUM(size)  FROM Videos WHERE chat_id={user_id}')
        results = self.cursor.fetchall()
        logger.debug(f"Get all videos size: {results}")
        return results

class TestStringMethods(unittest.TestCase):
    def test_create_bd(self):
        repo = Repository()
        repo.create_tables()

    def test_add_user(self):
        user = {
            "id": 13131121,
            "username": "zhenya",
            "first_name": "zhenya1",
            "last_name": "zhenya2"
        }
        repo = Repository()
        repo.add_user(user)

    def test_add_video(self):
        import time
        video = {
            "size": 12424552,
            "date": int(time.time()),
            "chat_id": 14
        }
        repo = Repository()
        repo.add_video(video)
    
    def test_check_user_exist(self):
        repo = Repository()
        result = repo.is_person_exist(11)
        assert result == True
        result = repo.is_person_exist(10)
        assert result == False


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
