
import random

class MykeyClass:
 	
    def __init__(self, key = ''):
        if key == '':
            self.key = self.generate()
        else:
            self.key = key.lower()

    def generate(self):
        key = ''
        chunk=''
        check_digit_count = 0
        alphabet = 'abcdefghijklmnopqrstuvwxyz1234567890'
        while True:
            while len(key) < 25:
                char = random.choice(alphabet)
                key += char
                chunk += char
                if len(chunk) == 4:
                    key += '-'
                    chunk = ''
            key = key[:-1]
            if MykeyClass(key).verify():
                return key
            else:
                key = ''


    def verify( self  ):
        score = 0
        check_digit = self.key[0]
        check_digit_count = 0
        chunks = self.key.split('-')
        for chunk in chunks:
            if len(chunk) != 4:
                return False
            for char in chunk:
                if char == check_digit:
                    check_digit_count += 1
                score += ord(char)
        if score == 1772 and check_digit_count == 3:
            return True
        return False
		 		
    def SaveKeyInFile(self, sKey):
        sPath = "./FRkey.txt"
        f= open(sPath,"a+")  
        f.write(f"{sKey}\n")
        f.close()
        


    def __str__(self):
        valid = 'Invalid'
        if self.verify():
            valid = 'Valid'
            self.SaveKeyInFile(self.key.upper())
        return self.key.upper() + ':' + valid
		
    
    
if __name__ == "__main__" :  

    # Key =  MykeyClass('aaaa-bbbb-cccc-dddd-1111')
    # print( Key  )    
    
    for i in range(10):
        abc  = MykeyClass()
        print(abc)
		