import imp

ID = "reload"
permission = 3


def execute(self, name, params, channel, userdata, rank):
    if len(params) > 0 and params[0] in self.commands:
        cmd = params[0]
        path = self.commands[cmd][1]
        print path
        
        self.sendChatMessage(self.send, channel, "Reloading "+path)
        self.commands[cmd] = (imp.load_source(cmd, path), path)
        self.sendChatMessage(self.send, channel, "Done!")
    
    elif len(params) > 0 and params[0] not in self.commands:
        self.sendChatMessage(self.send, channel, "Command does not exist")
    else:
        self.sendChatMessage(self.send, channel, "Reloading..")
        self.commands = self.__LoadModules__("commands")
        self.sendChatMessage(self.send, channel, "Done!")