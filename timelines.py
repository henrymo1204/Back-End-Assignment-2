import sys
import textwrap
import logging.config
import sqlite3

import bottle
import bottle_sqlite
from bottle import get, post, delete, error, abort, request, response, HTTPResponse

import users


conn = sqlite3.connect('timelines.db')
conn.execute("CREATE TABLE posts(id INTEGER PRIMARY KEY, user_id NOT NULL)")

app = bottle.default_app()
app.config.load_config('./etc/api.ini')

plugin = bottle_sqlite.Plugin(app.config['sqlite.timelines'])
app.install(plugin)

logging.config.fileConfig(app.config['logging.config'])


def json_error_handler(res):
    if res.content_type == 'application/json':
          return res.body
    res.content_type = 'application/json'
    if res.body == 'Unknown Error.':
          res.body = bottle.HTTP_CODES[res.status_code]
    return bottle.json_dumps({'errors': res.body})
    

app.default_error_handler = json_error_handler


if not sys.warnoptions:
    import warnings
    for warning in [DeprecationWarning, ResourceWarning]:
          warnings.simplefilter('ignore', warning)
          

def query(db, sql, args=(), one=False):
    cur = db.execute(sql, args)
    rv = [dict((cur.description[idx][0], value)
               for idx, value in enumerate(row))
          for row in cur.fetchall()]
    cur.close()

    return (rv[0] if rv else None) if one else rv


def execute(db, sql, args=()):
    cur = db.execute(sql, args)
    id = cur.lastrowid
    cur.close()

    return id
    
    
@post('/posts')
def postTweet(username, text):
    post = request.json

    if not post:
        abort(400)

    posted_fields = post.keys()
    required_fields = {'username', 'text'}
    
    if not required_fields <= posted_fields:
        abort(400, f'Missing fields: {required_fields - posted_fields}')

    try:
        user['id'] = execute(db,
                             '''INSERT INTO users(username, password, emailAddress) VALUES (:username, :password, :emailAddress)''', user)

    except sqlite3.IntegrityError as e:
        abort(409, str(e))

    response.status = 201
    response.set_header('Location', f"/users/{user['username']}/{user['password']}")
    return user


