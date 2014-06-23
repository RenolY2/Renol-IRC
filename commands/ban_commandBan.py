from BanList import InvalidCharacterUsed, NoSuchBanGroup

ID = "ban"
permission = 3

def execute(self, user, params, channel, userdata, rank):
    if len(params) == 0:
        self.sendNotice(user, "No user string specified.")
        return
    
    elif len(params) >= 1:
        userstring = params[0]
        countExclamationMark = userstring.count("!")
        countAt = userstring.count("@")
        
        # We need to confirm that the string is formatted correctly:
        # 1. Exactly one ! and one @
        # 2. ! comes before @
        if (
            (countExclamationMark != 1) 
            or (countAt != 1)
            or (userstring.find("!") > userstring.find("@"))
            ):
            self.sendNotice(user, "User string should be formatted like this: username!ident@host")
            return
        else:
            username, sep, identAndHost =  userstring.partition("!")
            ident, sep, host = identAndHost.partition("@")
            
            if username == "*" and ident == "*" and host == "*":
                self.sendNotice(user, "You can't ban everyone (including yourself)!")
                return
            
            try:
                if len(params) == 1:
                    result = self.Banlist.banUser(username, ident, host)
                    if result == True:
                        self.sendNotice(user, u"Userstring {0} banned.".format(userstring))
                    if result == False:
                        self.sendNotice(user, u"Userstring {0} is already banned.".format(userstring))
                else:
                    group = params[1]
                    result = self.Banlist.banUser(username, ident, host, group)
                    if result == True:
                        self.sendNotice(user, 
                                        u"Userstring {0} banned in group '{1}'.".format(userstring, group)
                                        )
                    if result == False:
                        self.sendNotice(user, 
                                        u"Userstring {0} is already banned in group {1}.".format(userstring, group)
                                        )
                        
            except NoSuchBanGroup as error:
                self.sendNotice(user, u"Ban group '{0}' does not exist.".format(error.group))
                return
            except InvalidCharacterUsed as error:
                self.sendNotice(user, 
                                u"Invalid character '{0}' found in position {1} of '{2}'.".format(error.char,
                                                                                                  error.pos,
                                                                                                  error.string))
                return