import random
import socket
import time
import urllib
import simplejson
import re
import traceback
import sys
import threading
import Queue

class ThreadShuttingDown(Exception):
    def __init__(self, nameOfThread, time):
        self.name = nameOfThread
        self.time = time
    def __str__(self):
        return "{0} has been shut down! Tried to call readMsg at {1}".format(self.name, self.time) 

class IRC_reader(threading.Thread):
    def __init__(self, serverSock): #host, port):
        threading.Thread.__init__(self)
        #self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.conn.settimeout()
        #self.host = host
        #self.port = port
        self.sock = serverSock
        self.ready = True
        self.line = ""
        
        self.buffer = Queue.Queue()
        
    def run(self):
        #self.conn.connect(self.host, self.port)
        
            while self.ready == True:
                try:
                    char = self.sock.recv(1)
                except Exception as error:
                    print 
                    print "ERROR: "+str(error)
                    print
                    self.ready = False
                    break
                else:
                    if char != "":
                        #print char
                        self.line += char
                        
                    # Check if current character is a LF and last character was a CL, if so: Put line into buffer!    
                    if len(self.line) > 1 and ord(char) == 10 and ord(self.line[-2]) == 13:
                        #print "RECEIVED: "+self.line
                        self.buffer.put(self.line[0:-2], True)         # Omit these annoying CL-LF's, we do not need them anymore!
                        self.line = ""
            print "ReadThread is down!"
        
    
    def readMsg(self):
        if self.ready == False:
            raise ThreadShuttingDown("readThread", time.time())
        else:
            return self.buffer.get_nowait()


class IRC_writer(threading.Thread):
    def __init__(self, serverSock):#, host, port):
        threading.Thread.__init__(self)
        
        #self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.conn.settimeout()
        #self.host = host
        #self.port = port
        self.sock = serverSock
        self.ready = True
        self.line = ""
        self.signal = False
        self.died = False
        
        self.buffer = Queue.Queue()
        
    def run(self):
        #self.conn.connect(self.host, self.port)
        
        while self.ready == True:
            try:
                toSend = self.buffer.get_nowait()
                self.sock.send(toSend)
                time.sleep(1.5)
                #print "SENT: "+toSend
                
            except Queue.Empty:
                # an attemt to fix the bug that causes the writeThread to hang indifinitely because it receives no more data from the Queue
                if self.signal == False:
                    # it's empty? oh well, better luck next time
                    time.sleep(0.05) 
                else:
                    # the signal to turn the thread off has been set? Ok, time to break out of the loop
                    self.ready = False
                    
            except Exception as error:
                print 
                print "ERROR: "+str(error)
                print
                self.ready = False
                break
            else:
                if self.signal == True and self.buffer.empty():
                    self.ready = False
            #else:
            #    self.ready = False
            #    self.sock.close()
            #    print "SHIT GOES LOSE, WE CAN'T SEND ANYTHING TO SERVER"
        print "SendThread is down!"
    
    def waitUntilEmpty(self):
        self.buffer.join()
    
    def sendMsg(self, msg, priority = False):
        msg = msg.replace(chr(13), " ")
        msg = msg.replace(chr(10), " ")
        self.buffer.put(msg+chr(13)+chr(10))