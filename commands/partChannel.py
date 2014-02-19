ID = "part"
permission = 3
privmsgEnabled = True

def execute(self, name, params, channel, userdata, rank, isChannel):
    channels = []
    
    if len(params) == 0 and isChannel == True:
        channels.append(channel)
    elif len(params) == 0 and isChannel == False:
        self.sendNotice(name, "Please specify a channel")
        return
    else:
        for chanEntry in params:
            if chanEntry[0] != "#":
                chanEntry = "#"+chanEntry
                
            chan = self.retrieveTrueCase(chanEntry)
            if chan != False:
                channels.append(chan)
            else:
                print chanEntry, "wat"
                
    partParams = ",".join(channels)
    print partParams
    print channels
    
    if len(partParams) > 0:
        self.send("PART :"+partParams+"", 4)
        for chan in channels:
            del self.channelData[chan]
    
    