

ID = "PRIVMSG"

def execute(self, sendMsg, msgprefix, command, params):
    #print params, prefix
    
    part1 = msgprefix.partition("!")
    part2 = part1[2].partition("@")
    
    name = part1[0]
    indent = part2[0]
    host = part2[2]
    
    cmdprefix = self.cmdprefix
    splitted = params.split(" ", 1)
    
    channel = splitted[0]
    chatMessage = splitted[1][1:]
    if channel[0] not in "#&":
        channel = name
        chan = False
        perms = ""
        print "HELP I'M GETTING PRIVMSGD BY ",name," : ",chatMessage
    else: 
        chan = True
        channel = self.retrieveTrueCase(channel)
        perms = self.userGetRank(channel, name)
        
    #print splitted, channel()
    
    
    #print msgprefix, params
    
    print "<"+name+"> "+chatMessage
    
    chatParams = chatMessage.rstrip().split(" ")
    
    for i in range(chatParams.count("")):
        chatParams.remove("")
    
    try:
        chatCmd = chatParams[0][1:].lower()
        usedPrfx = chatMessage[0]
    except IndexError:
        chatCmd = ""
        usedPrfx = ""
    #print "ok"
    
    
    
    if name in self.bot_userlist and self.Bot_Auth.isRegistered(name): #and (perms == "@" or perms == "+"):
        #print name + " is in Botlist"
        rank = 3
        perms = "@@"
    elif perms == "@":
        #print name + " is OP"
        rank = 2
    elif perms == "+":
        #print name + " is Voiced"
        rank = 1
    else:
        #print name + " is Nothing"
        rank = 0
        
    #rank = {"@" : 2, "+" : 1, "" : 0}[self.userGetRank(channel, name)]
    #print self.commands
    #print chatCmd
    if usedPrfx == cmdprefix and chatCmd in self.commands:
        try:
            support = self.commands[chatCmd][0].privmsgEnabled
        except AttributeError:
            support = False
            
        try:
            if rank >= self.commands[chatCmd][0].permission:
                if support == True:
                    self.commands[chatCmd][0].execute(self, name, chatParams[1:], channel, (indent, host), perms, chan)
                elif support == False and chan == True:
                    self.commands[chatCmd][0].execute(self, name, chatParams[1:], channel, (indent, host), perms)
        except KeyError as error:
            print "KeyError for command: "+str(error)
        except AttributeError as error:
            print "AttributeError for command: "+str(error)
    else:
        # if the message comes from a user, set channel to False
        # otherwise, set channel to the channel from which the message was received
        channel = chan == True and channel or False
        self.events["chat"].tryAllEvents(self, {"name" : name, "ident" : indent, "host" : host}, chatMessage, channel)
    
    #if "heyman" in chatMessage.lower():
    #    sendMsg("PRIVMSG "+channel+" :"+"Hey! :D",5)
    #elif "hallo" in chatMessage.lower():
    #    sendMsg("PRIVMSG "+channel+" :"+"Hi! :D",5)
    #            
    #if usedPrfx == cmdprefix:
    #
    #    if name == "Yoshi2" and chatCmd == "hardreload" :
    #        sendMsg("PRIVMSG "+channel+" :"+"Reloading...",2)
    #        self.Plugin = self.__LoadModules__("IRCpackets")
    #        sendMsg("PRIVMSG "+channel+" :"+"Reloaded! ;)",2)
    #    elif chatCmd == "say":
    #        sendMsg("PRIVMSG "+channel+" :"+" ".join(chatParams[1:]),3)
    #    elif (name == "SinZ" or name == "Yoshi2") and chatCmd == "raw":
    #        sendMsg(" ".join(chatParams[1:]), 4)
    #    elif chatCmd == "userlist":
    #        self.sendChatMessage(sendMsg, channel, "0123")
    #        print self.channelData
    #        self.sendChatMessage(sendMsg, channel, str(self.channelData[channel]["Userlist"]))
    #    elif chatCmd == "rank":
    #        self.sendChatMessage(sendMsg, channel, "You "+{"@" : "are OP", "+" : "are voiced", "" : "do not have a special rank"}[self.userGetRank(channel, name)])
            
            