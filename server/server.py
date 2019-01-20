import json
from flask import Flask, Response, request, g
import sqlite3
import os
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.headerregistry import Address


app = Flask(__name__)
app.config['APPLICATION_ROOT'] = '/api/v1'

### Endpoints

@app.route('/api/v1/')
def root():
    obj = {
        "version": 1.0
    }
    return send_json(obj)

@app.route('/api/v1/search/', methods=['POST'])
def search():
    req = request.json
    if req == None:
        return error('empty search request')
    db = get_db()
    tags = req['tags']
    matches = []
    for tag in tags:
        c = db.execute(
                '''SELECT name, age, email, hashtag FROM users
                JOIN search ON users.userid = search.user
                WHERE hashtag = ?''', [tag['tag']]
                )
        matches.append([tuple(row) for row in c.fetchall()])
    return send_json(matches)

@app.route('/api/v1/cross/', methods=['GET'])
def cross() :
    db = get_db()
    cruzerID = request.args['cruzerID']
    cruzedID = request.args['cruzedID']
    tag = request.args['tag']
    print("test4")
    cruzedMail = db.execute(
            ''' SELECT email FROM users WHERE userid = ?''',cruzedID
    ).fetchone()[0]
    cruzerMail = db.execute(
            ''' SELECT email FROM users WHERE userid = ?''', cruzerID
    ).fetchone()[0]
    print("test5")
    sendEmail(cruzerMail, cruzedMail, tag)
    print(cruzedMail)
    return Response(status=200)


### Helper Functions

def send_json(message, code=200):
    return Response(response=json.dumps(message),
                    status=code,
                    mimetype='application/json')

def error(message, code =400):
    return Response(response=message,
                    status=code,
                    mimetype='text/plain')


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(os.path.join(app.root_path, 'database.db'))
    rv.row_factory = sqlite3.Row
    return rv


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


def init_db():
    """
    Set up the database, clearing any data and loading the data for cities.
    """
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
        db.commit()


@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


def sendEmail(cruzerMail, cruzedMail, tag) :
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "CruzrCrossManager@gmail.com"  # Enter your address
    receiver_email = cruzedMail   #"tbaillym@ucsc.edu"  # Enter receiver address
    password = "DLUCT0120"

    message = MIMEMultipart("alternative")
    message["Subject"] = "You got crossed"
    message["From"] = sender_email
    message["To"] = receiver_email

    html = f"""\
    <html>
      <body>
        <p>Hi there!<br>
        You got crossed for the tag <strong>{tag}</strong>.<br>
        Contact your Cruzer at:  <strong>{cruzerMail} </strong><br>
        </p>
      </body>
    </html>
    """
    # Turn these into plain/html MIMEText objects
    part = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())



