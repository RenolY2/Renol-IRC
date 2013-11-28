ID = "convert"
permission = 0

import simplejson
import urllib2
import urllib
from os import makedirs

def UpdateRates(appid, path):
    try:
        url = "http://openexchangerates.org/api/latest.json?app_id={0}".format(appid)
        
        exrate = urllib2.urlopen(url, timeout = 15)
        result = exrate.read()
        exrate.close()
        
        data = open(path, "w")
        data.write(result)
        data.close()
        
        return simplejson.loads(result)["rates"]
    except IOError as error:
        dir = "/".join(path.split("/")[:-1])
        makedirs(dir)
        
        data = open(path, "w")
        data.write(result)
        data.close()
        
        return simplejson.loads(result)["rates"]
    except Exception as error:
        print str(error)
        return None

def read_CurrencyRate(path):
    file = open(path, "r")
    data = simplejson.loads(file.read())
    file.close()
    return data["rates"]



def findGroup(item):
    for group in conversion:
        if item in conversion[group]:
            return True, group
    return False, None

def matchGroup(item1, item2):
    for group in conversion:
        if item1 in conversion[group] and item2 in conversion[group]:
            return True, group
    
    return False, None

def __initialize__(self, Startup):
    if Startup == True:
        self.unit_conversion = conversion

words = ["to", "in"]
currency_path = "commands/Currency/currency_data.txt"
conversion = {  "distance":{"m" : 1, "ft" : 0.3048, "km" : 1000, "mi" : 1609.344, "in" : 0.0254,
                            "cm" : 1/100, "mm" : 1/1000, "nm" : 1/(10**(-9)), "yard" :  0.9144},
                "area":{},
                "volume":{},
                "mass" : {  "kg" : 1, "lb" : 0.45359237, "oz" : 0.028, "st" : 6.35029318, "t" : 1000, "shtn" : 907.18474,
                             "longtn": 1016.0469088 },
                "currency":{},
                "time":{"sec" : 1, "min" : 60, "h" : 60*60, "day" :24*60*60, "year": 24*60*60*365},
                "speed":{},
                "pressure":{},
                "compstorage" : {   "b" : 1, "B" : 8, "Kbit" : 10**3, "Mbit" : 10**6, "Gbit" : 10**9, "Tbit" : 10**12, "Pbit" : 10**15,
                                    "KB" : 8*(10**3), "MB" : 8*(10**6), "GB" : 8*(10**9), "TB" : 8*(10**12), "PB": 8*(10**15),
                                    "KiB" : 8*(2**10),"MiB" : 8*(2**20), "GiB" : 8*(2**30), "TiB" : 8*(2**40), "PiB" : 8*(2**50)}
                                }

# The currency conversion retrieves data from https://openexchangerates.org/
# An App ID is required for using the API from the website.
# Register an account on the website to receive your own App ID, or ask me for one.
# A free account can access the API 1000 times per month
appid = "PutYourAppidHere"


# We check if the local file with the currency exchange rates exists locally.
# If not, we try to download it or use fall-back data
# the fall back data is slightly less accurate and needs to be kept up to date manually.
try:
    conversion["currency"] = read_CurrencyRate(currency_path)
except Exception as error:
    print "ERROR: "+str(error) 
    
    result = UpdateRates(appid, currency_path)
    
    # Downloading the rates can fail due to various reasons: invalid appid or the website is down
    # If downloading fails, let's use some placeholder data
    if result == None:
        # Euro, US Dollar, British Pound, Japanese Yen, Australian Dollar, Canadian Dollar
        conversion["currency"] = {"EUR" : 0.7352, "USD" : 1, "GBP" : 0.6116, "JPY" : 102.135, "AUD" : 1.0995, "CAD" : 1.0585}
    else:
        conversion["currency"] = result

def execute(self, name, params, channel, userdata, rank):
    if len(params) == 1 and params[0].lower() == "update" and rank == "@@":
        data = UpdateRates(appid, currency_path)
        if data == None:
            self.sendChatMessage(self.send, channel, "Failed to update the currency exchange rates.")
        else:
            self.unit_conversion = data
            self.sendChatMessage(self.send, channel, "Updated currency exchange rates.")
            
    elif len(params) == 4 and params[2].lower() in words or len(params) == 3 and params[2].lower() not in words:
        num = params[0]
        
        unit1 = params[1]
        unit2 = len(params) == 4 and params[3] or params[2]
        
        doesMatch, group = matchGroup(unit1, unit2)
        
        if not doesMatch:
            self.sendChatMessage(self.send, channel, "Incompatible or unknown units")
        elif doesMatch:
            if "." in num:
                try:
                    num = float(num)
                except:
                    self.sendChatMessage(self.send, channel, "Invalid number")
                    return
            else:
                if not num.isdigit():
                    self.sendChatMessage(self.send, channel, "Invalid number")
                    return
                else:
                    num = int(num)
                    
            
            base = conversion[group][unit1] * num
            fin = (1.0/conversion[group][unit2])*base
            
            self.sendChatMessage(self.send, channel, "{0} {1} = {3} {2}".format(num, unit1, unit2, fin))
            
    elif len(params) > 3 and params[2].lower() not in words or len(params) > 4:
        self.sendChatMessage(self.send, channel, "Too many arguments")
        
    else:
        self.sendChatMessage(self.send, channel, "Not enough arguments")
        
        
    

