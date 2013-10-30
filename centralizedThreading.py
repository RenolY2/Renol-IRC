import threading
import multiprocessing
import traceback

class FunctionNameAlreadyExists(Exception):
    def __init__(self, eventName):
        self.name = eventName
    def __str__(self):
        return self.name
    
class ThreadTemplate(threading.Thread):
    def __init__(self, name, function, pipe_Thread, pipe_Main):
        threading.Thread.__init__(self)
        self.function = function
        self.name = name
        # toThread is the Queue that is used by the thread to receive data
        # fromThread is used by the thread to send data to outside of the thread
        self.ThreadPipe = pipe_Thread
        self.MainPipe = pipe_Main
        self.running = False
        
        self.signal = False
        
    def run(self):
        self.running = True
        try:
            self.function(self, self.ThreadPipe)#, self.Thread.send)
        except Exception as error:
            self.ThreadPipe.send({"action" : "exceptionOccured", "exception" : error, "functionName" : self.name, "traceback" : str(traceback.format_exc())})
            
        self.running = False


class ThreadPool():
    def __init__(self):
        self.pool = {}
    
    def addThread(self, name, function):
        toMain, toThread = multiprocessing.Pipe(True)#, multiprocessing.Pipe(True) 
        
        if name in self.pool:
            raise FunctionNameAlreadyExists("The name is already used by a different thread function!")
        
        thread = ThreadTemplate(name, function, toThread, toMain)
        self.pool[name] = {"thread" : thread, "read" : toMain, "write" : toThread}
        self.pool[name]["thread"].start()
        
        #return toMain, toThread
    
    def sigquitThread(self, name):
        self.pool[name]["thread"].signal = True
        del self.pool[name]
    
    def send(self, name, obj):
        self.pool[name]["read"].send(obj)
    
    def recv(self, name):
        return self.pool[name]["read"].recv()
    
    def poll(self, name, timeout = 0.1):
        return self.pool[name]["read"].poll(timeout)
        
    
    def sigquitAll(self):
        threads = [name for name in self.pool]
        
        for thread in threads:
            self.pool[thread]["thread"].signal = True
            del self.pool[thread]
        
        