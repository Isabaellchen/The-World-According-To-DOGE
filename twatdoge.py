# -*- coding: utf-8 -*-
"""
    The World According To Doge
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    A micro web app to display prices of Bigmacs 
    (and maybe other things) in different countries in Dogecoin.
    See more at dogecoin.com or reddit.com/r/dogecoin
    
    Author /u/Isabaellchen
"""

import datetime
from coinmarketcap import Coinmarketcap
from bigmacindex import BigMacIndex
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from flask.ext.cache import Cache

app = Flask(__name__)

cache = Cache(app,config={'CACHE_TYPE': 'simple'})
cache.init_app(app)

# Define configs

class Config(object):
    DEBUG = False
    TESTING = False
    PROD = False

class ProductionConfig(Config):
    PROD = True

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True

# Load config
app.config.from_object('twatdoge.DevelopmentConfig')

# DB Methods

@cache.cached(timeout=3600)
@app.route('/')
def show_prices():
    prices = BigMacIndex().read_index()
    values = Coinmarketcap().getDogeValue()
    return render_template('show_prices.html', prices=prices, usd_value=values[0], btc_value=values[1])


    
if __name__ == '__main__':
    app.run()
