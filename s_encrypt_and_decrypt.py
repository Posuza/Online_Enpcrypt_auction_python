import random


class A3Encryption():
    def __init__(self):
        self.encrypted_data = ''
        self.randomKey = random.randint(1, 65536)

    def start_encryption(self, text, key):
        encrypted_data = ''
        # NationalCyberCity
        totalKey = 0
        for i in key:
            totalKey += ord(i)

        key = int(bin(totalKey)[2:])

        for i in text:
            # print(int(bin(ord(i))[2:]) , int(bin(totalKey)[2:]))
            # print("check",type(ord(totalKey)))
            encrypted_ord = ord(i) ^ totalKey
            doubleEncrypted_rod = encrypted_ord ^ self.randomKey
            # print(doubleEncrypted_rod)
            # print(int(bin(encrypted_ord)[2:]))

            encrypted_data += str(hex(doubleEncrypted_rod)) + 'X'

        encrypted_data += str(hex(totalKey)) + 'X' + str(hex(self.randomKey))
        # print(self.encrypted_data)
        # print(type(self.encrypted_data))
        return encrypted_data


class A3Decryption():

    def __init__(self):
        self.dataList: list = []
        # self.decrypted_data: str=''

    def startDecryption(self, encrypted_data: str):
        decrypted_data =""
        dataList = encrypted_data.split('X')
        keyList = dataList[-2:]
        key = int(keyList[0], 16) # dec
        rKey = int(keyList[1], 16)
        print("user key:", key, ": random key:", rKey)

        for i in range(len(dataList) - 2):
            dDecrypt: int = int(dataList[i], 16) ^ rKey

            decrypted_int = dDecrypt ^ key
            decrypted_data += chr(decrypted_int)
        # print("description",self.decrypted_data)
        return decrypted_data
    
    # def emptyDescript(self):
    #     self.decrypted_data =""
    

if __name__ == "__main__":
    a3 = A3Encryption()
    da3 = A3Decryption()
    encrypted: str = a3.start_encryption("NationalCyberCity", "winhtut")
    decrypted: str =da3.startDecryption(encrypted)
    print("Decrypted data:",decrypted)
