import logging

import commands.miscLib.VigenereCipher as VigenereCipher

ID = "cipher"
permission = 0
privmsgEnabled = True

help_log = logging.getLogger("HelpModule")

def execute(self, name, params, channel, userdata, rank, chan):
    if len(params) < 3:
        self.sendNotice(name, "Not enough arguments. Check {0}help for information about the command.".format(self.cmdprefix))
    else:
        action = params[0].lower()
        key = params[1]
        
        
        if action == "encrypt":
            text = "".join(params[2:])
            
            if len(params) > 3:
                self.sendNotice(name, "All spaces in your plain text were removed.")
            
            try:
                encrypted = self.VigenereCipher.encrypt(text, key)
            except self.VigenereCipher.LetterNotContainedInAlphabet as error:
                self.sendNotice(name, "Your key or text contains an unsupported symbol: '{0}' in position {1}".format(error.letter,
                                                                                                                      error.pos))
            else:
                if chan == False:
                    self.sendNotice(name, "Your encrypted text: {0}".format(encrypted))
                else:
                    self.sendMessage(channel, "Your encrypted text: {0}".format(encrypted))
            
        elif action == "decrypt":
            text = params[2]
            
            try:
                decrypted = self.VigenereCipher.decrypt(text, key)
            except self.VigenereCipher.LetterNotContainedInAlphabet as error:
                self.sendNotice(name, "Your key or text contains an unsupported symbol: '{0}' in position {1}".format(error.letter,
                                                                                                                      error.pos))
            else:
                if chan == False:
                    self.sendNotice(name, "Your decrypted text: {0}".format(decrypted))
                else:
                    self.sendMessage(channel, "Your decrypted text: {0}".format(decrypted))
        else:
            self.sendNotice(name, "action needs to be 'encrypt' or 'decrypt'. Your action was '{0}'".format(action))

def __initialize__(self, Startup):
    if Startup:
        self.VigenereCipher = VigenereCipher.VigenereCipher()
    
    entry = self.helper.newHelp(ID)
    
    entry.addDescription("The 'cipher' command implements a Vigenere Cipher. Please note that the Vigenere Cipher is not cryptographically secure.")
    entry.addDescription("More dedicated users are able to break the cipher given enough time. But your friends can have a lot of fun trying to decipher your text!")
    entry.addArgument("action", "Needs to be either 'encrypt' or 'decrypt'.")
    entry.addArgument("key", "The key which will be used for the cipher.")
    entry.addArgument("text", "The text to be encrypted or decrypted, depending on your choosen action.")
    entry.rank = 0
    
    self.helper.registerHelp(entry, overwrite = True)