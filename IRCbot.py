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
import logging

from IRC_readwrite_threads import IRC_reader, IRC_writer, ThreadShuttingDown
from commandHandler import commandHandling
from configReader import Configuration

class IRC_Main():
    def __init__(self, config):
        self.host = config.config["server"]
        self.port = int(config.config["port"])
        self.name = config.config["usernick"]
        self.passw = config.config["pass"]
        self.channels = config.getChannels()
        self.myident = config.config["ident"]
        
        self.adminlist = config.getAdmins()
        
        self.nsAuth = False
        
        self.shutdown = False
        self.prefix = config.config["prefix"]
        
        self.loglevel = config.config["loglevel"]
        
    def start(self):
        self.serverConn = socket.create_connection((self.host, self.port), 300) 
        
        self.readThread = IRC_reader(self.serverConn)
        self.writeThread = IRC_writer(self.serverConn)
        
        self.readThread.start()
        self.writeThread.start()
        
        self.writeThread.sendMsg('PASS ' + self.passw, 0)
        self.writeThread.sendMsg('NICK ' + self.name, 0)
        self.writeThread.sendMsg('USER '+ self.myident + ' '+self.passw+' '+"HOST"+' '+self.host, 0)
        
        self.comHandle = commandHandling(self.channels, self.prefix, self.name, self.myident, self.adminlist, self.loglevel)
        
        peerinfo = self.serverConn.getpeername()
        clientinfo = self.serverConn.getsockname()
        
        self.__root_logger__ = logging.getLogger("IRCMainLoop")
        
        self.__root_logger__.info("Connected to %s (IP address: %s, port: %s)",self.host, peerinfo[0], peerinfo[1])
        self.__root_logger__.debug("Local IP: %s, local port used by this connection: %s", clientinfo[0], clientinfo[1])
        
        self.__root_logger__.info("BOT IS NOW ONLINE: Starting listening for server responses.")
        
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
                
            except Queue.Empty:
                pass
            
            # Bugfix for when only the writeThread, i.e. the one that sends data to server, dies
            # we raise an exception so the main loop exits and the readThread is shut down too
            if self.writeThread.ready == False:
                self.__root_logger__.critical("Write Thread was shut down, raising exception.")
                raise ThreadShuttingDown("writeThread", time.time())
                
            
            self.comHandle.timeEventChecker()
            
            
            
            time.sleep(0.0012)
            
        self.__root_logger__.info("Main loop has been stopped")
        self.readThread.ready = False
        self.writeThread.ready = False
        self.__root_logger__.info("Read and Write thread signaled to stop.")
        
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
    dat["ident"] = raw_input("Identification string (can be the same as the Nickname): ")
    dat["channels"] = raw_input("Channels (if you want to join several channels, delimit with a comma): ")
    dat["prefix"] = raw_input("Command Prefix: ")
    dat["admins"] = raw_input("Admins (which users should have elevated rights on the bot? If more than one, delimit with a comma): ")
    dat["loglevel"] = raw_input("Which is the least severe type of log messages that should still be logged? \n"
                                "(starting with the least severe, one of NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL (INFO is recommended))")
    
    config.createNewConfig(dat)
    
config.loadConfig()
dat = config.config
    
 
bot = IRC_Main(config)   

try:
    bot.start()
except Exception as error:
    bot.__root_logger__.exception("The bot has encountered an exception and had to shut down.")
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
        bot.comHandle.threading.sigquitAll()
        bot.__root_logger__.debug("All threads were signaled to shut down.")
        
    excFile.write("-----------------------------------------------------\n")
    excFile.write("ReadThread Exception: \n")
    excFile.write(str(bot.readThread.error)+" \n")
    bot.__root_logger__.info("Exception encountered by ReadThread (if any): %s\n", str(bot.readThread.error))
    excFile.write("-----------------------------------------------------\n")
    excFile.write("WriteThread Exception: \n")
    excFile.write(str(bot.writeThread.error)+" \n")
    bot.__root_logger__.info("Exception encountered by WriteThread (if any): %s\n", str(bot.writeThread.error))
    
    excFile.close
    
    
    
    bot.readThread.ready = False
    #bot.writeThread.waitUntilEmpty()
    bot.writeThread.signal = True
    #raise error
bot.__root_logger__.info("End of Session\n\n\n\n")
logging.shutdown()