import xlrd
import requests
import datetime

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
        for row in range(sheet.nrows):
            self.prices[sheet.cell_value(row, 0)] = sheet.cell_value(row, 3)
        return self.prices