import time
import datetime
from calendar import timegm

ID = "utc"
permission = 0
privmsgEnabled = True


def execute(self, name, params, channel, userdata, rank, chan):
    UTCtime = time.time()
    
    
    if len(params) > 0:
        tzParameter = params[0]
        sign = tzParameter[0]
        
        if sign == "+":
            sign = 1
        elif sign == "-":
            sign = -1
        else:
            self.sendChatMessage(self.send, channel, "Incorrect format. Check help about the command.")
            return
        
        timeoffset = tzParameter[1:]
        
        if ":" in timeoffset:
            hour, minute = timeoffset.split(":", 1)
            
            if not hour.isdigit() or not minute.isdigit():
                self.sendChatMessage(self.send, channel, "Incorrect time offset. Needs to be a number.")
                return
            
            tzOffsetHour = sign*int(hour)
            tzOffsetMinute = sign*int(minute)
            
        else:
            if not timeoffset.isdigit():
                self.sendChatMessage(self.send, channel, "Incorrect time offset. Needs to be a number.")
                return
            
            tzOffsetHour = sign*int(timeoffset)
            tzOffsetMinute = 0
        
        
    else:
        tzOffsetHour = 0
        tzOffsetMinute = 0
    
    offsetTime = UTCtime + 3600*tzOffsetHour + 60*tzOffsetMinute
    offsetUTCtime = time.gmtime(offsetTime)
    
    
    
    self.sendChatMessage(self.send, channel, time.asctime(offsetUTCtime))

def __initialize__(self, Startup):
    entry = self.helper.newHelp(ID)
    
    entry.addDescription("The 'utc' command shows the current time in UTC. Optionally, you can set a offset according to which the time will be modified. ")
    entry.addDescription("This allows you to check the time in different time zones, if you know the offset value for that time zone.")
    entry.addArgument("UTC offset", "The offset value for the UTC time. Format needs to be +<hour> or -<hour>, "
                        "where you replace <hour> with a hour value. You can also specify the minutes, "
                        "in which case the format is +<hour>:<minute> or -<hour>:<minute>.", optional = True)
    entry.rank = 0
    
    self.helper.registerHelp(entry, overwrite = True)