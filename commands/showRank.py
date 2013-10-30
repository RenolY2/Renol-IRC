ID = "rank"
permission = 1

def execute(self, name, params, channel, userdata, rank):
    print rank
    self.sendChatMessage(self.send, channel, "You "+{"@" : "are OP", "+" : "are voiced", "" : "do not have a special rank", "@@" : "are Bot OP"}[rank])
    #self.sendChatMessage(self.send, channel, "You "+{"@" : "are OP", "+" : "are voiced", "" : "do not have a special rank", "@@" : "are Bot OP"}[self.userGetRank(channel, name)])