import sqlite3
import datetime
from flask import Flask, render_template, g, request, redirect, url_for, redirect

PATH = 'db/jobs.sqlite'

app = Flask(__name__)

def open_connection():
    print("You're connected!")
    connection = getattr(g, '_connection', None)
    if connection == None:
        connection = g._connection = sqlite3.connect(PATH)
    connection.row_factory = sqlite3.Row
    return connection

def execute_sql(sql, values=(), commit=False, single=False):
    print("You're executing SQL!")
    connection = open_connection()
    cursor = connection.execute(sql, values)
    if commit == True:
        results = connection.commit()
    else:
        results = cursor.fetchone() if single else cursor.fetchall()
    cursor.close()
    return results

@app.teardown_appcontext
def close_connection(exception):
    print("You're closing connection!")
    connection = getattr(g, '_connection', None)
    if connection is not None:
        connection.close()

@app.route('/')
@app.route('/jobs')
def jobs():
    print("You're in jobs!")
    jobs = execute_sql('SELECT job.id, job.title, job.description, job.salary, employer.id as employer_id, employer.name as employer_name FROM job JOIN employer ON employer.id = job.employer_id')
    return render_template('index.html', jobs=jobs)

@app.route('/job/<job_id>')
def job(job_id):
    print("You're in job!")
    jobs = execute_sql('SELECT job.id, job.title, job.description, job.salary, employer.id as employer_id, employer.name as employer_name FROM job JOIN employer ON employer.id = job.employer_id WHERE job.id = ?', [job_id], single=True)
    return render_template('job.html', job=job)

@app.route('/employer/<employer_id>')
def employer(employer_id):
    print("You're in employer!")
    employer = execute_sql('SELECT * FROM employer WHERE id=?', [employer_id], single=True)
    jobs = execute_sql('SELECT job.id, job.title, job.description, job.salary FROM job JOIN employer ON employer.id = job.employer_id WHERE employer.id = ?', [employer_id])
    reviews = execute_sql('SELECT review, rating, title, date, status FROM review JOIN employer ON employer.id = review.employer_id WHERE employer.id = ?', [employer_id])
    return render_template('employer.html', employer=employer, jobs=jobs, reviews=reviews)

@app.route('/employer/<employer_id>/review', methods=('GET', 'POST'))
def review(employer_id):
    print("You're in review!")
    if request.method == 'POST':
        review = request.form['review']
        rating = request.form['rating']
        title = request.form['title']
        status = request.form['status']

        date = datetime.datetime.now().strftime("%m/%d/%Y")
        execute_sql('INSERT INTO review (review, rating, title, date, status, employer_id) VALUES (?, ?, ?, ?, ?, ?)', (review, rating, title, date, status, employer_id), commit=True)

        return redirect(url_for('employer', employer_id=employer_id))

    return render_template('review.html', employer_id=employer_id)
# if __name__ == '__main__':
#     app.debug = True
#     app.run() #go to http://localhost:5000/ to view the page.
