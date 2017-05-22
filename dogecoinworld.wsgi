activate_this = '/home/twatdoge/TWATDoge/venv/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))
    
from twatdoge import app as application