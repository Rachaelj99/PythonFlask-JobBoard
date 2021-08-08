import sqlite3
from flask import Flask, render_template, g

PATH = 'db/jobs.sqlite'

app = Flask(__name__)

def open_connection():
    connection = getattr(g, '_connection', None)

@app.route('/')
@app.route('/jobs')
def jobs():
    return render_template('index.html')


if __name__ == '__main__':
    app.debug = True
    app.run() #go to http://localhost:5000/ to view the page.
