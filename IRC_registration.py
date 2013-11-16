import random

class NameAlreadyExists(Exception):
    def __init__(self, eventName):
        self.name = eventName
    def __str__(self):
        return self.name

class trackVerification():
    def __init__(self, userlist):
        self.users = {}
        for item in userlist:
            self.users[item.lower()] = False
        print self.users
        self.userQueue = []
    
    def doesExist(self, user):
        return user.lower() in self.users
    
    def isQueued(self, user):
        return user.lower() in self.userQueue
    
    def queueUser(self, user):
        user = user.lower()
        if user not in self.userQueue:
            self.userQueue.append(user.lower())
            return True
        else:
            return False
    
    def unqueueUser(self, user):
        user = user.lower()
        if user in self.userQueue:
            self.userQueue.remove(user)
            return True
        else:
            return False
    
    def isRegistered(self, user):
        user = user.lower()
        if user in self.users and self.users[user] == True:
            return True
        else:
            return False
    
    def unregisterUser(self, user):
        user = user.lower()
        self.users[user] = False
    
    def registerUser(self, user):
        user = user.lower()
        self.users[user] = True
    
    def addUser(self, user):
        user = user.lower()
        self.users[user] = True
    
    def remUser(self, user):
        user = user.lower()
        if user in self.users:
            del self.users[user]