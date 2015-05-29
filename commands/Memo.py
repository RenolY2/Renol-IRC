import time
import logging

from BotEvents import ChannelAlreadyExists
from commands.MemoDB.memo_db import MemoDB

ID = "memo"
permission = 0

channel = "#test"

def join_event(self, channels, name, ident, host, channel):
    if channel in channels:
        msgcount = self.ModDota_MemoDB.getMsgCount_toUser(name, channel)[0]
        
        if msgcount == 1: 
            suffix = ""
            referingTo = "it"
        else: 
            suffix = "s"
            referingTo = "them"

        if msgcount > 0:
            bannedInfo = self.Banlist.checkBan(name, ident, host, groupName="Memo")
            if bannedInfo[0] == True:
                return

        if msgcount > 0 and msgcount < 5:
            self.sendMessage(channel, (
                                       "{2}: You have {0} unread message{1}. "
                                        "Say anything to read {3}.".format(msgcount,
                                                                            suffix, name, 
                                                                            referingTo)
                                        ))
        elif msgcount >= 5 and msgcount < 10:
            self.sendMessage(channel, (
                                       "{3}: You have {0} unread message{1}. "
                                       "Say anything to read them. "
                                       "Use '{2}memo #pm' to read them privately.".format(msgcount, suffix,
                                                                                        self.cmdprefix, name)
                                        ))
            
        elif msgcount >= 10:
            self.sendMessage(channel, (
                                       "{3}: You have {0} unread message{1}. "
                                       "Say anything to read them. "
                                       "Use '{2}memo #pm' to read them privately, "
                                       "or {2}memo #clear' to delete them.".format(msgcount, suffix,
                                                                                   self.cmdprefix, name)
                                        ))

def message_event(self, channels, userdata, message, channel):
    if channel in channels:
        name, ident, host = userdata["name"], userdata["ident"], userdata["host"]
        
        msgcount = self.ModDota_MemoDB.getMsgCount_toUser(name, channel)[0]

        if msgcount > 0:
            bannedInfo = self.Banlist.checkBan(name, ident, host, groupName="Memo")
            if bannedInfo[0] == True:
                return

        if msgcount > 0:
            message = self.ModDota_MemoDB.getOneMessage_toUser(name, channel)
            
            memoID, date, author, target, text = message
            
            self.sendMessage(channel, u"{3}: <{0}> {1}  [sent at {2}]".format(author, text, 
                                                                              date, userdata["name"]))
            
            self.ModDota_MemoDB.removeMessage(memoID)
            

def user_changes_nickname(self, channels, name, newName, ident, host, affectedChannels):
    for channel in channels:
        if channel in affectedChannels:
            msgcount = self.ModDota_MemoDB.getMsgCount_toUser(newName, channel)[0]


            if msgcount > 0:
                bannedInfo = self.Banlist.checkBan(name, ident, host, groupName="Memo")
                if bannedInfo[0] == True:
                    return

            if msgcount == 1: 
                suffix = ""
                referingTo = "it"
            else: 
                suffix = "s"
                referingTo = "them"
                    
            if msgcount > 0 and msgcount < 5:
                self.sendMessage(channel, (
                                           "{2}: You have {0} unread message{1}. "
                                            "Say anything to read {3}.".format(msgcount,
                                                                                suffix, newName, 
                                                                                referingTo)
                                            ))
            elif msgcount >= 5 and msgcount < 10:
                self.sendMessage(channel, (
                                           "{3}: You have {0} unread message{1}. "
                                           "Say anything to read them. "
                                           "Use '{2}memo #pm' to read them privately.".format(msgcount, suffix,
                                                                                            self.cmdprefix, newName)
                                            ))
                
            elif msgcount >= 10:
                self.sendMessage(channel, (
                                           "{3}: You have {0} unread message{1}. "
                                           "Say anything to read them. "
                                           "Use '{2}memo #pm' to read them privately, "
                                           "or {2}memo #clear' to delete them.".format(msgcount, suffix,
                                                                                       self.cmdprefix, newName)
                                            ))
    #print name, newName, ident, host
    #print "OH HE CHANGES NAMES FROM {0} TO {1}".format(name, newName)

