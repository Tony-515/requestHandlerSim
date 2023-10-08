import flask
import collections
import sqlite3

from flask import Flask, render_template
from collections import deque

app = Flask(__name__)

posts = [
	{
		'author': 'Anthony Nosoff',
		'title': 'Something',
		'content': 'First post content'
	}
]

conn = sqlite3.connect('database.db')
print("Opened database successfully")

conn.execute('CREATE TABLE students (name TEXT, addr TEXT, city TEXT, pin TEXT)')
print("Table created successfully")
conn.close()

pending_requests = 0

@app.route("/")
def hello_world():
    return render_template('index.html', req=pending_requests)
	
if __name__ == '__main__':
	app.run(debug=True)