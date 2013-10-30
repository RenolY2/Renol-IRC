ID = "addop"
permission = 3

def notInList(user, userlist):
    for name in userlist:
        if name.lower() == user.lower():
            return False
    
    return True

def execute(self, name, params, channel, userdata, rank):
    names = params
    
    for name in names:
        if notInList(name, self.bot_userlist):
            self.bot_userlist.append(name)
            self.Bot_Auth.addUser(name)
            self.whoisUser(name)
    
    self.sendChatMessage(self.send, channel, "Added "+", ".join(names))