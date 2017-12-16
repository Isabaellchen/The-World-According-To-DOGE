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
        d = datetime.datetime.now()
        year = d.year
        month = 'Jan'
        
        # shifted by one month to accomodate update cycles
        if (d.month > 7):
            month = 'Jul'
        elif (d.month < 2):
            month = 'Jul'
            year = d.year - 1
        
        url = 'http://infographics.economist.com/{}/databank/BMFile2000to{}{}.xls'\
            .format(year,month,year)
            
        xls_file = requests.get(url)
        
        with open(self.temp_file, 'wb') as file:
            file.write(xls_file.content)
            
        
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
        

index = BigMacIndex()

if __name__ == '__main__':
    index.update_index()