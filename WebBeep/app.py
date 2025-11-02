from flask import Flask, render_template, request, redirect, url_for
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv('dotenv.env')

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute('''
        SELECT e.eventid, e.eventname, e.category, e.status, e.eventtime, l.locationname
        FROM "Event" e
        JOIN "Location" l ON e.locationid = l.locationid
        ORDER BY e.eventid;
    ''')
    
    events = cur.fetchall()
    cur.close()
    conn.close()
    
    return render_template('WebBeepMockup.html', events=events)


@app.route('/add-event', methods=['GET', 'POST'])
def add_event():
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Fetch locations for dropdown
    cur.execute('SELECT locationid, locationname FROM "Location" ORDER BY locationname;')
    locations = cur.fetchall()
    
    if request.method == 'POST':
        eventname = request.form['eventname']
        category = request.form['category']
        status = request.form['status']
        eventtime = request.form['eventtime']
        locationid = request.form['locationid']
        creatorid = 1  # For now, default user id; later can tie to logged-in user
        
        cur.execute('''
            INSERT INTO "Event" (eventname, category, status, eventtime, locationid, creatorid)
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', (eventname, category, status, eventtime, locationid, creatorid))
        
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('index'))
    
    cur.close()
    conn.close()
    return render_template('add_event.html', locations=locations)
