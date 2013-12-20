ID = "convert"
permission = 0

import simplejson
import urllib2
from os import makedirs
import os.path as os_path

words = ["to", "in"]
currency_path = "commands/Currency/currency_data.txt"
conversion = {  "distance":{"m" : 1.0, "ft" : 0.3048, "km" : 1000, "mi" : 1609.344, "in" : 0.0254,
                            "cm" : 1.0/100, "mm" : 1.0/1000, "nm" : 1.0/(10**(-9)), "yard" :  0.9144},
                "area":{},
                "volume":{},
                "mass" : {  "kg" : 1, "lb" : 0.45359237, "oz" : 0.028, "st" : 6.35029318, "t" : 1000, "shtn" : 907.18474,
                             "longtn": 1016.0469088 },
                "currency":{},
                "time":{"sec" : 1, "min" : 60, "h" : 60*60, "day" :24*60*60, "year": 24*60*60*365},
                "speed":{},
                "pressure":{},
                "compstorage" : {   "bit" : 1, "byte" : 8, "Kbit" : 10**3, "Mbit" : 10**6, "Gbit" : 10**9, "Tbit" : 10**12, "Pbit" : 10**15,
                                    "KB" : 8*(10**3), "MB" : 8*(10**6), "GB" : 8*(10**9), "TB" : 8*(10**12), "PB": 8*(10**15),
                                    "KiB" : 8*(2**10),"MiB" : 8*(2**20), "GiB" : 8*(2**30), "TiB" : 8*(2**40), "PiB" : 8*(2**50)}
              }

# We define a dictionary of aliases, i.e. alternative names for units of measure
# Ideas for how it can be improved are welcome!
alias = {"distance" : {"meter" : "m", "feet" : "ft", "mile" :"mi", "inch" : "in"},
         "area" : {},
         "volume" : {},
         "mass" : {"kilogram": "kg", "pound" : "lb", "tonne" : "t", "stone" : "st"},
         "currency" : {},
         "time" : {"second" : "sec", "minute" : "min", "hour" : "h"},
         "speed" : {},
         "pressure" : {},
         "compstorage" : {"bytes" : "byte", "bits" : "bit"}
         
         }




# The currency conversion retrieves data from https://openexchangerates.org/
# An App ID is required for using the API from the website.
# Register an account on the website to receive your own App ID, or ask me for one.
# A free account can access the API 1000 times per month
appid = ""

def UpdateRates(appid, path):
    try:
        dir = "/".join(path.split("/")[:-1])
        if not os_path.exists(dir):
            print dir
            makedirs(dir)
            
        url = "http://openexchangerates.org/api/latest.json?app_id={0}".format(appid)
        
        exrate = urllib2.urlopen(url, timeout = 15)
        result = exrate.read()
        exrate.close()
        
        data = open(path, "w")
        data.write(result)
        data.close()
        
        
        
        return invertRates(simplejson.loads(result)["rates"])
    except Exception as error:
        print str(error), "wat"
        return None

# We are inverting the data so it is in the
# the CURRENCY->USD format instead of the USD->CURRENCY format
def invertRates(rates):
    for item in rates:
        rates[item] = 1.0/rates[item]
    return rates

def read_CurrencyRate(path):
    file = open(path, "r")
    data = simplejson.loads(file.read())
    file.close()
    return invertRates(data["rates"])

def updateDoge(BTC_USD_rate):
    try:
        website = "https://www.coins-e.com/api/v2/market/DOGE_BTC/depth/"
        
        opener = urllib2.urlopen(website, timeout = 15)
        content = simplejson.loads(opener.read())
        opener.close()
        
        return (float(content["ltp"])*BTC_USD_rate)
    except Exception as error:
        print "Error appeared", str(error)
        return False
        
    
def findGroup(item, conv):
    for group in conv:
        trueCase = get_true_case(item, group, conv)
        if trueCase != False:
            return True, group, trueCase
        #if item in conv[group]:
        #    return True, group
    return False, None, False

def matchGroup(item1, item2, conv):
    for group in conv:
        trueCase1 = get_true_case(item1, group, conv)
        trueCase2 = get_true_case(item2, group, conv)
        if trueCase1 != False and trueCase2 != False:
            # We have found the correct cases of the strings item1 and item2!
            return True, group, trueCase1, trueCase2
    
    # We haven't been successful and have to return placeholder values
    return False, None, False, False

def get_true_case(item, group, dataDict):
    for key in dataDict[group]:
        if item.lower() == key.lower():
            return key
    
    return False




# We check if the local file with the currency exchange rates exists locally.
# If not, we try to download it or use fall-back data
# the fall back data is slightly less accurate and needs to be kept up to date manually.
try:
    conversion["currency"] = read_CurrencyRate(currency_path)
    alias["currency"] = {"euro" : "eur", "dollar" : "usd", "pound" : "gbp", "yen" : "jpy", "bitcoin" : "btc"}
    
    dogeRate = updateDoge(conversion["currency"]["BTC"])
    if dogeRate != False: 
        conversion["currency"]["DOGE"] = dogeRate
        alias["currency"]["dogecoin"] = "doge"
    
