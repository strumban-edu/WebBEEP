from flask import Flask, render_template, request, redirect, url_for
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv('dotenv.env')

app = Flask(__name__)

def get_db_connection():
    connection = psycopg2.connect(
        host     =os.getenv('DB_HOST'),
        database =os.getenv('DB_NAME'),
        user     =os.getenv('DB_USER'),
        password =os.getenv('DB_PASSWORD')
    )
    return connection


# HOME PAGE
@app.route('/')
def index():
    connection = get_db_connection()
    cursor = connection.cursor()
    command = '''
        SELECT e.eventid, e.eventname, e.category, e.status, e.eventtime, l.locationname
        FROM "Event" e
        JOIN "Location" l ON e.locationid = l.locationid
        ORDER BY e.eventid;
    '''
    
    cursor.execute(command)
    events = cursor.fetchall()
    
    cursor.close()
    connection.close()
    
    return render_template('WebBeepMockup.html', events=events)


# EVENT ADDING PAGE
@app.route('/add-event', methods=['GET', 'POST'])
def add_event():
    if request.method == 'POST':
        eventname = request.form['eventname']
        category = request.form['category']
        status = request.form['status']
        eventtime = request.form['eventtime']
        location_name = request.form['location_name']
        location_address = request.form.get('location_address', '')

        connection = get_db_connection()
        cursor = connection.cursor()
        # FIRST COMMAND
        command = """
            INSERT INTO "Location" (locationname, locationaddress)
            VALUES (%s, %s)
            RETURNING locationid;
        """

        cursor.execute(command, (location_name, location_address))
        locationid = cursor.fetchone()[0]

        # SECOND COMMAND
        command = """
            INSERT INTO "Event" (eventname, category, status, eventtime, creatorid, locationid)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(command, (eventname, category, status, eventtime, 1, locationid))
        connection.commit()
        cursor.close()
        connection.close()

        return redirect(url_for('index'))

    return render_template('add_event.html')