def execute(self, name, params, channel, userdata, rank):
    if len(params) >= 1 and params[0].startswith("#"):
        # The first parameter starts with '#', this means it is a command.
        command = params[0][1:]
        rank = self.rankconvert[rank]
        
        if command in memo_commands:
            if rank >= memo_commands[command].rank:
                memoparams = params[1:]
                if len(memoparams) >= memo_commands[command].params:
                    memo_commands[command].run(self, name, memoparams, channel, userdata)
                else:
                    self.sendNotice(name, 
                                    ("Not enough parameters, needs {0} "
                                     "parameters".format(memo_commands[command].params))
                                    )
            else:
                pass # Rank too low, do nothing
        else:
            pass # No such command, do nothing
        
    elif len(params) >= 2:
        # Proceed as normal: First parameter is the name of the user to whom the memo goes.
        # Everything past the first parameter is the message.
        target = params[0]
        message = " ".join(params[1:])
        
        if not self.events["channeljoin"].doesExist("ModDotaMemo_channeljoin"):
            self.sendNotice(name, "Memo service isn't running.")
            return
        
        channels = self.events["channeljoin"].getChannels("ModDotaMemo_channeljoin")
        if channel not in channels:
            self.sendNotice(name, "Memo service isn't running in this channel.")
            return
        
        
        
        
        self.ModDota_MemoDB.addMessage(name, target, channel, message)
        memoID = self.ModDota_MemoDB.getLatestMessage()[0]
        
        self.sendMessage(channel, "Memo Nr. {0} created.".format(memoID))

def __initialize__(self, startup):
    if startup:
        self.ModDota_MemoDB = MemoDB("commands/MemoDB/memo.db")
        self.ModDota_MemoDB_UnreadMessages = {}

    self.Banlist.defineGroup("Memo")


##
##
## __________________________________
## Commands For Memo are defined here
## vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
##
##

class command_turnOn():
    def __init__(self):
        self.params = 0
        self.rank = 2
        
    def run(self, irc, name, memoparams, channel, userdata):
        if not irc.events["channeljoin"].doesExist("ModDotaMemo_channeljoin"):
            if len(memoparams) == 0:
                add_events(irc, [])
                
                irc.sendNotice(name, "Memo event enabled. Add a channel in which memo should run.")
            else:
                memo_channel = memoparams[0]
                
                if memo_channel not in irc.channelData:
                    irc.sendNotice(name, "I'm not in such a channel. Check {0}channels".format(irc.cmdprefix))
                else:
                    add_events(irc, [memo_channel])
                    
                    irc.sendNotice(name, "Memo event enabled. Running in {0}".format(memo_channel))
                    
        else:
            irc.sendNotice(name, "Memo event is already running")

class command_turnOff():
    def __init__(self):
        self.params = 0
        self.rank = 2
        
    def run(self, irc, name, memoparams, channel, userdata):
        if irc.events["channeljoin"].doesExist("ModDotaMemo_channeljoin"):
            remove_events(irc)
            
            irc.sendNotice(name, "Memo event disabled")
        else:
            irc.sendNotice(name, "Memo event is already disabled")

class command_status():
    def __init__(self):
        self.params = 0
        self.rank = 2
    def run(self, irc, name, memoparams, channel, userdata):
        if irc.events["channeljoin"].doesExist("ModDotaMemo_channeljoin"):
            channels = irc.events["channeljoin"].getChannels("ModDotaMemo_channeljoin")
            irc.sendNotice(name, "ModDotaMemo is running in the channels {0}".format(channels))
        else:
            irc.sendNotice(name, "ModDotaMemo is not running.")

class command_add():
    def __init__(self):
        self.params = 1
        self.rank = 2
    def run(self, irc, name, memoparams, channel, userdata):
        memo_channel = memoparams[0]
        
        if memo_channel not in irc.channelData:
            irc.sendNotice(name, "I'm not in that channel! Check {0}channels".format(irc.cmdprefix))
            return
        
        if not irc.events["channeljoin"].doesExist("ModDotaMemo_channeljoin"):
            irc.sendNotice(name, "Memo event isn't running.")
            return
        
        try:
            add_channel(irc, memo_channel)
            
            irc.sendNotice(name, "Channel '{0}' added.".format(memo_channel))
        except ChannelAlreadyExists:
            irc.sendNotice(name, "Channel {0} already exists. Channel not added.".format(memo_channel))

