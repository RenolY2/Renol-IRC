
import urllib2
from urllib import quote

from commands.miscLib.xml_to_dict import xml_to_dict

appid = ""

ID = "wolfram"
permission = 3

class WolframAlpha():
    def __init__(self, appid):
        self.appid = appid
        self.url = "http://api.wolframalpha.com/v1/query.jsp"+"?appid="+quote(appid)
        
    def submit(self, inputstring):
        inputstring = quote(inputstring)
        urlstring = self.url+"&input="+inputstring
        
        data = urllib2.urlopen(urlstring, timeout = 8)
        result = data.read()
        
        return result
        
def __initialize__(self, Startup):
    self.WolframAlpha = WolframAlpha(appid)

def execute(self, name, params, channel, userdata, rank):
    request = " ".join(params)
    request = request.strip()
    
    if len(request) > 1:
        try:
            result = self.WolframAlpha.submit(request)
            xmldict = xml_to_dict(result)
            pod = xmldict["queryresult"]["pod"]
            
            for item in pod:
                description = item["@title"]
                result = item["subpod"]["plaintext"]
                
                if result != None:
                    result = result.strip("| ")
                    result = result.replace(" | ", ": ")
                    result = " | ".join(result.split("\n"))
                   
                    
                    self.sendMessage(channel, "{0}: {1}".format(description, result))
            
        except Exception as error:
            self.sendMessage(channel, "Error appeared: {0}".format(str(error)))