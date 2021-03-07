import sys
import textwrap
import logging.config
import sqlite3

import bottle
import bottle_sqlite
from bottle import get, post, delete, error, abort, request, response, HTTPResponse

# conn = sqlite3.connect('users.db')
# conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username string UNIQUE NOT NULL, password string NOT NULL, emailAddress string UNIQUE)")
# conn.execute("CREATE TABLE followers (id INTEGER PRIMARY KEY, username string NOT NULL, usernameToFollow string NOT NULL)")

app = bottle.default_app()
app.config.load_config('./etc/api.ini')

plugin = bottle_sqlite.Plugin(app.config['sqlite.dbfile'])
app.install(plugin)

logging.config.fileConfig(app.config['logging.config'])


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
def getAll(db):
    users = query(db, 'SELECT * FROM users')
    return {'users': users}


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
                             '''INSERT INTO users(username, password, emailAddress) VALUES (:username, :password, :emailAddress)''',
                             user)

    except sqlite3.IntegrityError as e:
        abort(409, str(e))

    response.status = 201
    response.set_header('Location', f"/users/{user['username']}/{user['password']}")
    return user


@post('/users/<username>/<password>')
def checkPassword(db, username, password):
    db_password = query(db, 'SELECT password FROM users WHERE username=?', [username])
    if db_password != [] and db_password[0]['password'] == password:
        response.status = 200
        return {'Authentication': True}
    else:
        response.status = 401
        return {'Authentication': False}


@post('/users/<username>/<usernameToFollow')
def addFollower(db, username, usernameToFollow):
    try:
        execute(db,
                '''INSERT INTO followers(username, usernameToFollow) VALUES (''' + username + ''', ''' + usernameToFollow + ''')''')

    except sqlite3.IntegrityError as e:
        abort(409, str(e))

    response.status = 201


@delete('/users/<username>/<usernameToDelete>')
def removeFollower(db, username, usernameToRemove):
    execute(db,
            '''DELETE FROM followers WHERE username = ''' + username + ''' AND usernameToFollow =  ''' + usernameToRemove + ''')''')
    # add exception later

    response.status = 200
