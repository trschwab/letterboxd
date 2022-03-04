import re
import sqlite3
import requests

from bs4 import BeautifulSoup

def utility_test():
	''' This is a test function to ensure the import of this file is correct
	'''
	print("This is a test of utility imports")
	return 1

def get_page(url):
	s = requests.session()
	r = s.get(url)
	soup = BeautifulSoup(r.text, "html.parser")
	return soup

def create_connection(db):
        conn = None
        try:
                conn = sqlite3.connect(db)
        except Error as e:
                print(e)
        return conn

def close_connection(conn):
        conn.close()
        print("closed connection")
        return 1

def execute_task(conn, task):
        cur = conn.cursor()
        cur.execute(task)
        return 1

def select_all_tasks(conn, db):
        cur = conn.cursor()
        cur.execute("SELECT * from " + db)
        rows = cur.fetchall()
        for row in rows:
                print(row)
        return 1
