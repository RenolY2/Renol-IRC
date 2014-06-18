import sqlite3

from cStringIO import StringIO

ALLOWEDCHARS = '-0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}'

class InvalidCharacterUsed(Exception):
    def __init__(self, string, char, pos):
        self.string = string
        self.char = char
        self.pos = pos
        
    def __str__(self):
        hexChar = hex( ord(self.char) )
        return "String contains invalid character {0} on position {1}".format(hexChar, self.pos)

class NoSuchBanGroup(Exception):
    def __init__(self, groupName):
        self.group = groupName
        
    def __str__(self):
        return "No such ban group exists: '{0}'".format(self.group)


class BanList:
    def __init__(self, filename):
        self.ESCAPESTRING = ""
        
        self.conn = sqlite3.connect(filename)
        self.cursor = self.conn.cursor()
        
        # Create table for bans
        self.cursor.execute(""" 
                            CREATE TABLE IF NOT EXISTS Banlist(groupName TEXT, pattern TEXT, timestamp INTEGER, banlength INTEGER)
                            """)
        
        # Create table for the names of the ban groups.
        # This will be used to check if a group exists
        # when checking if a user is banned in that group.
        self.cursor.execute(""" 
                            CREATE TABLE IF NOT EXISTS Bangroups(groupName TEXT)
                            """)
        
        self.defineGroup("Global")
        
        
    # You need to define a group name if you want
    # to have your own ban groups.
    # This should prevent accidents in which an user
    # is banned in a group that doesn't exist.
    def defineGroup(self, groupName):
        doesExist = self.__groupExists__(groupName)
        
        if not doesExist:
            self.cursor.execute(""" 
                                INSERT INTO Bangroups(groupName)
                                VALUES (?)
                                """, (groupName, ) )
            self.conn.commit()
            # True means that a new group has been defined.
            return True
        
        # False means that no new group has been defined, i.e.
        # the group already exists.
        return False
            
    
    
        
        
        
    def banUser(self, user, ident = "*", host = "*", groupName = "Global", 
                timestamp = -1, banlength = -1):
        banstring = self.__assembleBanstring__(user, ident, host).lower()
        
        if not self.__groupExists__(groupName):
            raise NoSuchBanGroup(groupName)
        
        if not self.__banExists__(groupName, banstring):
            self.__ban__(banstring, groupName, timestamp, banlength)
            
            # The operation was successful
            return True
        else:
            # The pattern is already banned.
            # We don't need to do anything.
            
            # The Operation was not successful
            return False
            
            
        
    def unbanUser(self, user, ident = "*", host = "*",
                  groupName = "Global"):
        banstring = self.__assembleBanstring__(user, ident, host).lower()
        
        if not self.__groupExists__(groupName):
            raise NoSuchBanGroup(groupName)
        
        if self.__banExists__(groupName, banstring):
            self.__unban__(banstring, groupName)
            
            # The operation was successful
            return True
        else:
            # The pattern is not banned.
            # We don't need to do anything.
            
            # The operation was not successful 
            return False
    
    def clearBanlist_all(self):
        self.cursor.execute(""" 
                            DELETE FROM Banlist
                            """)
        self.conn.commit()
    
    def clearBanlist_group(self, groupName):
        self.cursor.execute(""" 
                            DELETE FROM Banlist
                            WHERE groupName = ?
                            """, (groupName, ) )
        self.conn.commit()
        
    
    def getBans(self, groupName = None, matchingString = None):
        if groupName == None:
            if matchingString == None:
                self.cursor.execute(""" 
                                    SELECT * FROM Banlist
                                    """)
            else:
                self.cursor.execute(""" 
                                    SELECT * FROM Banlist
                                    WHERE ? GLOB pattern
                                    """, (matchingString.lower(), ))
            
            return self.cursor.fetchall()
        else:
            if self.__groupExists__(groupName):
                if matchingString == None:
                    self.cursor.execute(""" 
                                        SELECT * FROM Banlist
                                        WHERE groupName = ?
                                        """, (groupName, ))
                else:
                    self.cursor.execute(""" 
                                        SELECT * FROM Banlist
                                        WHERE groupName = ? AND ? GLOB pattern
                                        """, (groupName, matchingString.lower()))
                    
                return self.cursor.fetchall()
                    
            else:
                raise NoSuchBanGroup(groupName)
    
    
    
    def checkBan(self, user, ident, host,
                      groupName = "Global"):
        
        if not self.__groupExists__(groupName):
            raise NoSuchBanGroup(groupName)
        else:
            #escapedUser = self.__createString_forSQL__(user)
            #escapedIdent = self.__createString_forSQL__(ident)
            #escapedHost = self.__createString_forSQL__(host)
            
            #banstring = "{0}!{1}@{2}".format(escapedUser, escapedIdent, escapedHost)
            banstring = "{0}!{1}@{2}".format(user, ident, host).lower()
            
            self.cursor.execute(""" 
                                SELECT * FROM Banlist
                                WHERE groupName = ? AND ? GLOB pattern
                                """, (groupName, banstring))#, self.ESCAPESTRING))
            
            result = self.cursor.fetchone()
            
            if result != None:
                return True, result
            else:
                return False, None
    
    def getGroups(self):
        self.cursor.execute(""" 
                            SELECT groupName FROM Bangroups
                            """)
        
        result = self.cursor.fetchall()
        return result
    
    def __assembleBanstring__(self, user, ident, host):
        escapedUser = self.__createString_forSQL__(user)
        escapedIdent = self.__createString_forSQL__(ident)
        escapedHost = self.__createString_forSQL__(host)
        
        banstring = "{0}!{1}@{2}".format(escapedUser, escapedIdent, escapedHost)
        
        return banstring
        
    def __ban__(self, banstring, groupName = "Global", timestamp = -1, banlength = -1):
        self.cursor.execute(""" 
                            INSERT INTO Banlist(groupName, pattern, timestamp, banlength)
                            VALUES (?, ?, ?, ?)
                            """, (groupName, banstring, timestamp, banlength))
        
        self.conn.commit()
        
    def __unban__(self, banstring, groupName = "Global"):
        self.cursor.execute(""" 
                            DELETE FROM Banlist
                            WHERE groupName = ? AND pattern = ?
                            """, (groupName, banstring))
        
        self.conn.commit()
    
    
    def __banExists__(self, groupName, banstring):
        self.cursor.execute(""" 
                            SELECT 1 FROM Banlist
                            WHERE groupName = ? AND pattern = ?
                            """, (groupName, banstring) )
        
        result = self.cursor.fetchone()
        print result, type(result)
        if result != None and result[0] == 1:
            return True
        else:
            return False
    
    def __groupExists__(self, groupName):
        self.cursor.execute(""" 
                            SELECT 1 FROM Bangroups
                            WHERE groupName = ?
                            """, (groupName, ) )
        
        result = self.cursor.fetchone()
        print result, type(result)
        if result != None and result[0] == 1:
            return True
        else:
            return False
        
    def __stringIsValid__(self, string):
        for char in string:
            if char not in ALLOWEDCHARS:
                return False
        
        return True
    # The createString_forSQL function takes a string and
    # formats it according to specific rules.
    # It also prevents characters that aren't in
    # the ALLOWEDCHARS constant to be used so that
    # characters not allowed in specific IRC arguments
    # (nickname, ident, host) appear in the string.
    #
    # It is not very specific and is only useful for 
    # very simple filtering so that unicode characters
    # or special characters aren't used.
    def __createString_forSQL__(self, string):
        escape = ""
        not_escape = "*?"
        newString = StringIO()
        
        for pos, char in enumerate(string):
            # We try reverse-escaping: 
            # - escaped chars will be written as literals
            # - non-escaped chars included in the escape string will be escaped
            # pos == 0 is an exception because characters at this
            # position cannot be escaped in any way that makes sense.
            if char == self.ESCAPESTRING:
                continue
            if pos > 0 and string[pos-1] == self.ESCAPESTRING or char in not_escape:
                newString.write(char)
            elif char in escape:
                newString.write(self.ESCAPESTRING+char)
            else:
                if char not in ALLOWEDCHARS:
                    raise InvalidCharacterUsed(string, char, pos)
                else:
                    newString.write(char)
                    
        return newString.getvalue()
    
    

myBans = BanList("Banlist.db")
myBans.clearBanlist_all()
myBans.banUser("TestU*er", "baMybutt", "*")
myBans.banUser("ABS", "*", "*")

print myBans.getBans(None, "abs!bamybutt@b"), "wut"
#print myBans.getBans()
#print myBans.unbanUser("TestUasdsadasser", "baMybutT", "*")
print myBans.getBans()
print myBans.checkBan("TestUser", "baMybuTT", "Hello")
print myBans.getGroups()
myBans.clearBanlist_group("derp")