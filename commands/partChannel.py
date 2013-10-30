ID = "part"
permission = 3

def execute(self, name, params, channel, userdata, rank):
    channels = []
    if len(params) == 0:
        channels.append(channel)
    else:
        for chan in params:
            chan = self.retrieveTrueCase(chan)
            if chan[0] != "#":
                channels.append("#"+chan)
            else:
                channels.append(chan)
                
    partParams = ",".join(channels)
    print partParams
    print channels
    self.send("PART :"+partParams+"", 4)
    for chan in channels:
        del self.channelData[chan]
    
    