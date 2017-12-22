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
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, jsonify
from flask.ext.cache import Cache

app = Flask(__name__)

cache = Cache(app, config={'CACHE_TYPE': 'simple'})
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
app.config.from_object('twatdoge.ProductionConfig')

accepted_symbols = ['USD', 'BTC']

BigMacIndex.update_index(BigMacIndex)

@app.route('/')
@cache.cached(timeout=300)
def main():
	template_data = {
		'prices': BigMacIndex().read_index(),
		'currencies': {symbol: Coinmarketcap().getCurrentValue(symbol.lower()) for symbol in accepted_symbols}
	}

	return render_template('main.html', **template_data)


@app.route('/price/<currency>')
@cache.cached(timeout=300)
def price_service(currency):
	if currency in accepted_symbols:
		return jsonify(Coinmarketcap().getCurrentValue(currency.lower()))
	else:
		return 404


@app.route('/qr/')
@cache.cached(timeout=300)
def qr_display():
	return render_template('qr_display.html')


@app.route('/send')
def send():
	url = url_for('qr_display') + '#' + request.values.get('address') + '/' + request.values.get('amount') + '/' + request.values.get('currency')
	return redirect(url, code=302)


if __name__ == '__main__':
	app.run()
