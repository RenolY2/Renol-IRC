import time
import datetime
import Queue

##  TODO:   Write a Logger so the bot can log any errors it encounters without
##          resulting in a crash.  

class WarningLogger():
    def __init__(self):
        self.warning_queue = Queue.Queue()
        


