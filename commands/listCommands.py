ID = "commands"
permission = 2

def execute(self, name, params, channel, userdata, rank):
    commands = ""
    for cmd in self.commands:
        commands += cmd + " | "
        
    self.sendChatMessage(self.send, channel, "Available commands:")   
    self.sendChatMessage(self.send, channel, commands)
    