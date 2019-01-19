import json
from flask import Flask, Response, request, g, send_file
import io
import sqlite3
import os

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

@app.route('/api/v1/user/image/', methods=['GET'])
def user_images():
    try:
        user = request.args['user']
    except KeyError as e:
        return error('Missing user parameter')
    db = get_db()
    old = db.text_factory
    db.text_factory = bytes
    c = db.execute('SELECT picture FROM users WHERE userid = ?', [user])
    try:
        img = c.fetchone()[0]
    except TypeError as e:
        return error(f'No image for user {user}')
    db.text_factory = old
    return send_file(
            io.BytesIO(img),
            mimetype='image/jpeg',
            attachment_filename=f'{user}.jpg'
            )

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
