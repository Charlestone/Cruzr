import json
from flask import Flask, Response, request, g
import sqlite3

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
    return send_json(req)

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
