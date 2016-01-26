# -*- coding: utf-8 -*-
"""
    The World According To Doge
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    A micro web app to display prices of Bigmacs 
    (and maybe other things) in different countries in Dogecoin.
    See more at dogecoin.com or reddit.com/r/dogecoin
    
    Author /u/Isabaellchen
"""

import os
import datetime
from sqlite3 import dbapi2 as sqlite3
from contextlib import closing
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
app = Flask(__name__)

# Define configs

class Config(object):
    DEBUG = False
    TESTING = False
    DATABASE_URI = 'sqlite://:memory:'

class ProductionConfig(Config):
    DATABASE_URI = 'mysql://user@localhost/foo'

class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE = os.path.join(app.root_path, 'twatdoge.db')
    SECRET_KEY = 'meinr00tkey'
    USERNAME = 'admin'
    PASSWORD = 'admin'

class TestingConfig(Config):
    TESTING = True
    DATABASE = os.path.join(app.root_path, 'twatdoge.db')
    SECRET_KEY = 'meinr00tkey'
    USERNAME = 'admin'
    PASSWORD = 'admin'

# Load config
app.config.from_object('twatdoge.DevelopmentConfig')

# DB Methods

def connect_db():
    con = sqlite3.connect(app.config['DATABASE'])
    con.row_factory = sqlite3.Row
    return con
    

def get_db():
    if not hasattr(g, 'db'):
        g.db = connect_db()
    return g.db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'db'):
        g.db.close()


# This method can be called from the python command prompt

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

''' 
These methods are request wrapper methods. 
The same functionality is used in the app context.
We now have to call get_db() each time we resolve a route


@app.before_request
def before_request():
    get_db()


@app.teardown_request
def teardown_request():
    if not hasattr(g, 'db')::
        g.db.close()
'''

# Routes & views

@app.route('/')
def show_prices():
    db = get_db()
    cur = db.execute('select name, factor, updated_at from prices order by id desc')
    prices = cur.fetchall()
    return render_template('show_prices.html', prices=prices)


@app.route('/add', methods=['POST'])
def add_price():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('insert into prices (name, factor, updated_at) values (?, ?, ?)',
               [request.form['name'], request.form['factor'], datetime.datetime.now()])
    db.commit()
    flash('New price was successfully added')
    return redirect(url_for('show_prices'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_prices'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_prices'))
    
if __name__ == '__main__':
    app.run()
