import imp

ID = "newload"
permission = 3

"""def LoadNewModules(self,path):     
    ModuleList = self.__ListDir__(path)
    self.__CMDHandler_log__.info("Loading modules in path '%s'...", path)
    Packet = {}
    for i in ModuleList:
        self.__CMDHandler_log__.debug("Loading file %s in path '%s'", i, path)
        module = imp.load_source(i[0:-2], path+"/"+i)
        #print i
        Packet[module.ID] = (module, path+"/"+i)
        
        try:
            if not callable(module.__initialize__):
                module.__initialize__ = False
                self.__CMDHandler_log__.log(0, "File %s does not use an initialize function", i)
        except AttributeError:
            module.__initialize__ = False
            self.__CMDHandler_log__.log(0, "File %s does not use an initialize function", i)
        
            
        Packet[module.ID] = (module, path+"/"+i)
        #Packet[i[1].lower()].PATH = path + "/"+i[2]
        #self.Packet[i[1]] = self.Packet[i[1]].EXEC()
    
    print "ALL MODULES LOADED"   
    self.__CMDHandler_log__.info("Modules in path '%s' loaded.", path)
    return Packet"""


def execute(self, name, params, channel, userdata, rank):
    files = self.__ListDir__("commands")
    print files
    currentlyLoaded = [self.commands[cmd][1] for cmd in self.commands]
    
    for item in currentlyLoaded:
        filename = item.partition("/")[2]
        files.remove(filename)
    
    if len(files) == 0:
        self.sendMessage(channel, "No new commands found.")
    else:
        if len(files) == 1:
            self.sendMessage(channel, "1 new command found.")
        else:
            self.sendMessage(channel, "{0} new commands found.".format(len(files)))
        
        for filename in files:
            path = "commands/"+filename
            module = imp.load_source(filename[0:-2], path)
            cmd = module.ID
            
            self.commands[cmd] = (module, path)
            
            try:
                if not callable(module.__initialize__):
                    module.__initialize__ = False
                    self.__CMDHandler_log__.log("File {0} does not use an initialize function".format(filename))
            except AttributeError:
                module.__initialize__ = False
                self.__CMDHandler_log__.log("File {0} does not use an initialize function".format(filename))
            
            if module.__initialize__ != False:
                module.__initialize__(self, True)
            
            self.sendMessage(channel, "{0} has been loaded.".format(path))
            self.__CMDHandler_log__.info("File {0} has been newly loaded.".format(filename))


def __initialize__(self, Startup):
    entry = self.helper.newHelp(ID)
    
    entry.addDescription("The 'newload' command will load any newly added plugins that have not been loaded yet without reloading other plugins.")
    entry.rank = permission
    
    self.helper.registerHelp(entry, overwrite = True)