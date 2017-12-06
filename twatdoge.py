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

    
@cache.cached(timeout=600, key_prefix='usd_value')
def cached_usd_value():
    return Coinmarketcap().getUSDValue()
    
    
@cache.cached(timeout=600, key_prefix='btc_value')
def cached_btc_value():
    return Coinmarketcap().getBTCValue()


@app.route('/')
@cache.cached(timeout=600)
def show_prices():
    prices = BigMacIndex().read_index()
    usd_value = cached_usd_value()
    btc_value = cached_btc_value()
    return render_template('show_prices.html', prices=prices, usd_value=usd_value, btc_value=btc_value)
    
    
@app.route('/price/<currency>')
@cache.cached(timeout=600)
def price_service(currency):
    return {
        'USD': str(cached_usd_value()),
        'BTC': str(cached_btc_value())
    }.get(currency, ('', 404))
    
@app.route('/qr/')
@cache.cached(timeout=600)
def qr_display():
    return render_template('qr_display.html')
    
    
if __name__ == '__main__':
    app.run()
