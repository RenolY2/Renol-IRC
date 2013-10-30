try:
    import praw
    import re
    import datetime
    import urllib2
    available = True
except:
    available = False

ID = "reddit"
permission = 3
privmsgEnabled = False

def execute(self, name, params, channel, userdata, rank):
    if available == False:
        print "reddit feature not available; requires PRAW"
        
    else:
        
        if len(params) == 1 and params[0] == "on":
            if not self.events["chat"].doesExist("redditChecker"):
                #print "Turning redditevent on."
                #self.sendChatMessage(self.send, channel, "Turning chatevent on.")
                
                self.events["chat"].addEvent("redditChecker", redditLinkChecker, [channel])
                self.redditInstance = praw.Reddit(user_agent="Renol-IRC's info retriever for reddit submissions for IRC")
                
                self.sendChatMessage(self.send, channel, "Turning RedditEvent on") 
            else:
                if channel in self.events["chat"].getChannels("redditChecker"):
                    #print "redditChecker is already running in this channel"
                    self.sendNotice(name, "RedditEvent is already running")
                    
                else:
                    self.events["chat"].addChannel("redditChecker", channel)
                    self.sendChatMessage(self.send, channel, "Turning RedditEvent on")
                    #print "added "+channel
                #self.sendChatMessage(self.send, channel, "chatevent is already running.")
                
        elif len(params) == 1 and params[0] == "off":
            if self.events["chat"].doesExist("redditChecker"):
                #print "turning off in "+str(channel)
                #self.sendChatMessage(self.send, channel, "Turning chatevent off.") 
                self.events["chat"].removeChannel("redditChecker", channel)
                self.sendChatMessage(self.send, channel, "RedditEvent is now off in this channel") 
                
                if self.events["chat"].getChannels("redditChecker") == []:
                    self.events["chat"].removeEvent("redditChecker")
                    del self.redditInstance
                    
                    print "killed redditEvent"
            else:
                #self.sendChatMessage(self.send, channel, "redditevent isn't running!") 
                self.sendNotice(name, "RedditEvent is already off") 
                print "redditEvent is off"

def redditLinkChecker(self, channels, userdata, message, currChannel):     
    if currChannel in channels:
        #print "reddit event is working "+currChannel
        exists = "redd.it/" in message or "reddit.com/" in message
        if exists:
            message = message.strip()
            
            redditUrl = findLink(message, "redd.it/")
            if redditUrl != False:
                temp = urllib2.urlopen(redditUrl, timeout = 1)
                redditUrl = temp.geturl()
            else:
                redditUrl = findLink(message, "reddit.com/")
            
                
            print redditUrl
            if redditUrl != False:
                try:
                    inst = self.redditInstance.get_submission(redditUrl)
                except Exception as error:
                    print "issue with retrieving link:"
                    print str(error)
                else:
                    if isinstance(inst, praw.objects.Submission):
                        #print inst
                        
                        date = datetime.datetime.fromtimestamp(inst.created_utc)
                        #date.microsecond = 0
                        date = date.isoformat(" ")+" (UTC)"
                        
                        points = inst.ups > inst.downs and inst.ups - inst.downs or 0
                        
                        finpoints = points == 1 and "1 point" or str(points) + " points"
                        finups = inst.ups == 1 and "1 upvote" or str(inst.ups)+" upvotes"
                        findowns = inst.downs == 1 and "1 downvote" or str(inst.downs) + " downvotes"
                        fincomms = inst.num_comments == 1 and "1 comment" or str(inst.num_comments)+" comments"
                        
                        info = ("author: {0}, {1} ({2}, {3})"
                        ", {4}, created on {5}".format(inst.author, finpoints, finups, findowns, fincomms, date))
                        #print info
                        self.sendChatMessage(self.send, currChannel, info)

def findLink(message, keyword):
    split = message.split(" ")
    for derp in split:
        if keyword in derp:
            return derp
    return False