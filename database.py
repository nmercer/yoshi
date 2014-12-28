import sqlite3

class Database(object):
    def __init__(self, db_name):
        self.db_name = db_name

    def fetch(self, query):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute(query)
        data = c.fetchall()

        conn.commit()
        conn.close()
        return data

    def exists(self, query):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute(query)
        data = c.fetchone()

        conn.commit()
        conn.close()
        if data:
            return True
        return data

    def insert(self, query):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute(query)
        conn.commit()
        conn.close()

    def check(self, query):
        try:
            self.insert(query)
            return False
        except:
            return True
