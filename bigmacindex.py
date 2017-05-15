import xlrd
import requests
import datetime
import pycountry

from random import randrange

class BigMacIndex(object):
    
    temp_file = 'temp.xls'
    prices = {}
    country_exception = {
            'Britain': 'gb',
            'Euro area': 'eu',
            'Czech Republic': 'cz',
            'Russia': 'ru',
            'South Korea': 'kr',
            'Taiwan': 'tw',
            'UAE': 'ae',
            'Venezuela': 've',
            'Vietnam': 'vn'
        }
    
    def update_index(self):
        xls_file = requests.get(self.get_url())
        with open(self.temp_file, 'wb') as file:
            file.write(xls_file.content)
        
    def get_url(self):
        d = datetime.datetime.now()
        url = 'http://infographics.economist.com/{}/databank/BMfile2000to{}{}.xls'\
            .format(d.year,d.strftime("%b"),d.year)
        return url
        
    def read_index(self, timerange = 0):
        book = xlrd.open_workbook(self.temp_file)
        sheet = book.sheet_by_index(timerange)
        for row in range(1,sheet.nrows):
            name = sheet.cell_value(row, 0)
            try:
                country = pycountry.countries.get(name=name)
                abbreviation = str(country.alpha_2).lower()
            except KeyError:
                abbreviation = self.country_exception[name]
                
            rnd_burger_num = str(randrange(1,6))
                
            final_value = float(sheet.cell_value(row, 3))
            flag_path = 'images/flags/' + abbreviation + '.png'
            bigmac_path = 'images/bigmacs/bigmac' + rnd_burger_num + '.png'
            name_rotation = str(randrange(-5,5))
                
            self.prices[name] = (final_value, flag_path, bigmac_path, name_rotation)
        return self.prices