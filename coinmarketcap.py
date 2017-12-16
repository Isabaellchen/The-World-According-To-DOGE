from lxml import html
import requests
import datetime
from pytz import timezone
import pytz


class Coinmarketcap(object):
    
    url = 'http://coinmarketcap.com/all/views/all/'
        
    def getCurrentValue(self, symbol):
        tz = timezone('Europe/Berlin')
        raw_date = tz.normalize(tz.localize(datetime.datetime.now())).astimezone(pytz.utc)
        timestamp = int(raw_date.timestamp())
        
        page = requests.get(self.url)
        tree = html.fromstring(page.content)
        value = tree.xpath('//tr[@id="id-dogecoin"]/td//a[@class="price"]/@data-' + symbol)
        float_value = float(value[0])
        return {'value': 1 / float_value, 'cvalue' : float_value, 'utc': timestamp}