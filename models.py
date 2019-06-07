import sqlite3

conn = sqlite3.connect('calendarevents.db')

c = conn.cursor()


def create_date_table():
    c.execute(
        '''CREATE TABLE IF NOT EXISTS events(date TEXT, start TEXT, end TEXT, duration REAL, summary TEXT, location 
        TEXT, description TEXT)''')

def add_event():
    pass

def next_event():
    pass

def close_connections():
    conn.commit()
    conn.close()


create_date_table()

close_connections()
