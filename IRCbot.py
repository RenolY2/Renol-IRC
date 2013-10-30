import warnings
warnings.simplefilter("ignore", RuntimeWarning)

import socket
import time
import re
import sys
import threading
import traceback
import Queue
import datetime
import getpass

from IRC_readwrite_threads import IRC_reader, IRC_writer, ThreadShuttingDown
from commandHandler import commandHandling
from configReader import Configuration

class IRC_Main():
    def __init__(self, host, port, name, passw, channels, myident, prefix = "=", adminlist = []):
        self.host = host
        self.port = port
        self.name = name
        self.passw = passw
        self.channels = channels
        self.myident = myident
        
        self.adminlist = adminlist
        
        self.serverConn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverConn.settimeout(300)
        
        self.nsAuth = False
        
        self.shutdown = False
        self.prefix = prefix
        
    def start(self):
        self.serverConn.connect((self.host, self.port))

        self.readThread = IRC_reader(self.serverConn)
        self.writeThread = IRC_writer(self.serverConn)
        
        self.readThread.start()
        self.writeThread.start()
        

        state = 1
        
        self.writeThread.sendMsg('PASS ' + self.passw, 0)
        self.writeThread.sendMsg('NICK ' + self.name, 0)
        self.writeThread.sendMsg('USER '+ self.myident + ' '+self.passw+' '+"HOST"+' '+self.host, 0)
        
        self.comHandle = commandHandling(self.channels, self.prefix, self.name, self.myident, self.adminlist)
        
        while self.shutdown == False:
            
            try:
                msg = self.readThread.readMsg()
                
                msgParts = msg.split(" ", 2)
                
                #print msgParts
                
                if msgParts[0][0] == ":":
                    prefix = msgParts[0][1:]
                else:
                    prefix = None
                
                if prefix == None:
                    command = msgParts[0]
                    
                    try:
                        commandParameters = msgParts[1]
                    except IndexError:
                        commandParameters = ""
                else:
                    command = msgParts[1]
                    try:
                        commandParameters = msgParts[2]
                    except IndexError:
                        commandParameters = ""
                
                
                #print "HEY", command, commandParameters
                self.comHandle.handle(self.writeThread.sendMsg, prefix, command, commandParameters, self.nsAuth)
                
                #if msg[0:4] == "PING":
                #    hash = msg[5:]
                #    writeThread.sendMsg("PONG "+hash, 0)
                
                #print msg
            except Queue.Empty:
                pass
            
            # Bugfix for when only the writeThread, i.e. the one that sends data to server, dies
            # we raise an exception so the main loop exits and the readThread is shut down too
            if self.writeThread.ready == False:
                raise ThreadShuttingDown("writeThread", time.time())
            
            self.comHandle.timeEventChecker()
            
            
            
            time.sleep(0.001)
        self.readThread.ready = False
        self.writeThread.ready = False
        
    def customNickAuth(self, result):
        if isinstance(result, str): 
            self.nsAuth = result
        else:
            raise TypeError
        
startFile = open("lastStart.txt", "w")  
startFile.write("Started at: "+str(datetime.datetime.today()))
startFile.close()              

config = Configuration()
if not config.doesExist():
    print "config.txt is missing, please input the information."
    
    dat = {}
    dat["server"] = raw_input("Server IP or address: ")
    dat["port"] = raw_input("Server port (default is 6667): ")
    dat["usernick"] = raw_input("Nickname: ")
    dat["pass"] = getpass.getpass("Password (for authentication with nickserv, if server supports it): ")
    dat["ident"] = raw_input("Identification string (can be the same as the Nickname, server will prepend): ")
    dat["channels"] = raw_input("Channels (if you want to join several channels, delimit with a comma): ")
    dat["prefix"] = raw_input("Command Prefix: ")
    dat["admins"] = raw_input("Admins (which users should have elevated rights on the bot? If more than one, delimit with a comma): ")
    
    config.createNewConfig(dat)
    
config.loadConfig()
dat = config.config
    
 
bot = IRC_Main(dat["server"], int(dat["port"]), dat["usernick"], dat["pass"], config.getChannels(), dat["ident"], dat["prefix"], config.getAdmins())   

try:
    bot.start()
except Exception as error:
    print "OH NO I DIED: "+str(error)
    traceb = str(traceback.format_exc())
    print traceb
    excFile = open("exception.txt", "w")
    excFile.write("Oh no! The bot died! \n"+str(traceb)+"\nTime of death: "+str(datetime.datetime.today())+"\n")
    excFile.write("-----------------------------------------------------\n")
    
    # Check if the attribute 'comhandle' is contained in 'bot'. If so, proceed with playback of packet log.
    # This is for the cases where the program crashes while comHandle is being initialized, resulting
    # in comHandle missing afterwards.
    if getattr(bot, "comHandle", None) != None: 
        for i in range(bot.comHandle.PacketsReceivedBeforeDeath.qsize()):
            excFile.write(bot.comHandle.PacketsReceivedBeforeDeath.get(block = False)+"\n")
        
    excFile.write("-----------------------------------------------------\n")
    excFile.close
    
    bot.comHandle.threading.sigquitAll()
    
    bot.readThread.ready = False
    #bot.writeThread.waitUntilEmpty()
    bot.writeThread.signal = True
    #raise error
