import xlrd
import requests
import datetime
import pycountry

class BigMacIndex(object):
    
    temp_file = 'temp.xls'
    prices = {}
    
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
                abbreviation = "un"
            self.prices[name] = (float(sheet.cell_value(row, 3)), 'images/flags/' + abbreviation + '.png')
        return self.prices