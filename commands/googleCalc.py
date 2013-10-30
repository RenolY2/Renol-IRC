import simplejson
import urllib
import re

ID = "calc"
permission = 0

def convertSpecialSymbols(string):
    #print ord(string[6])
    toreplace = {"\\x26#215;" : "x", "\\x3" : "", "csup" : "^", "c/supe" : "", chr(0xA0) : "", "\\x26#8260" : ""}
    
    newstr = string
    for rep in toreplace:
        
        newstr = newstr.replace(rep, toreplace[rep])
        #print newstr
    newstr = newstr.replace("^e", "e^")
    #print newstr
    return newstr

def execute(self, name, params, channel, userdata, rank):
    calc = " ".join(params)
    file = urllib.urlopen("http://www.google.com/ig/calculator?q="+urllib.quote_plus(calc));
    #print calc
    result = file.read()
    #print result
    derp = result.replace('"', '')
    #derp.rep
    #print result
    #self.sendChatMessage(self.send, channel,result)
    #Functions().SendMsg(Socket, ConnectInfo.CHAN ,name, result)
    result = re.sub("([,{])(.*?):", '\g<1>"\g<2>":',result)
    #result = result.replace("([,{])(.*?):",  "\g<1>\g<2>:"   )
    #print result
    res2 = convertSpecialSymbols(result)
    #print res2
    result = res2
    #print "\x03"
    
    try:
        result = simplejson.loads(result, strict = False )
    #print result
        self.sendChatMessage(self.send, channel,result['lhs'] + " = "+ result['rhs'])
        if result['error'] != "":
            self.sendChatMessage(self.send, channel,"Error: "+ result['error'])
    
    except Exception as error: 
        self.sendChatMessage(self.send, channel, "An error appeared: "+str(error))
        #Functions().SendMsg(Socket, ConnectInfo.CHAN ,name,"Some error appeared, but no idea which one it is")
        #print traceback.print_tb(sys.last_traceback)
        #print traceback.print_stack()
        #Functions().SendMsg(Socket, ConnectInfo.CHAN ,name, traceback.print_tb(sys.last_traceback))
    #print result
    file.close()