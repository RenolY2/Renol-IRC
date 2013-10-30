import urllib2
import re
import datetime
import simplejson
import time as timederp



ID = "youtube"
permission = 3
privmsgEnabled = False

def execute(self, name, params, channel, userdata, rank):
    if len(params) == 1 and params[0] == "on":
        if not self.events["chat"].doesExist("ytChecker"):
            #print "Turning youtubeevent on."
            #self.sendChatMessage(self.send, channel, "Turning event on.")
            
            self.events["chat"].addEvent("ytChecker", ytLinkChecker, [channel])
            
            self.sendNotice(name, "Turning YtEvent on") 
        else:
            if channel in self.events["chat"].getChannels("ytChecker"):
                #print "youtubeChecker is already running in this channel"
                self.sendNotice(name, "YtEvent is already running")
                
            else:
                self.events["chat"].addChannel("ytChecker", channel)
                self.sendNotice(name, "Turning YtEvent on")
                #print "added "+channel
            #self.sendChatMessage(self.send, channel, "event is already running.")
            
    elif len(params) == 1 and params[0] == "off":
        if self.events["chat"].doesExist("ytChecker"):
            #print "turning off in "+str(channel)
            #self.sendChatMessage(self.send, channel, "Turning event off.") 
            self.events["chat"].removeChannel("ytChecker", channel)
            self.sendNotice(channel, "YtEvent is now off in this channel") 
            
            if self.events["chat"].getChannels("ytChecker") == []:
                self.events["chat"].removeEvent("ytChecker")
                
                print "killed YtEvent"
        else:
            #self.sendChatMessage(self.send, channel, "youtube event isn't running!") 
            self.sendNotice(name, "YtEvent is already off") 
            print "YtEvent is off"

def ytLinkChecker(self, channels, userdata, message, currChannel):     
    if currChannel in channels:
        #print "reddit event is working "+currChannel
        exists = "youtu.be/" in message or "youtube.com/" in message
        if exists:
            message = message.strip()
            
            ytUrl = findLink(message, "youtu.be/")
            if ytUrl != False:
                temp = urllib2.urlopen(ytUrl, timeout = 1)
                ytUrl = temp.geturl()
            else:
                ytUrl = findLink(message, "youtube.com/")
            
                
            print ytUrl
            if ytUrl != False:
                start = timederp.time()
                ythandler = urllib2.urlopen(ytUrl)
                html = ythandler.read()
                ythandler.close()
                ytmatch = re.search("<script>var ytplayer = ytplayer \|\| \{\};ytplayer.config = (\{.*?\});</script>", html)
                
                authormatch = re.search("""<span itemprop="author" itemscope itemtype="http://schema.org/Person">
          <link itemprop="url" href="http://www.youtube.com/user/(.*)">
        </span>""", html)
                
                viewcountmatch = re.search("""</span></span><div id="watch7-views-info">      <span class="watch-view-count " >
    ([0-9\.]+)
  </span>""", html)
                
                if ytmatch == None or viewcountmatch == None or authormatch == None:
                    #print "ERRORORORO~~~~~~"
                    print "Matches didn't match"
                    print ytUrl
                    return False
                
                viewcount = viewcountmatch.group(1)
                author = authormatch.group(1)
                json = simplejson.loads(ytmatch.group(1))
                
                title = json["args"]["title"]
                lengthSeconds = json["args"]["length_seconds"]
                
                min = int(lengthSeconds/60)
                sec = lengthSeconds%60
                time = "{0}:{1:02d}".format(min, sec)
                
                #date = datetime.date.fromtimestamp(json["args"]["timestamp"])
                #created = date.strftime("%d.%m.%Y")
                #print created
                formats = getFormats(json["args"]["fmt_list"])
                #print formats
                
                #print "yup, works"
                
                
                
                infostring = ("Author: {0}, Title: '{1}', length: {2}, "
                "viewcount: {3}, available resolutions: {4}".format(author, title, time, viewcount, ", ".join(formats)))
                
                self.sendChatMessage(self.send, currChannel, infostring)
                
                #print "Time taken: {0}".format(timederp.time()-start)
                
def getFormats(formatString):
    fmtList = []
    for format in formatString.split(","):
        info = format.split("/")
        res = info[1]
        if res not in fmtList:
            fmtList.append(res)
            
    return fmtList                
                
def findLink(message, keyword):
    split = message.split(" ")
    for derp in split:
        if keyword in derp:
            return derp
    return False