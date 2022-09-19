import psycopg2
from contextlib import contextmanager
from sqlite3 import Error


@contextmanager
def create_connection():
    conn = None
    try:
        conn = psycopg2.connect(host='localhost', database='postgres', user='postgres', password='password')
        print('Connected!')
        yield conn
        conn.commit()
    except Error as e:
        print(e)
        conn.rollback()
    finally:
        conn.close()
