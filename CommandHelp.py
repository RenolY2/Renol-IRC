


class HelpEntity():
    def __init__(self, cmdname):
        self.cmdname = cmdname
        
        self.arguments = []
        
        self.description = []
        
        self.rank = 0
    
        self.custom_handler = None
        
    def addDescription(self, description):
        if isinstance(description, basestring):
            self.description.append(description)
        else:
            raise TypeError("Wrong type! Should be subclass of basestring, but is {0}: {1}".format(type(description), description))
    
    def addArgument(self, argument, description = None, optional = False):
        if not isinstance(argument, basestring):
            raise TypeError("Wrong type! Should be subclass of basestring, but is {0}: {1}".format(type(argument), argument))
        
        if optional != False and optional != True:
            raise TypeError("Wrong type! Variable 'optional' should be False or True, but is {0}: {1}".format(type(description), description))
        
        if description == None:
            self.arguments.append((argument, None, optional))
        elif isinstance(description, basestring):
            self.arguments.append((argument, description, optional))
        else:
            raise TypeError("Wrong type! Variable 'description' should be None or subclass of basestring, but is {0}: {1}".format(type(description), description))
    
    def setCustomHandler(self, func):
        if not callable(func):
            raise TypeError("Wrong type! Custom handler should be callable, but is {0}: {1}".format(type(func), func))
        else:
            self.custom_handler = func
    
    def __run_custom_handler__(self, bot_self, *args):
        self.custom_handler(bot_self, *args)
        
class HelpModule():
    def __init__(self):
        self.helpDB = {}
    
    def newHelp(self, cmdname):
        return HelpEntity(cmdname)
    
    def registerHelp(self, helpObject, overwrite = False):
        if not isinstance(helpObject, HelpEntity):
            raise TypeError("Invalid Object provided: '{0}' (type: {1})".format(helpObject, type(helpObject)))
        elif helpObject.cmdname in self.helpDB and overwrite == False:
            raise RuntimeError("Conflict Error: A command with such a name already exists!")
        elif helpObject.cmdname in self.helpDB and overwrite == True:
            print "ATTENTION: A command with such a name is already registered."
            self.helpDB[helpObject.cmdname] = helpObject
        else:
            self.helpDB[helpObject.cmdname] = helpObject
    
    def unregisterHelp(self, cmdname):
        del self.helpDB[cmdname]
        
    
    def getCmdHelp(self, cmdname):
        return self.helpDB[cmdname]