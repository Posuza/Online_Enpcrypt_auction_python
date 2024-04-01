import os

class Database:
    def __init__(self):
        #add your db here but make sure it in ".txt"
        self.db_list = ["users.txt","items.txt"]
        # self.create_db_files()
        
# Create single text file 
    def create_newFile(self,file):
        if  file[len(file)-4:len(file)] != ".txt":
            print(f"invalid file extension..{file}")
            return None
        if self.db_file(file) == None:
            f = open(f"{os.getcwd()}/DB/{file}","w")
            f.close()
            print(f"{file}.... is created")
        else:
            pass
            # print(f"{file}.... alredy existed")

# Create Db files
    def create_db_files(self):
        pwd = os.getcwd()
        folder = os.path.join(pwd,"DB")        
        try:
            os.makedirs(folder,exist_ok=False)
        except Exception as err:
            # print(err)
            pass
        for i in self.db_list:
            self.create_newFile(i)
    
#exit db
    def db_file(self,fileName):
            try:
                file = [f for f in os.listdir("DB") if f == fileName].pop()
                if  file:
                    return  f"{os.getcwd()}/DB/{file}"
            except Exception as err:
                print(err)
                return  None

#record dic data:       
    def recod_reload_dic_data(self,file,dic):
        main = {}
        try:
            print
            if self.db_file(file) != None:
                with open(self.db_file(file),"w") as note:
                    for element in dic:
                        note.write(f"{element}: {dic[element]}")
                        note.write("\n")
                with open(self.db_file(file),"r") as note:
                    id =0
                    for line in note: 
                        text = line.strip()
                        # print(text[3:])
                        result= eval(text[3:])
                        id += 1
                        data = {id:result} 
                        main.update(data)
            return main
        except Exception as err:
            print(err)
            return None
#load data from beginning
    def loadBegin(self,file):
        main = {}
        try:
            if self.db_file(file) != None:
                with open(self.db_file(file),"r") as note:
                    id =0
                    for line in note: 
                        text = line.strip()
                        # print(text[3:])
                        result= eval(text[3:])
                        id += 1
                        data = {id:result} 
                        main.update(data)
            return main
        except Exception as err:
            print(err)
            return None
 
    
if __name__ == '__main__':
    db = Database()
    # group = {}
    # newGroup = db.recod_reload_dic_data("new.txt",group)
    
    # print(newGroup)
    # new = db.loadBegin("users.txt")
    # print("hsew",new)
    # print(db.recod_data_infile("user.txt"))
    

