import sys
from datetime import datetime

# Todo - Timestamps - process name
class Logger(object):
    def __init__(self, filename="log"):
        self.terminal = sys.stdout
        self.filename = filename
    def write(self, message):
        self.log = open(self.filename, "a")
        date = '[%s] - ' % (str(datetime.now())) + message
        self.log.write(date)
        self.log.close()
