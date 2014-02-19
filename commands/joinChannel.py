ID = "join"
permission = 3
privmsgEnabled = True

def execute(self, name, params, channel, userdata, rank, chan):
    
    channels = params
    finchan = []
    
    for chan in channels:
        if chan[0] != "#":
            finchan.append("#"+chan)
        else:
            finchan.append(chan)
    
    if len(finchan) > 0:
        self.joinChannel(self.send, finchan)
    else:
        self.sendNotice(name, "Please specify a channel")