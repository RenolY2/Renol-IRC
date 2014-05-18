ID = "PART"

def execute(self, sendMsg, prefix, command, params):
    print "SOMEBODY LEFT CHANNEL:"
    print prefix
    print params
    
    part1 = prefix.partition("!")
    part2 = part1[2].partition("@")
    
    name = part1[0]
    ident = part2[0]
    host = part2[2]
    
    print "CHANNEL LEAVE"
        
    chan = self.retrieveTrueCase(params)
    
    self.events["channelpart"].tryAllEvents(self, name, ident, host, chan)
            
    if chan != False:
        for i in range(len(self.channelData[chan]["Userlist"])):
            user, pref = self.channelData[chan]["Userlist"][i]
            if user == name:
                del self.channelData[chan]["Userlist"][i]
                break
    else:
        self.__CMDHandler_log__.debug("Channel %s not found", params)
    
    if self.Bot_Auth.doesExist(name) and self.Bot_Auth.isRegistered(name) and not self.userInSight(name):
        #print "OK, WE LOST SIGHT OF HIM"
        self.Bot_Auth.unregisterUser(name)