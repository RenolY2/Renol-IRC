import simplejson
import urllib
import re

ID = "old_calc"
permission = 3


## Google took down the iGoogle services. Thanks to that, the calculator api, which was
## apparently a part of the iGoogle services, is no longer functional.
## The calculator api was hosted at http://www.google.com/ig/calculator?q=

## Until a replacement is found, the google calc command will be out of commission.

def convertSpecialSymbols(string):
    toreplace = {"\\x26#215;" : "x", "\\x3" : "", "csup" : "^", "c/supe" : "", chr(0xA0) : "", "\\x26#8260" : ""}
    newstr = string
    
    for rep in toreplace:
        newstr = newstr.replace(rep, toreplace[rep])
        
    newstr = newstr.replace("^e", "e^")
    return newstr

def execute(self, name, params, channel, userdata, rank):
    self.sendNotice(name,"Command is out of commission due to the iGoogle service being no more existent.")
    
    
    
#    calc = " ".join(params)
#    file = urllib.urlopen("http://www.google.com/ig/calculator?q="+urllib.quote_plus(calc));
#    #print calc
#    result = file.read()
#    print result
#    derp = result.replace('"', '')
#    #derp.rep
#    #print result
#    #self.sendChatMessage(self.send, channel,result)
#    result = re.sub("([,{])(.*?):", '\g<1>"\g<2>":',result)
#    #result = result.replace("([,{])(.*?):",  "\g<1>\g<2>:"   )
#    #print result
#    res2 = convertSpecialSymbols(result)
#    #print res2
#    result = res2
#    
#    try:
#        result = simplejson.loads(result, strict = False )
#        self.sendChatMessage(self.send, channel,result['lhs'] + " = "+ result['rhs'])
#        
#        if result['error'] != "":
#            self.sendChatMessage(self.send, channel,"Error: "+ result['error'])
#    
#    except Exception as error: 
#        self.sendChatMessage(self.send, channel, "An error appeared: "+str(error))
#        
#    file.close()