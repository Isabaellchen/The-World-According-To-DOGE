import xlrd
import requests
import datetime

class BigMacIndex(object):
    
    temp_file = 'temp.xls'
    
    def update_index():
        xls_file = requests.get(self.get_url())
        with open(self.temp_file, 'wb') as file:
            file.write(xls_file.content)
        book = xlrd.open_workbook(self.temp_file)
        sheet = book.sheet_by_index(0)
        
    def get_url():
        d = datetime.datetime.now()
        url = 'http://infographics.economist.com/{}/databank/BMfile2000to{}{}.xls'\
            .format(d.year,d.strftime("%b"),d.year)
        return url