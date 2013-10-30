ID = "KICK"

def execute(self, sendMsg, prefix, command, params):
    print "SOMEBODY WAS KICKED:"
    print prefix
    print params
    
    fields = params.split(" ")
    
    channel = fields[0]
    name = fields[1]
    
    chan = self.retrieveTrueCase(channel)
    
    
            
    if chan != False:
        
        for i in range(len(self.channelData[chan]["Userlist"])):
            user, pref = self.channelData[chan]["Userlist"][i]
            if user == name:
                del self.channelData[chan]["Userlist"][i]
                break
    
    if self.Bot_Auth.doesExist(name) and self.Bot_Auth.isRegistered(name) and not self.userInSight(name):
        self.Bot_Auth.unregisterUser(name)