class command_remove():
    def __init__(self):
        self.params = 1
        self.rank = 2
        
    def run(self, irc, name, memoparams, channel, userdata):
        rem_channel = memoparams[0]
        
        if not irc.events["channeljoin"].doesExist("ModDotaMemo_channeljoin"):
            irc.sendNotice(name, "Memo event isn't running.")
            return
        
        currentChannels = irc.events["channeljoin"].getChannels("ModDotaMemo_channeljoin")
        
        if rem_channel not in currentChannels:
            irc.sendNotice(name, "No such channel, check {0}memo #status.".format(irc.cmdprefix))
            return
        
        remove_channel(irc, rem_channel)
        
        irc.sendNotice(name, "Channel '{0}' added.".format(rem_channel))

class command_PM_memos():
    def __init__(self):
        self.params = 0
        self.rank = 0
        
    def run(self, irc, name, memoparams, channel, userdata):
        if not irc.events["channeljoin"].doesExist("ModDotaMemo_channeljoin"):
            irc.sendNotice(name, "Memo event isn't running.")
            return
        
        currentChannels = irc.events["channeljoin"].getChannels("ModDotaMemo_channeljoin")
        
        if channel not in currentChannels:
            irc.sendNotice(name, "Memo event isn't running in this channel.")
            return
        
        messages = irc.ModDota_MemoDB.getAllMessages_toUser(name, channel)
        
        if len(messages) == 0:
            irc.sendNotice(name, "You have no messages.")
            return
        else:
            suffix = (len(messages) != 1 and "s") or ""
            irc.sendNotice(name, "You have {0} message{1}.".format(len(messages), suffix))
            
        for memo in messages:
            memoID, date, author, target, text = memo
            irc.sendNotice(name, u"{3}: <{0}> {1}  [sent at {2}]".format(author, text, date, name))
            
        irc.ModDota_MemoDB.removeAllMessages_toUser(name, channel)

class command_clear_memos():
    def __init__(self):
        self.params = 0
        self.rank = 0
        
    def run(self, irc, name, memoparams, channel, userdata):
        if not irc.events["channeljoin"].doesExist("ModDotaMemo_channeljoin"):
            irc.sendNotice(name, "Memo event isn't running.")
            return
        
        currentChannels = irc.events["channeljoin"].getChannels("ModDotaMemo_channeljoin")
        
        if channel not in currentChannels:
            irc.sendNotice(name, "Memo event isn't running in this channel.")
            return
        
        msgcount =  irc.ModDota_MemoDB.getMsgCount_toUser(name, channel)[0]
        
        if msgcount == 0:
            irc.sendNotice(name, "You have no messages.")
        else:
            suffix = (msgcount == 1 and "") or "s"
            irc.sendNotice(name, "You have {0} message{1}.".format(msgcount, suffix))
            irc.ModDota_MemoDB.removeAllMessages_toUser(name, channel)
            irc.sendNotice(name, "All messages deleted.")

class command_inbox():
    def __init__(self):
        self.params = 0
        self.rank = 0
        
    def run(self, irc, name, memoparams, channel, userdata):
        if not irc.events["channeljoin"].doesExist("ModDotaMemo_channeljoin"):
            irc.sendNotice(name, "Memo event isn't running.")
            return
        
        currentChannels = irc.events["channeljoin"].getChannels("ModDotaMemo_channeljoin")
        
        if channel not in currentChannels:
            irc.sendNotice(name, "Memo event isn't running in this channel.")
            return
        
        msgcount =  irc.ModDota_MemoDB.getMsgCount_toUser(name, channel)[0]
        
        if msgcount == 0:
            irc.sendNotice(name, "You have no messages.")
        else:
            suffix = (msgcount != 1 and "s") or ""
            irc.sendNotice(name, "You have {0} message{1}.".format(msgcount, suffix))
            
            msgcount_fromAuthors = []
            
            cursor = irc.ModDota_MemoDB.cursor
            
            cursor.execute( """
                            SELECT DISTINCT author FROM Memo
                            WHERE target = ? AND channel = ?
                            ORDER BY author
                            """, (name.lower(), channel))
            
            authors = cursor.fetchall()
            print authors
            print channel, type(channel)
            for author in authors:
                author = author[0]
                cursor.execute( """
                                SELECT Count(*) FROM Memo
                                WHERE target = ? AND channel = ? AND author = ?
                                """, (name.lower(), channel, author))
                msgcount = cursor.fetchone()[0]
                
                msgcount_fromAuthors.append("{0} ({1})".format(author, msgcount))
            
            msgcount_fromAuthors_string = ", ".join(msgcount_fromAuthors)
            irc.sendNotice(name, ("You have received messages "
                                  "from the following people: {0}".format(msgcount_fromAuthors_string)))
                
