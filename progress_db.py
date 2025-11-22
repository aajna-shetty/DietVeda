import sqlite3
import datetime

class ProgressDB:
    def __init__(self):
        self.conn = sqlite3.connect("progress.db")
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT ,
            dosha TEXT,
            score INTEGER
        );
        """
        self.conn.execute(query)
        self.conn.commit()

    def save_score(self, dosha, score):
        today = str(datetime.date.today())
        query = "INSERT INTO progress (date, dosha, score) VALUES (?, ?, ?)"
        self.conn.execute(query, (today, dosha, score))
        self.conn.commit()

    def get_last_30_days(self):
        query = """
        SELECT date, dosha, score 
        FROM progress
        ORDER BY date ASC
        LIMIT 30;
        """
        cursor = self.conn.execute(query)
        return cursor.fetchall()
