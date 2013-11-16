ID = "convert"
permission = 0

words = ["to", "in"]

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

def findGroup(item):
    for group in conversion:
        if item in conversion[group]:
            return True, group
    return False, None

def execute(self, name, params, channel, userdata, rank):
    
    if len(params) == 4 and params[2].lower() in words or len(params) == 3 and params[2].lower() not in words:
        num = params[0]
        
        unit1 = params[1]
        
        unit2 = len(params) == 4 and params[3] or params[2]
        
        unit1_found, group1 = findGroup(unit1)
        unit2_found, group2 = findGroup(unit2)
        
        if unit1_found and unit2_found and group1 != group2:
            self.sendChatMessage(self.send, channel, "Incompatible units")
        elif unit1_found and unit2_found and group1 == group2:
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
                    
            
            base = conversion[group1][unit1] * num
            fin = (1.0/conversion[group1][unit2])*base
            
            self.sendChatMessage(self.send, channel, "{0} {1} = {3} {2}".format(num, unit1, unit2, fin))
        else:
            self.sendChatMessage(self.send, channel, "Unknown units")
    elif len(params) > 3 and params[2].lower() not in words or len(params) > 4:
        self.sendChatMessage(self.send, channel, "Too many arguments")
    else:
        self.sendChatMessage(self.send, channel, "Not enough arguments")
        
        
    

