import sqlite3
from flask import Flask
from flask import g

app = Flask(__name__)

@app.route('/')
def getstuff():
    return 'hello world'
   # return  get_users()
	#(get_RFID())

DATABASE = 'Siip.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def get_users():
    return get_db().execute("select * from users;")

def get_RFID():
    return get_db().execute("select * from RFID;")

if __name__ == '__main__':
    app.run()

