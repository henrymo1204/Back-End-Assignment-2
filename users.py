import sys
import textwrap
import logging.config
import sqlite3

import bottle
import bottle_sqlite
from bottle import get, post, delete, error, abort, request, response, HTTPResponse


# conn = sqlite3.connect('users.db')
# conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username string UNIQUE NOT NULL, password string NOT NULL, emailAddress string UNIQUE)")
# conn.execute("CREATE TABLE followers (id INTEGER PRIMARY KEY, user_id string NOT NULL, user_idToFollow string NOT NULL, FOREIGN KEY(user_id) REFERENCES users(id), FOREIGN KEY(user_idTOFOllow) REFERENCES users(id))")

app = bottle.default_app()
app.config.load_config('./etc/users.ini')

plugin = bottle_sqlite.Plugin(app.config['sqlite.users'])
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


@get('/users/')
def getUsers(db):
    users = query(db, 'SELECT * FROM users')
    return {'users': users}


@get('/followers/')
def getFollowers(db):
    followers = query(db, 'SELECT * FROM followers')
    return {'followers': followers}


@post('/users')
def create_user(db):
    user = request.json

    if not user:
        abort(400)

    posted_fields = user.keys()
    required_fields = {'username', 'password', 'emailAddress'}

    if not required_fields <= posted_fields:
        abort(400, f'Missing fields: {required_fields - posted_fields}')

    try:
        user['id'] = execute(db,
                             '''INSERT INTO users(username, password, emailAddress)
                             VALUES (:username, :password, :emailAddress)''', user)

    except sqlite3.IntegrityError as e:
        abort(409, str(e))

    response.status = 201
    return user


@post('/users/<username>/password')
def checkPassword(db, username):
    password = request.json

    if not password:
        abort(400)

    posted_fields = password.keys()
    required_fields = {'password'}

    if not required_fields <= posted_fields:
        abort(400, f'Missing fields: {required_fields - posted_fields}')

    db_password = query(db, 'SELECT password FROM users WHERE username=?', [username])
    if db_password != [] and db_password[0]['password'] == password['password']:
    	response.status = 200
    	return {'Authentication': True}
    else:
    	response.status = 401
    	return {'Authentication': False}


@post('/followers')
def addFollower(db):
    follower = request.json
    if not follower:
        abort(400)

    posted_fields = follower.keys()
    required_fields = {'user_id', 'user_id_to_follow'}

    if not required_fields <= posted_fields:
        abort(400, f'Missing fields: {required_fields - posted_fields}')

    try:
        follower['id'] = execute(db, '''INSERT INTO followers(user_id, user_id_to_follow) VALUES (:user_id, :user_id_to_follow)''', follower)

    except sqlite3.IntegrityError as e:
        abort(409, str(e))

    response.status = 201
    return follower


@delete('/followers')
def removeFollower(db):
    follower = request.json

    if not follower:
        abort(400)

    posted_fields = follower.keys()
    required_fields = {'user_id', 'user_id_to_remove'}

    username = follower['user_id']
    userToFollow = follower['user_id_to_remove']

    if not required_fields <= posted_fields:
        abort(400, f'Missing fields: {required_fields - posted_fields}')

    try:
        execute(db, '''DELETE from followers where user_id=? and user_id_to_follow=?''', (username, userToFollow))
        message = { 'Status' : '200 OK'}
    except sqlite3.IntegrityError as e:
        abort(409, str(e))

    return message
