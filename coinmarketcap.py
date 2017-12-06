from lxml import html
import requests

class Coinmarketcap(object):
    
    url = 'http://coinmarketcap.com/all/views/all/'
    
    def parseCMCPage(self):
        page = requests.get(self.url)
        return html.fromstring(page.content)
        
    def invertDogeValue(self, value):
        return 1 / value
        
    def getUSDValue(self):
        tree = self.parseCMCPage()
        usd_price = tree.xpath('//tr[@id="id-dogecoin"]/td//a[@class="price"]/@data-usd')
        return self.invertDogeValue(float(usd_price[0]))
        
    def getBTCValue(self):
        tree = self.parseCMCPage()
        btc_price = tree.xpath('//tr[@id="id-dogecoin"]/td//a[@class="price"]/@data-btc')
        return self.invertDogeValue(float(btc_price[0]))