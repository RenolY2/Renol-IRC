import sqlite3
#from datetime import datetime
import time

class MemoDB():
    def __init__(self, filename):
        self.conn = sqlite3.connect(filename)

        self.cursor = self.conn.cursor()

        self.cursor.execute("""
                            CREATE TABLE IF NOT EXISTS Memo
                            (memoID INTEGER PRIMARY KEY AUTOINCREMENT,
                            date TEXT, author TEXT, target TEXT, channel TEXT, memoText TEXT);
                            """)
        
    def addMessage(self, name, target, channel, message):
        self.cursor.execute("""
                            INSERT INTO Memo(date, author, target, channel, memoText)
                            VALUES (?, ?, ?, ?, ?)
                            """, (create_date(), 
                                  name, target.lower(), channel, message))
        self.conn.commit()
    
    def removeMessage(self, rowID):
        self.cursor.execute("""
                            DELETE FROM Memo
                            WHERE memoID = ?
                            """, (rowID, ))
        
        self.conn.commit()
    
    def getLatestMessage(self):
        self.cursor.execute("""
                            SELECT memoID, date, author, target, memoText FROM Memo
                            ORDER BY memoID DESC
                            """)
        return self.cursor.fetchone()
    
    def removeAllMessages_toUser(self, target, channel):
        self.cursor.execute("""
                            DELETE FROM Memo
                            WHERE target = ? AND channel = ?
                            """, (target.lower(), channel))
        self.conn.commit()
     
    def getOneMessage_toUser(self, target, channel):
        self.cursor.execute("""
                            SELECT memoID, date, author, target, memoText FROM Memo
                            WHERE target = ? AND channel = ?
                            """, (target.lower(), channel))
        
        return self.cursor.fetchone()
    
    def getAllMessages_toUser(self, target, channel):
        self.cursor.execute("""
                            SELECT memoID, date, author, target, memoText FROM Memo
                            WHERE target = ? AND channel = ?
                            """, (target.lower(), channel))
        
        return self.cursor.fetchall()
    
    def getMsgCount_toUser(self, target, channel):
        self.cursor.execute("""
                            SELECT Count(*) FROM Memo
                            WHERE target = ? AND channel = ?
                            """, (target.lower(), channel))
        
        return self.cursor.fetchone()
    
    def clearDB(self):
        self.cursor.execute("""
                            DELETE FROM Memo
                            """)
        self.conn.commit()
        
    def clearDB_channel(self, channel):
        self.cursor.execute("""
                            DELETE FROM Memo
                            WHERE channel = ?
                            """, (channel, ))
        self.conn.commit()
    
def create_date():
    gm_time = time.gmtime()
    datetimestring = time.strftime("%I:%M%p, {0} of %B %Y (UTC+0)", gm_time) 
    day = time.strftime("%d", gm_time)
    day = day.lstrip("0")

    return datetimestring.format(format_day_of_month(day))
    
def choose_st_nd_rd_th(number):
    if number.endswith("1"):
        return "st"
    elif number.endswith("2"):
        return "nd"
    elif number.endswith("3"):
        return "rd"
    else:
        return "th"

def format_day_of_month(day):
    if len(day) > 1:
        if day[-2] == "1":
            return day + "th"
        else:
            return day + choose_st_nd_rd_th(day)
    else:
        return day + choose_st_nd_rd_th(day)