from lxml import html
import requests

class Coinmarketcap(object):
    
    url = 'http://coinmarketcap.com/all/views/all/'
    
    def getDogeValue(self):
        page = requests.get(self.url)
        tree = html.fromstring(page.content)
        usd_price = tree.xpath('//tr[@id="id-dogecoin"]/td//a[@class="price"]/@data-usd')
        btc_price = tree.xpath('//tr[@id="id-dogecoin"]/td//a[@class="price"]/@data-btc')
        return ( self.invertDogeValue(float(usd_price[0])), self.invertDogeValue(float(btc_price[0])) )
        
    def invertDogeValue(self, value):
        return 1 / value