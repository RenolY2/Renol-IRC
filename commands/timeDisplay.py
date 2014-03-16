import time

ID = "time"
permission = 2
privmsgEnabled = True


def execute(self, name, params, channel, userdata, rank, chan):
    self.sendChatMessage(self.send, channel, time.asctime())