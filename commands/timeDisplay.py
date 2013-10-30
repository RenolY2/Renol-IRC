import time

ID = "time"
permission = 2
privmsgEnabled = True


def execute(self, name, params, channel, userdata, rank, chan):
    if len(params) > 0 and params[0] == "unix":
        self.sendChatMessage(self.send, channel, "{0}".format(time.time()))
    else:
        self.sendChatMessage(self.send, channel, time.asctime())