ID = "JOIN"

def execute(self, sendMsg, prefix, command, params):
    print "SOMEBODY JOINED CHANNEL:"
    print prefix
    print params
    
    part1 = prefix.partition("!")
    part2 = part1[2].partition("@")
    
    name = part1[0]
    indent = part2[0]
    host = part2[2]
    
    channel = self.retrieveTrueCase(params)
    
    if self.Bot_Auth.doesExist(name) and not self.Bot_Auth.isRegistered(name):
            self.whoisUser(name)
            
    if channel != False:
    
    #if (name, "") not in self.channelData[channel]["Userlist"]:
        
        
        
        nothere = True
        for derp in self.channelData[channel]["Userlist"]:
            if derp[0] == name:
                nothere = False
                break
        
        if nothere == True:
            self.channelData[channel]["Userlist"].append((name, ""))