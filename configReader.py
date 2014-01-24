import re

class invalidConfig(Exception):
    def __init__(self, key, line):
        self.line = line+1
        self.key = key
    def __str__(self):
        return "Invalid data on line {0}: {1}".format(self.line, self.key)

class Configuration():
    def __init__(self):
        self.config = {}
        self.template = ["server", "port", "usernick", "pass", "ident", "channels", "prefix", "admins", "loglevel", "force_ipv6"]
        self.configname = "config.txt"
        
        self.found = []
        
    def doesExist(self):
        try:
            temp = open(self.configname, "r")
        except:
            return False
        else:
            temp.close()
            return True
    
    def createNewConfig(self, data = {}):
        config = open(self.configname, "w")
        config.write("")
        config.close()
        
        config = open(self.configname, "a")
        
        for item in self.template:
            val = item in data and data[item] or ""
            config.write("{0} = {1}\n".format(item, val))
        
        config.close()
    
    def loadConfig(self):
        config = open(self.configname, "r")
        
        for i, line in enumerate(config.readlines()):
            
            #print i, line
            match = re.match("\s*(?P<key>\w+)\s*=\s*(?P<val>.+)?\s*",line)
            
            if match != None:
                key, val = match.group("key"), match.group("val")
                
                if val == None:
                    raise invalidConfig("key \'{0}\' has no value".format(key), i)
                elif match == None or key not in self.template:
                    raise invalidConfig("incorrect key: \'{0}\'".format(line.strip()), i)
                key, val = key.strip(), val.strip()
                
                self.config[key] = val
                if key not in self.found:
                    self.found.append(key)
        
        notFound = []
        for key in self.template:
            if key not in self.found:
                notFound.append(key)
        
        if len(notFound) > 0:
            raise RuntimeError("The following keys were not found in config.txt, please add them: "+", ".join(notFound))
    
    def getChannels(self):
        chans = self.config["channels"].split(",")
        newchans = []
        for chan in chans:
            chan = chan.strip()
            if chans[0].isalnum():
                newchans.append("#"+chan)
            else:
                newchans.append(chan)
        
        return newchans
    
    def getAdmins(self):
        admins = self.config["admins"].split(",")
        newadmins = []
        for admin in admins:
            admin = admin.strip()
            newadmins.append(admin)
            
        return newadmins