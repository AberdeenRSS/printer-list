from flask import Flask, render_template,request

import sqlite3
import os
import json

app = Flask(__name__)

IN_PROD = os.environ.get('PRODUCTION','false').lower() == 'true'

if IN_PROD:
    DATABASE_URL = '/app/data/printer.db'
    CURRENT_ACCESS_KEY = os.environ.get('ACCESS_KEY')
else:
    DATABASE_URL = 'printer.db'
    CURRENT_ACCESS_KEY = '123456789'

# Home page that shows the current links to the printers in the database
@app.route('/')
def home():
    conn = sqlite3.connect(DATABASE_URL)

    cur = conn.cursor()
    
    # Return true if printer table exists
    printers_exists = cur.execute('SELECT name FROM sqlite_master WHERE type="table" AND name="printers"')
    if not printers_exists.fetchone():
        return "No printers found in database"
    
    cur.execute('SELECT * FROM printers')
    printers = cur.fetchall()
    conn.close()        
    # Create a list of dictionaries for each printer
    printers_context = []
    for printer in printers:
        printer_dict = {
            'name': printer[0],
            'url': printer[1],
            'status': printer[2],
            'last_updated': printer[3]
        }
    printers_context.append(printer_dict)

    return render_template('home.html',printers=printers_context)


# Webhook for printer server to send the url of currently running printers, first checking an access key
@app.route('/webhook',methods=['POST'])
def webhook():
    if request.method == 'POST':
        # Get the X-API-KEY header 
        api_key = request.headers.get('X-API-KEY')

        # Check if access key is correct
        # Should be in the form "Bearer 1234"
        access_key = api_key.split(' ')[1]

        # If access key is incorrect, return 401
        if access_key != CURRENT_ACCESS_KEY:
            return "Unauthorized"

        conn = sqlite3.connect(DATABASE_URL)
        cur = conn.cursor()  
        
        # Get the request payload and update the database or create a new row if a printer doesnt yet exist 

        # Check if printer table exists
        printers_exists = cur.execute('SELECT name FROM sqlite_master WHERE type="table" AND name="printers"')
        if not cur.fetchone():
                # Create the table if it doesn't exist
                cur.execute('''CREATE TABLE printers 
                               (name TEXT PRIMARY KEY, 
                                url TEXT, 
                                status TEXT, 
                                last_updated DATETIME DEFAULT CURRENT_TIMESTAMP)''')
            
        
        # Add or update the printers
        printers = request.json
        for printer in printers:
            cur.execute('''INSERT OR REPLACE INTO printers (name, url, status, last_updated) 
                           VALUES (?, ?, 'online', CURRENT_TIMESTAMP)''', 
                        (printer['name'], printer['url']))

        # Set the status of all printers that weren't updated to offline
        cur.execute('UPDATE printers SET status="offline" WHERE last_updated < datetime("now","-1 minute")')

        conn.commit()
        conn.close()

        return "Success"


if __name__ == '__main__':
    app.run(host='0.0.0.0')