class command_help():
    def __init__(self):
        self.params = 0
        self.rank = 0
        
    def run(self, irc, name, memoparams, channel, userdata):
        irc.sendNotice(name, "The memo plugin allows you to send messages to yourself or other people.")
        irc.sendNotice(name, ("Do note that the name of the recipient will not be verified, "
                              "anybody with the name you specified can receive the message. "
                              "Do not send confidential messages."))
        irc.sendNotice(name, "Usage: {0}memo <name> <message>".format(irc.cmdprefix))
        irc.sendNotice(name, ("Use '{0}memo #pm' to read all received messages privately. "
                              "Use '{0}memo #clear' to delete all received messages.".format(irc.cmdprefix)))
        irc.sendNotice(name, ("Use '{0}memo #inbox' to check how many messages "
                              "you have received and who has sent them.".format(irc.cmdprefix)))
    
    
##
##
## __________________________________
## Command List
## vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
##
##

memo_commands = {"enable" : command_turnOn(),
                 "disable" : command_turnOff(),
                 "status" : command_status(),
                 "add" : command_add(),
                 "remove" : command_remove(),
                 "pm" : command_PM_memos(),
                 "clear" : command_clear_memos(),
                 "help" : command_help(),
                 "inbox" : command_inbox()}

##
##
## __________________________________
## Misc/Helper Functions
## vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
##
##

def add_events(irc, channels):
    irc.events["channeljoin"].addEvent("ModDotaMemo_channeljoin", join_event, channels)
    irc.events["chat"].addEvent("ModDotaMemo_message", message_event, channels)
    
    #irc.events["channelpart"].addEvent("ModDotaMemo_userPart", user_leaves_event, channels)
    #irc.events["channelkick"].addEvent("ModDotaMemo_userKick", user_is_kicked_event, channels)
    #irc.events["userquit"].addEvent("ModDotaMemo_userQuit", user_quits, channels)
    irc.events["nickchange"].addEvent("ModDotaMemo_userNickchange", user_changes_nickname, channels)

def remove_events(irc):
    irc.events["channeljoin"].removeEvent("ModDotaMemo_channeljoin")
    irc.events["chat"].removeEvent("ModDotaMemo_message")
    
    #irc.events["channelpart"].removeEvent("ModDotaMemo_userPart")
    #irc.events["channelkick"].removeEvent("ModDotaMemo_userKick")
    #irc.events["userquit"].removeEvent("ModDotaMemo_userQuit")
    irc.events["nickchange"].removeEvent("ModDotaMemo_userNickchange")

def add_channel(irc, channel):
    irc.events["channeljoin"].addChannel("ModDotaMemo_channeljoin", channel)
    irc.events["chat"].addChannel("ModDotaMemo_message", channel)
    
    #irc.events["channelpart"].addChannel("ModDotaMemo_userPart", channel)
    #irc.events["channelkick"].addChannel("ModDotaMemo_userKick", channel)
    #irc.events["userquit"].addChannel("ModDotaMemo_userQuit", channel)
    irc.events["nickchange"].addChannel("ModDotaMemo_userNickchange", channel)

def remove_channel(irc, channel):
    irc.events["channeljoin"].removeChannel("ModDotaMemo_channeljoin", channel)
    irc.events["chat"].removeChannel("ModDotaMemo_message", channel)
    
    #irc.events["channelpart"].removeChannel("ModDotaMemo_userPart", channel)
    #irc.events["channelkick"].removeChannel("ModDotaMemo_userKick", channel)
    #irc.events["userquit"].removeChannel("ModDotaMemo_userQuit", channel)
    irc.events["nickchange"].removeChannel("ModDotaMemo_userNickchange", channel)

