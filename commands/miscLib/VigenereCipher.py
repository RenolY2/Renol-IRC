import StringIO

class VigenereCipher():
    def __init__(self, alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
        self.alphabet = alphabet
        self.vigTable = self.VigenereTable(alphabet)

    class VigenereTable():
        # precalculating a Vigenere table using the alphabet
        def __init__(self, alphabet):
            self.alphabet = alphabet
            
            self.rows = []
            self.letterPos = {}
            
            alphabet_table = [letter for letter in alphabet]
            
            for i in xrange(26):
                self.letterPos[alphabet_table[0]] = i
                self.rows.append(alphabet_table)
                
                alphabet_table = list(alphabet_table)
                
                # remove the first item and add it to the end
                alphabet_table.append(alphabet_table.pop(0))
        
        # Based on the letter from the key and the letter from the plain text, we return a new letter
        def getResult(self, keyLetter, plainTextLetter):
            row = self.rows[self.letterPos[keyLetter]]
            result = row[self.letterPos[plainTextLetter]]
            
            return result
        
        # We search for the position of the encrypted letter in the row.
        # Once we found it, we will return a letter from the alphabet according
        # to the position of the encrypted letter in the row.
        def getColumn(self, keyLetter, encryptedLetter):
            row = self.rows[self.letterPos[keyLetter]]
            columnNumber = row.index(encryptedLetter)
            
            return self.alphabet[columnNumber]
            
            
    def __encryptORdecrypt__(self, text, key, mode):
        # The operations for decrypting and encrypting are identical.
        # The only difference is the way the decrypted or encrypted letter
        # is retrieved from the Vigenere table. So we will merge both
        # operations in a single function.
        if mode not in ("encrypt", "decrypt"):
            raise RuntimeError("mode needs to be 'encrypt' or 'decrypt'")
        else:
            # We will only work with the upper case variants of the plain text and key
            text, key = text.upper(), key.upper()
            
            # Check for unknown symbols in the key and plaintext
            self.validateString(text)
            self.validateString(key)
            
            keyLength = len(key)
            
            resultText = StringIO.StringIO()
            
            for position, letter in enumerate(text):
                keyLetter = key[position%keyLength]
                
                if mode == "encrypt":
                    resultLetter = self.vigTable.getResult(keyLetter, letter)
                elif mode == "decrypt":
                     resultLetter = self.vigTable.getColumn(keyLetter, letter)
                
                resultText.write(resultLetter)
            
            finalText = resultText.getvalue()
            resultText.close()
            
            return finalText
    
    def encrypt(self, plainText, key):
        return self.__encryptORdecrypt__(plainText, key, "encrypt")
    
    def decrypt(self, encryptedText, key):
        return self.__encryptORdecrypt__(encryptedText, key, "decrypt")
    
    def validateString(self, string):
        for position, letter in enumerate(string):
            if letter not in self.alphabet:
                raise self.LetterNotContainedInAlphabet(letter, position)
                
    class LetterNotContainedInAlphabet(Exception):
         def __init__(self, letter, position):
            self.letter = letter
            self.pos = position
             
         def __str__(self):
             return "The following letter (on position = {0}) does not exist: {1}".format(self.pos, self.letter)

if __name__ == "__main__":
    
    vigCipher = VigenereCipher()
    
    plainText = "attackatdawn"
    print plainText
    
    encryptedText = vigCipher.encrypt(plainText, "LEMON")
    print encryptedText
    
    decryptedText = vigCipher.decrypt(encryptedText, "LEMON")
    print decryptedText