except Exception as error:
    print "ERROR: "+str(error) 
    
    result = UpdateRates(appid, currency_path)
    
    # Downloading the rates can fail due to various reasons: invalid appid or the website is down
    # If downloading fails, let's use some placeholder data
    if result == None:
        # Euro, US Dollar, British Pound, Japanese Yen, Australian Dollar, Canadian Dollar
        conversion["currency"] = {"eur" : 1/0.7266, "usd" : 1.0, "gbp" : 1/0.6139, "jpy" : 1/102.969, "aud" : 1/1.1206, "cad" : 1/1.0579}
        alias["currency"] = {"euro" : "EUR", "dollar" : "USD", "pound" : "gbp", "yen" : "jpy"}
    else:
        conversion["currency"] = result
        alias["currency"] = {"euro" : "eur", "dollar" : "usd", "pound" : "gbp", "yen" : "jpy", "bitcoin" : "btc"}
        
        dogeRate = updateDoge(conversion["currency"]["BTC"])
        if dogeRate != False: 
            conversion["currency"]["DOGE"] = dogeRate
            alias["currency"]["dogecoin"] = "doge"

def __initialize__(self, Startup):
    #if Startup == True:
    self.unit_conversion = conversion

def execute(self, name, params, channel, userdata, rank):
    if len(params) == 1 and params[0].lower() == "update" and rank == "@@":
        data = UpdateRates(appid, currency_path)
        if data == None:
            self.sendChatMessage(self.send, channel, "Failed to update the currency exchange rates.")
        else:
            self.unit_conversion["currency"] = data
            
            dogeRate = updateDoge(conversion["currency"]["BTC"])
            if dogeRate != False: 
                self.unit_conversion["currency"]["DOGE"] = dogeRate
                
            self.sendChatMessage(self.send, channel, "Updated currency exchange rates.")
            
    elif len(params) == 4 and params[2].lower() in words or len(params) == 3 and params[2].lower() not in words:
        num = params[0]
        
        unit1 = params[1].lower()
        unit2 = len(params) == 4 and params[3].lower() or params[2].lower()
        
        
        doesMatch, group, alias_unit1, alias_unit2 = matchGroup(unit1, unit2, self.unit_conversion)
        
        # Case 1: unit1 and unit2 are both not aliases/alternative names 
        # or not contained within the same group
        if not doesMatch:
            # To avoid long if/else chains, we will do both searches at once
            # 1st check: unit1 is alias, unit2 is normal
            # 2nd check: unit1 is normal, unit2 is alias
            match_alias1, alias_group1, alias_case1 = findGroup(unit1, alias)
            match_normal2, norm_group2, norm_case2 = findGroup(unit2, self.unit_conversion)
            
            
            match_normal1, norm_group1, norm_case1 = findGroup(unit1, self.unit_conversion)
            match_alias2, alias_group2, alias_case2 = findGroup(unit2, alias)
            
            # Case 2.1
            # If a match has been found for both searches, but the groups don't match,
            # we check the group of the normal unit if the alias is contained
            if match_alias1 == True and match_normal2 == True and alias_group1 != norm_group2:
                if alias_case1 in alias[norm_group2]:
                    doesMatch = True
                    group = norm_group2
                    unit1 = alias[norm_group2][alias_case1]
                    
                    unit1 = get_true_case(unit1, norm_group2, self.unit_conversion)
                    unit2 = norm_case2
                    
            elif match_alias2 == True and match_normal1 == True and alias_group2 != norm_group1:
                if alias_case2 in alias[norm_group1]:
                    doesMatch = True
                    group = norm_group1
                    unit2 = alias[norm_group1][alias_case2]
                    
                    unit1 = norm_case1
                    unit2 = get_true_case(unit2, alias_group2, self.unit_conversion)
                    
            # Case 3.1: unit1 is an alias, unit2 is not an alias, both are contained in the same group
            elif match_alias1 == True and match_normal2 == True and alias_group1 == norm_group2:
                print alias, alias_group1, alias_case1
                unit1 = alias[alias_group1][alias_case1]
                
                unit1 = get_true_case(unit1, alias_group1, self.unit_conversion)
                unit2 = norm_case2
                
                doesMatch = True
                group = alias_group1
                
            # Case 3.2: unit1 is not an alias, unit2 is an alias, both are contained in the same group
            elif match_alias2 == True and match_normal1 == True and norm_group1 == alias_group2:
                unit2 = alias[norm_group1][alias_case2]
                
                unit1 = norm_case1
                unit2 = get_true_case(unit2, norm_group1, self.unit_conversion)
                
                doesMatch = True
                group = norm_group1
                
            #Case 4: unit1 and unit2 are both aliases, and contained within the same group
            # or unit1 and unit2 do not exist within the same group or do not exist at all
            else:
                doesMatch, group, unit1_case, unit2_case = matchGroup(unit1, unit2, alias)
                # At this point, we have traversed the dictionary a few times which is not very good
                # Does anybody know a better way to do it?
                if doesMatch:
                    unit1 = alias[group][unit1_case]
                    unit2 = alias[group][unit2_case]
                    
                    unit1 = get_true_case(unit1, group, self.unit_conversion)
                    unit2 = get_true_case(unit2, group, self.unit_conversion)
                else:
                    self.sendChatMessage(self.send, channel, "Incompatible or unknown units")
        else:
            unit1 = alias_unit1
            unit2 = alias_unit2
                
        if doesMatch:
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
                    
            base = self.unit_conversion[group][unit1] * num
            fin = (1.0/float(self.unit_conversion[group][unit2]))*base
            
            self.sendChatMessage(self.send, channel, "{0} {1} = {3} {2}".format(num, unit1, unit2, fin))
            
    elif len(params) > 3 and params[2].lower() not in words or len(params) > 4:
        self.sendChatMessage(self.send, channel, "Too many arguments")
        
    else:
        self.sendChatMessage(self.send, channel, "Not enough arguments")
        
        
    

