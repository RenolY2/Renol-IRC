ID = "join"
permission = 3

def execute(self, name, params, channel, userdata, rank):
    
    channels = params
    finchan = []
    
    for chan in channels:
        if chan[0] != "#":
            finchan.append("#"+chan)
        else:
            finchan.append(chan)
    
    self.joinChannel(self.send, finchan)