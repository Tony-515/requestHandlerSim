import collections
import math
import sqlite3
import threading
from collections import deque
from datetime import datetime

import flask
import flask_wtf
from flask import Flask, jsonify, render_template, request
from flask_wtf import FlaskForm
from wtforms import DecimalField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange

app = Flask(__name__)

app.config['SECRET_KEY'] = '4f8fcb540c29564687435347124c9acd'

pending_requests = 0
factorial = 0
postQueue = deque()

con = sqlite3.connect("database.db")
print("Opened database successfully")

def create_db():
    with con:
        cur = con.cursor()
        cur.execute("DROP TABLE IF EXISTS Requests")
        cur.execute("CREATE TABLE requests (id INTEGER PRIMARY KEY AUTOINCREMENT, number INTEGER, factorial TEXT, timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP);")

        ## call commit on the connection...
        con.commit()

create_db()

def getLastHundredRows():
    try:
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        # print("Connected to SQLite")

        sqlite_select_query = """SELECT * from Requests ORDER BY id DESC"""
        cursor.execute(sqlite_select_query)
        records = cursor.fetchmany(100)

        cursor.close()
        return records

    except sqlite3.Error as error:
        print("Failed to read data from table", error)
    finally:
        if connection:
            connection.close()
            # print("The Sqlite connection is closed")
def getFirstRow():
    try:
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        # print("Getting first row")

        sqlite_select_query = """SELECT * from Requests LIMIT 1"""
        cursor.execute(sqlite_select_query)
        record = cursor.fetchone()

        cursor.close()
        return record

    except sqlite3.Error as error:
        print("Failed to read data from table", error)
    finally:
        if connection:
            connection.close()
            # print("The Sqlite connection is closed")

class NewThreadedTask(threading.Thread):
    def __init__(self):
        super(NewThreadedTask, self).__init__()

    def run(self):
        global pending_requests
        global factorial
        global postQueue
        con = sqlite3.connect("database.db")
        while bool(postQueue):
            input = postQueue.popleft()
            factorial = math.factorial(input)
            # print(input, factorial)
            con.execute("INSERT INTO Requests (number, factorial) VALUES (?, ?);", (input, str(factorial)))
            pending_requests -= 1
        con.commit()
        print('Current Queue Processed')

class IntegerForm(FlaskForm): 
  # Form for submitting a single integer less than or equal to 100
  input_integer = DecimalField('Integer', 
                               validators=[DataRequired(), 
                               NumberRange(min=0, max=100)])
  submit = SubmitField('Send')

posts = [
    {
        'author': 'Anthony Nosoff',
        'title': 'Something',
        'content': 'First post content'
    }
]

# conn.execute('CREATE TABLE requests (id INTEGER PRIMARY KEY AUTOINCREMENT, number INTEGER, factorial INTEGER, timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP)')
# print("Table created successfully")
# conn.close()

# @app.route("/", methods=["GET", "POST"])
# def index():
    # if request.method == "POST":
        # try:
            # input_integer = int(request.form.get("input_integer"))
            # factorial_value = math.factorial(input_integer)
            
            # # Insert data into the "requests" table
            # conn.execute('INSERT INTO requests (number, factorial) VALUES (?, ?)', (input_integer, factorial_value))
            # conn.commit()
            
            # return "Data inserted successfully!"
        # except ValueError:
            # return "Invalid input. Please enter an integer."
    
    # return render_template('index.html')

# '''input_integer = 3
# #how do i get it from user input?
# factorial_value = math.factorial(input_integer)
# conn.execute('INSERT INTO requests (number, factorial) VALUES (?, ?)', (input_integer, factorial_value))
# conn.commit()
# conn.close()
# '''
active_thread = NewThreadedTask()

@app.route("/", methods=['GET', 'POST'])
def readPost():
    global pending_requests
    global factorial
    global active_thread
    if request.method == 'POST':
        # print("***", request.json)
        input_integer = int(request.json.get('number'))
        postQueue.append(input_integer)
        pending_requests += 1
        if active_thread is not None and not active_thread.is_alive():
            active_thread = NewThreadedTask()
            active_thread.start()
        return jsonify({'integer': 0}), 200
    else:
        form = IntegerForm()
        return render_template('index.html', req=pending_requests, form=form, factorial=factorial)
        
        
@app.route('/log')
def show_log():
    reqs = getLastHundredRows()
    firstRow = getFirstRow()
    return render_template('log.html', reqs=reqs, firstRow=firstRow)
	
@app.route('/prq')
def pending():
	global pending_requests
	return "<p>"+str(pending_requests)+"</p>"
    
input = 0
# while True:


if __name__ == '__main__':
    app.run(debug=True)