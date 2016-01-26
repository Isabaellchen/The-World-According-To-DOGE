from lxml import html
import requests

class Coinmarketcap(object):
    
    url = 'http://coinmarketcap.com/all/views/all/'
    
    def getDogeValue():
        page = requests.get(self.url)
        tree = html.fromstring(page.content)
        price = tree.xpath('//tr[@id="id-dogecoin"]/td//a[@class="price"]/@data-usd
        ')
        return price[0]