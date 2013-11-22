import imp, os
import Queue

import centralizedThreading
from BotEvents import TimerEvent, MsgEvent
from IRC_registration import trackVerification


class commandHandling():
    def __init__(self, channels, cmdprefix, name, ident, adminlist):
        self.name = name
        self.ident = ident
        self.Plugin = self.__LoadModules__("IRCpackets")
        self.commands = self.__LoadModules__("commands")
        
        print adminlist
        self.bot_userlist = adminlist
        self.Bot_Auth = trackVerification(adminlist)
        
        self.channels = channels
        self.channelData = {}
        
        self.topic = {}
        self.cmdprefix = cmdprefix
        
        self.events = {"time" : TimerEvent(), "chat" : MsgEvent()}
        self.server = None
        
        self.latency = None
        
        self.PacketsReceivedBeforeDeath = Queue.Queue(maxsize = 25)
        
        self.threading = centralizedThreading.ThreadPool()
        
        
    def handle(self, send, prefix, command, params, auth, ):
        self.send = send
        
        ## In the next few lines I implement a basic logger so the logs can be put out when the bot dies.
        ## Should come in handy when looking at what or who caused trouble
        ## There is room for 25 entries, number can be increased at a later point
        try:
            self.PacketsReceivedBeforeDeath.put("{0} {1} {2}".format(prefix, command, params), False)
        except Queue.Full:
            self.PacketsReceivedBeforeDeath.get(block = False)
            self.PacketsReceivedBeforeDeath.put("{0} {1} {2}".format(prefix, command, params), False)
        
        
        if command == "376":
            self.auth = auth
        
        try:
            self.Plugin[command][0].execute(self, send, prefix, command, params)
        except KeyError as error:
            #print "Unknown command '"+command+"'"
            print "Unimplemented Packet or missing channel: "+str(error)
    
    def timeEventChecker(self):
        self.events["time"].tryAllEvents(self)
    
    def userGetRank(self, channel, username):
        #print self.channelData[channel]["Userlist"]
        for user in self.channelData[channel]["Userlist"]:
            if user[0].lower() == username.lower():
                return user[1]
            
    def retrieveTrueCase(self, channel):
        for chan in self.channelData:
            if chan.lower() == channel.lower():
                return chan
        return False
    
    def sendMessage(self, channel, msg, msgsplitter = None, splitAt = " "):
        self.sendChatMessage(self.send, channel, msg, msgsplitter, splitAt)
    
    def sendChatMessage(self, send, channel, msg, msgsplitter = None, splitAt = " "):
        # we calculate a max length value based on what the server would send to other users 
        # if this bot sent a message.
        # Private messages from the server look like this:
        # nick!user@hostname PRIVMSG target :Hello World!
        # For the purpose of this bot, nick and user are the same, and target is the channel 
        # to which we send the message. At the end, we add a constant (25) to the length to account
        # for whitespaces and other characters and eventual oddities. 
        # The Hostname will be limited to 63, regardless of the actual length.
        
        # if you want to create your own tweaked message splitter, 
        # provide it as the fourth argument to self.sendChatMessage
        # otherwise, the default one, i.e. self.defaultsplitter, is used
        if msgsplitter == None:
            msgsplitter = self.defaultsplitter
                                                      #PRIVMSG
        prefixLen = len(self.name) + len(self.ident) + 63 + 7 + len(channel) + 25
        remaining = 512-prefixLen
        #print remaining
        
        if len(msg)+prefixLen > 512:
            msgpart = msgsplitter(msg, remaining, splitAt)
            
            for part in msgpart:
                send("PRIVMSG "+str(channel)+" :"+str(part), 5)
        else:
            send("PRIVMSG "+str(channel)+" :"+str(msg), 5)
    
    def sendNotice(self, destination, msg, msgsplitter = None, splitAt = " "):
        # Works the same as sendChatMessage
        # Only difference is that this message is sent as a NOTICE
        if msgsplitter == None:
            msgsplitter = self.defaultsplitter
                                                            #NOTICE
        prefixLen = len(self.name) + len(self.ident) + 63 + 6 + len(destination) + 25
        remaining = 512-prefixLen
        #print remaining
        
        if len(msg)+prefixLen > 512:
            msgpart = msgsplitter(msg, remaining, splitAt)
            
            for part in msgpart:
                self.send("NOTICE "+str(destination)+" :"+str(part))
        else:
            self.send("NOTICE "+str(destination)+" :"+str(msg))
        
    def defaultsplitter(self, msg, length, splitAt):
        
        start = 0
        end = length
        items = []
        
        
        while end <= len(msg):
            splitpos = msg[start:end].rfind(splitAt)
    
            # case 1: whitespace has not been found, ergo: 
            # message is too long, so we split it at the position specified by 'end'
            if splitpos < 0: 
                items.append(msg[start:end])
                start = end
            # case 2: whitespace has been found, ergo:
            # we split it at the whitespace
            # splitpos is a value local to msg[start:end], so we need to add start to it to get a global value
            else:
                items.append(msg[start:start+splitpos])
                start = start+splitpos+len(splitAt)
                
            end = start + length
        
        # Check if there is any remaining data
        # If so, append the remaining data to the list
        if start < len(msg):
            items.append(msg[start:])
        
        # remove all empty strings in the list because they are not needed nor desired
        for i in range(items.count("")):
            items.remove("")
                
        return items
    
    def joinChannel(self, send, channel):
        if isinstance(channel, str):
            if channel not in self.channelData:
                #self.channels.append(channel)
                self.channelData[channel] = {"Userlist" : [], "Topic" : "", "Mode" : ""}
                
            send("JOIN "+channel, 5)
        elif isinstance(channel, list):
            for chan in channel:
                if chan not in self.channelData:
                    #self.channels.append(channel)
                    self.channelData[chan] = {"Userlist" : [], "Topic" : "", "Mode" : ""}
            send("JOIN "+",".join(channel), 3)
        else:
            raise TypeError
        print self.channelData
    
    def whoisUser(self, user):
        self.send("WHOIS {0}".format(user))
        self.Bot_Auth.queueUser(user)
    
    def userInSight(self, user):
        print self.channelData
        for channel in self.channelData:
            for userD in self.channelData[channel]["Userlist"]:
                if user == userD[0]:
                    return True
                
        
        return False
    
    def __ListDir__(self, dir):
        files = os.listdir(dir)
        newlist = []
        for i in files:
            if ".pyc" not in i and "__init__" not in i and "conflicted copy" not in i and ".py" in i:
                newlist.append(i)
                
        return newlist
    
    def __LoadModules__(self,path):     
        ModuleList = self.__ListDir__(path)
        Packet = {}
        for i in ModuleList:
            module = imp.load_source(i[0:-2], path+"/"+i)
            Packet[module.ID] = (module, path+"/"+i)
            
            try:
                if not callable(module.__initialize__):
                    module.__initialize__ = False
            except AttributeError:
                module.__initialize__ = False
                
            Packet[module.ID] = (module, path+"/"+i)
            #Packet[i[1].lower()].PATH = path + "/"+i[2]
            #self.Packet[i[1]] = self.Packet[i[1]].EXEC()
        
        print "ALL MODULES LOADED"   
        return Packet