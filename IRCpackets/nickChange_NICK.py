ID = "NICK"

def execute(self, sendMsg, prefix, command, params):
    part1 = prefix.partition("!")
    part2 = part1[2].partition("@")
    
    name = part1[0]
    indent = part2[0]
    host = part2[2]
    
    newName = params[1:]
    print "NICKCHANGE"
    
    if self.Bot_Auth.doesExist(name): 
        self.Bot_Auth.unregisterUser(name)
        
    if self.Bot_Auth.doesExist(newName): 
        self.whoisUser(newName)
    
    for chan in self.channelData:
        for i in range(len(self.channelData[chan]["Userlist"])):
            user, pref = self.channelData[chan]["Userlist"][i]
            if user == name:
                self.channelData[chan]["Userlist"][i] = (newName, pref)
                break