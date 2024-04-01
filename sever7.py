import socket
import threading
from datetime import datetime
import time
import s_encrypt_and_decrypt
from dbmodel import Database
import sever_util 

class Server():
    def __init__(self):
        self.ip = "localhost"
        self.port = 9193
    #Import variables
        self.util = sever_util.dic_util()
        # create Database (user.txt,item.text,block.text.....)
        self.dbModel = Database()
        self.dbModel.create_db_files()
        
        self.encrypt = s_encrypt_and_decrypt.A3Encryption()
        self.decrypt = s_encrypt_and_decrypt.A3Decryption()

    #variable

        #dic for mutistore
        self.groups = {}
        self.auctionsItems = self.dbModel.loadBegin("items.txt")
        self.users =self.dbModel.loadBegin("users.txt")

        self.send_user={}
        self.clients={}
        self.send_members =[]

        self.tickler= 0
        self.tickle = False
        self.tickel_restart = False
 
    #Main
    def main(self):
        self.server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server.bind((self.ip,self.port))
        self.server.listen()
        print("Server listen on port: {}  and  ip {}".format(self.port,self.ip))

        thread1 = threading.Thread(target=self.establish_connection)
        thread1.start()
        thread2 = threading.Thread(target=self.itemStaus)
        thread2.start()
        
    #itme status inactivate 
    def itemStaus(self):
        while True:
            try:
                # if self.util.dic_length(self.users)>0:
                #     self.users =self.dbModel.recod_reload_dic_data("users.txt",self.users)
                # else:
                #     print("no data in users db")
                if self.util.dic_length(self.auctionsItems) > 0: 
                    for i in self.auctionsItems:
                        if self.auctionsItems[i]["status"] == "active":
                            d1= datetime.strptime(self.auctionsItems[i]["endTime"],'%Y-%m-%d (%H:%M:%S)')
                            d2 = d1- datetime.now()
                            f = str(d2).split('.')[0]
                            if f[0] == "-":
                                self.auctionsItems[i]["status"] = "Inactive"
                    self.auctionsItems =self.dbModel.recod_reload_dic_data("items.txt",self.auctionsItems)
                else:
                    print("no data in items db")
                
            except Exception as err:
                print(err)
            time.sleep(20)

    #connection established
    def establish_connection(self):
            while True:
                client, address = self.server.accept()
                print(f'{str(address)} is try to connect the sever!')

                message = {"header":"connect>",
                        "body":"you connected to sever successful.."}
                sms = f"{message}"
                client.send(sms.encode('utf-8'))

                try:
                    thread = threading.Thread(target=self.handle_clients, args=(client,))
                    thread.start()
                except Exception as err:
                    print("connection fail error")



    #handle clients
    def handle_clients(self,client):
        
        loginUser= ""
        while True:  
            message = {}       
            try:
                encry_message = client.recv(4096).decode("utf-8")
                message = self.decrypt.startDecryption(encry_message)
                client_message = eval(message)
                # print(type(client_message))
                header = client_message["header"]
                body = client_message["body"]
                print(client_message)

    #---------------------------user operation-----------------------------
                
                #request users
                if  header == "+req_users":
                    send_header = "#req_users"
                    info = ">Successful request, users data for crud.."
                    message ={"header":send_header,"body":{"info":info,"users":self.users}}

                #login Section
                elif  header == "+login":
                    user,i = self.util.dic_search(self.users,body["email"],"email")
                    if user:
                        if body["email"] == user["email"] and body["password"] == user["password"] and user["status"] != "login":

                            updateStatus = self.updateUser(user["userName"],"userName","login","status")
                            print(f">>{user['userName']} login_status is {updateStatus}")

                            self.clients.update({self.util.dic_length(self.users)+1:{"userName":user["userName"],"client":client}})
                            loginUser = user['userName']

                            send_header = "#login_sucessful"
                            info = ">Login successful...."   
                        else: 
                            send_header = "!loginPassword"
                            info = "!Invalid password from sever.."
                            user =None
                    else:
                        send_header = "!login"
                        info = "!Invalid UserName from sever.."
                        user =None
                    message ={"header":send_header,"body":{"info":info,"user":user}}
                    

                #register Section
                elif  header == "+creatUser":
                    newUser= body["user"]
                    creatUser = self.creatUser(newUser["userName"],newUser["email"],newUser["password"],newUser["phone"],"No bio yet",newUser["role"],"logout")
                    if creatUser == newUser["userName"]:
                        send_header = "!register"
                        info = f"\n???{creatUser} alredy existed try other"
                    elif creatUser == newUser["email"]:
                        send_header = "!register"
                        info = f"\n???{creatUser} alredy existed try other"
                    else:
                        print(self.users)
                        send_header = "#creatUser"
                        info = ">Successful create user .."
                    message ={"header":send_header,"body":{"info":info}}

                # delete user
                elif header=="+deleUser":
                    print(f"__delete user: {body['userName']}__")
                    user = body['userName']
                    dele_user = self.deleteUser(user)
                    print("afataifherer",dele_user)
                    if dele_user == True:
                        send_header = "#deleUser"
                        info = "successful delete user.."
                    else:
                        send_header = "!deleUser"
                        info = "user not found or failed to dele try agian"      
                    message ={"header":send_header,"body":{"info":info}}

                # Update User value
                elif header=="+upDateUserInfo":
                    print(f"--------update: {body['userName']}_{body['request'][7:]}------")
                    userName = body['userName']
                    upValue = body["upValue"]
                    #update userName
                    if body["request"] == f"+update{body['request'][7:]}":
                        value_type = body['request'][7:]
                        print(userName,value_type,upValue)
                        if value_type == "userName":    
                            update_info = self.updateUser(userName,value_type,upValue,value_type)
                            if update_info == True:
                                userName = upValue
                        else:
                            update_info = self.updateUser(userName,"userName",upValue,value_type)
               
                        if update_info == True:
                            send_header = f"#upDateUserInfo"
                            info = f"successful update user {value_type} .."
                        else:
                            send_header = "!upDateUserInfo"
                            info = f"user not found or failed to update {value_type} try agian"
                    else:
                        send_header = "!upDateUserInfo"
                        info = f"user not found or failed to update {value_type} try agian"
                    user =  self.searchUser(userName)    
                    message ={"header":send_header,"body":{"user":user,"info":info}}


    #-------------------------item opseration---------------------------
                #Admin request items
                elif  header == "+req_items":
                    send_header = "#req_items"
                    info = ">Successful request, auction items data for crud.."
                    if self.util.dic_length(self.auctionsItems) > 0: 
                        items = self.auctionsItems
                    else:
                        items = None
                    message ={"header":send_header,"body":{"info":info,"items":items}}
                
                # request all auction items
                elif header=="+activeItem":   
                    print(f"___Requesting all aution items____")   
                    if  self.util.dic_length(self.auctionsItems) > 0:
                        listActiveItem = self.util.search_dic_byValue_lists(self.auctionsItems,"status","active")
                        if listActiveItem:
                            send_header = "#activeItem"
                            info = "successful request items .."
                    else:
                        send_header = "!activeItem"
                        info = "No active items for polling.."
                        listActiveItem = None
                        
                    message ={"header":send_header,"body":{"items_list":listActiveItem,"info":info}}

                # reqeust own auction item 
                elif header=="+ownItems":
                    print(f"__create newAuction: {body['info']}__")
                    owner = body["owner"]
                    list_items=self.auctionItemByValue("owner",owner)
                    print(list_items)
                    if list_items == None:
                        send_header = "!ownItems"
                        info = "no item of your own"
                    else:
                        send_header = "#ownItems"
                        info = f"your successful request item.."
                        
                    message ={"header":send_header,"body":{"info":info,"list_items":list_items}}

                # create item
                elif header=="+createNewItem":
                    print(f"__create newAuction: {body['title']}__")
                    title = body["title"]
                    owner = body["owner"]
                    endTime  = body["endTime"]
                    created_item = self.creatAuction(title,"",owner,"active",endTime,"","")
                    
                    if created_item == None:
                        send_header = "!createNewItem"
                        info = "items name alredy existed try other"
                    else:
                        print(self.auctionsItems)
                        send_header = "#createNewItem"
                        info = "successful crate item.."
                    message ={"header":send_header,"body":{"info":info}}

                # Update item value
                elif header=="+upDateItem":
                    print(f"__update: {body['itemName']}_{body['request']}___")
                    title = body["itemName"]
                    upValue = body["upValue"]
                    #update title
                    if body["request"] == "+updateTitle":
                        value_type = "title"
                        update_item = self.updatAuction(title,upValue,value_type)
                        title = upValue
                    #update status
                    elif body["request"] == "+updateStatus":
                        value_type = "status"
                        update_item = self.updatAuction(title,upValue,value_type)

                    #update endTime
                    elif body["request"] == "+updateTime":
                        value_type = "endTime"
                        update_item = self.updatAuction(title,upValue,value_type)

                    #update bider
                    elif body["request"] == "+updateBider":
                        print("buyer")
                        value_type = "buyer"
                        update_item = self.updatAuction(title,upValue,value_type)

                    #update price
                    elif body["request"] == "+updatPrice":
                        print("price")
                        value_type = "price"
                        update_item = self.updatAuction(title,upValue,value_type)
                    
                    #update owner
                    elif body["request"] == "+updateOwner":
                        print("owner")
                        value_type = "owner"
                        update_item = self.updatAuction(title,upValue,value_type)
                              
                    if update_item == True:
                        send_header = "#upDateItem"
                        info = f"successful update {value_type} item.."
                    else:
                        send_header = "!upDateItem"
                        info = f"items not found or failed to update {value_type} try agian"
                    print("title",title)
                    item =  self.searchAuction(title)    
                    message ={"header":send_header,"body":{"newItem":item,"info":info}}
  
                # delete item
                elif header=="+deleItem":
                    print(f"__delete acution: {body['itemName']}__")
                    title = body["itemName"]
                    dele_item = self.deletAuction(title)
                    if dele_item == True:
                        send_header = "#deleItem"
                        info = "successful delete item.."
                    else:
                        send_header = "!deleItem"
                        info = "items not found or failed to dele try agian"      
                    message ={"header":send_header,"body":{"info":info}}
                
                # Update Auction value
                elif header == "+itemBidValue":
                    
                    print(f"__update: {body['title']}_{body['info']}___")
                    title = body["title"]
                    bider = body["bider"]
                    price = body["price"]
                    item,i = self.util.dic_search(self.auctionsItems,body["title"],"title")
                    print(item ,i)
                    if item:
                        if self.auctionsItems[i]["price"] == "":
                            update_buyer = self.updatAuction(title,bider,"buyer")
                            update_pirce = self.updatAuction(title,price,"price")
                            print(f"update price success _{update_buyer} {self.auctionsItems[i]['price']}_{update_pirce}")
                        else:
                            if int(price) > int(self.auctionsItems[i]["price"]):
                                update_buyer = self.updatAuction(title,bider,"buyer")
                                update_pirce = self.updatAuction(title,price,"price")
                                print(f"update price success _{update_buyer} {self.auctionsItems[i]['price']}_{update_pirce}")
                            else:
                                print(f"no update pirce to  {self.auctionsItems[i]['price']}")
                    else:
                        print("no item to update price ")
                    message = ""

                #Request biding items
                elif  header == "+bidingItem":
                    item = body["auctItem"]
                    foundItem = self.searchAuction(item)
                    if foundItem:
                        send_header = "#bidingItem"
                        info = ">Successful request biding items.."
                    else:
                        send_header = "!bidingItem"
                        info = "> biding items not found.."
                    message ={"header":send_header,"body":{"info":info,"bidingItem":foundItem}}

                else:
                    message =None

                if message:
                    print(message)
                    encrypted_data = self.encrypt.start_encryption(f'{message}', 'servertcp')

                    client.send(bytes(encrypted_data,"utf-8"))
                    # client.send(bytes(f"{message}","utf-8"))

            #clearance every variable
                send_header =None
                info = None
                message = None
                header = None
                body = None

            except Exception as err:
                print("Error",self.clients)
                user,i = self.util.dic_search(self.users,loginUser,"userName")
                if user:
                    self.users[i]["status"] = "logOut"
                    print(self.users[i])
                else:
                # if self.util.dic_length(self.clients) > 0:
                #     for i in self.clients:
                #         if self.clients[i]["client"] ==  client:
                #             print("TUe")
                #             
                #             if userName:
                #                 self.users[i]["status"] ="logout"
                #                 print(f"{user['userName']} has __ {self.users[i]['status']} __",)
                #             del self.clients[i]  
                # print("????? unknown client disconnected....")
                    message ={"header":"!attempt","info":"attem fail"}
                encrypted_data = self.encrypt.start_encryption(f'{message}', 'servertcp')
                break    


    def send_encry_data(self,data):    
        encrypted_data = self.encrypt.start_encryption(data, self.security_Key)
        self.client.send(bytes(encrypted_data, "utf-8"))

    #sendEncrp data to client
    def send_encry_data(self,client,data): 
        encrypted_data = self.encrypt.start_encryption(data,'servertcp')
        for client in self.clients:  
            client.send(bytes(encrypted_data, "utf-8"))





    ####---------------------------  Users  ------------------------#######

    #------create => True|email|userName------
    def creatUser(self,userName,email,password,phone,bio,role,status):
        if self.util.dic_length(self.users)>0:
            newUser,i = self.util.dic_search(self.users,userName,"userName")
            newEmail,j = self.util.dic_search(self.users,email,"email")
            print("here",newUser,email)
            if newEmail:
                print(f"Email alredy existed try other")
                return email
            elif newUser:
                print("Username alredy taken try other")
                return userName
        self.users.update({self.util.dic_length(self.users)+1:{"userName":userName,"email":email,"password":password,"phone":phone,"bio":bio,"role":role,"status":status}})
        print("herer")
        self.users = self.dbModel.recod_reload_dic_data("users.txt",self.users)
        print("Successful creating user")
        return True

    #------Search user => user:None------
    def searchUser(self,value):
        if self.util.dic_length(self.users)> 0:
            user,i= self.util.dic_search(self.users,value,"userName")
            # ["a","b"]
            users_list = self.util.search_dic_bykey_lists(self.groups,"userName")
            if user:
                return user
            print(f"['{user}'] ->! {users_list}")
            return None
        print("no data in dictionary")  
        return None
        
    #------update => True:None------
    def updateUser(self,find_data,find_type,value,value_type):
        if value_type == "userName" :
            user,i = self.util.dic_search(self.users,find_data,find_type)
            email = user["email"]
            for i in self.users:
                if self.users[i]["email"] != email:
                    if self.users[i]["userName"] == value:
                        print(f"{value} alredy exist...")
                        return None
        elif value_type == "email" :
            user,i = self.util.dic_search(self.users,find_data,find_type)
            userName = user["userName"]
            for i in self.users:
                if self.users[i]["userName"] != userName:
                    if self.users[i]["email"] == value:
                        print(f"{value} alredy exist...")
                        return None
        update = self.util.update_dic_by_value(self.users,find_data,find_type,value,value_type)
        print(update)
        if update == True:
            if value_type == "userName":
                user,i = self.util.dic_search(self.users,value,find_type)
                updateField = self.updateAuctionFieldByValue(find_data,"owner",user["userName"])
                print("update item ower field successful",updateField)
            else:
                user,i = self.util.dic_search(self.users,find_data,find_type)
            print(user,value_type)
            print(self.users)
            print(f"{i} value {user[value_type]} is updated!")
            self.users = self.dbModel.recod_reload_dic_data("users.txt",self.users)
            return True
        return None

    #------delete =>True:None------
    def deleteUser(self,userName):
        try:
            if self.util.dic_length(self.users)>0:
                user,i = self.util.dic_search(self.users,userName,"userName")
                
                if self.util.dic_length(self.auctionsItems)>0:
                    for i in self.auctionsItems:
                        if self.auctionsItems[i]["owner"] == userName:
                            self.deletAuction(self.auctionsItems[i]["title"])
                    print("Relation data in Auction Item also deleted!!")
                else:
                    print("no itme to delete")
                if user:
                    del self.users[i] 
                    temp ={}
                    id = 0
                    if self.util.dic_length(self.users)>0:
                        for i in self.users:
                            id = id +1
                            if self.users[i].values:
                                temp.update({id:self.users[i]})
                    self.users = temp
                    print(f"User data is deleted")

                    #reupdate the db
                    self.auctionsItems = self.dbModel.recod_reload_dic_data("items.txt",self.auctionsItems)
                    self.users = self.dbModel.recod_reload_dic_data("users.txt",self.users)  
                    return True
                return None 
        except Exception as err:
            return None    

    ####----------------------Aution items-------------------------########
    # item_categories = ["pot","coin","gold"]
    # bider = ["mgmg","KOKO","mimi"]
    # auctions = {1:"title":"chinese pot",
    #              "categories":"pot",
    #               "owner":"mgmg",
    #               "status":"active",
    #               "endTime":"12:00",
    #               "buyer":"mgmg",
    #               "prices":"8000"}
    #######------------------------itmes--------------------##########

    #------create => True:Nane------
    def creatAuction(self,title,catgories,owner,status,endTime,buyer,price):
        if self.util.dic_length(self.auctionsItems)>0:
            auction,i = self.util.dic_search(self.auctionsItems,title,"title")
            if auction:
                    print("items name alredy existed try other")
                    return None
        self.auctionsItems.update({self.util.dic_length(self.auctionsItems)+1:{"title":title,"category":catgories,"owner":owner,"status":status,"endTime":endTime,"buyer":buyer,"price":price}})
        self.dbModel.recod_reload_dic_data("items.txt",self.auctionsItems)
        print("Successful creating auction")
        self.auctionsItems = self.dbModel.recod_reload_dic_data("items.txt",self.auctionsItems )
        return True

    #------Search item => item:None------
    def searchAuction(self,value):
        try:
            if self.util.dic_length(self.auctionsItems) >0:
                auction,i = self.util.dic_search(self.auctionsItems,value,"title")
                item_list = self.util.search_dic_bykey_lists(self.auctionsItems,"title")
                if auction:
                    print(f" {auction['title']} -> {item_list}") 
                    return auction
        except Exception as err:
            print(f" {auction['title']} ->! {item_list}")
            return None

    #------Search item => item:None------
    def searchAuctionByReMainTime(self):
        tem = self.util.search_dic_limit_list("endTime",0)
        return tem
    
    #------Search list of object| => list_dic:None------
    def Auction_lists(self,cate):
        return self.util.search_dic_bykey_lists(self.auctionsItems,cate)

    #------update itmes=> True:None------
    def updatAuction(self,title,data,value_type):
        try:
            if self.util.dic_length(self.auctionsItems) > 0:
                auction,i = self.util.dic_search(self.auctionsItems,title,"title")
                if value_type == "title" and auction["title"] == data:
                        print("items name alredy existed try other")
                        return None
                updateData =  self.util.update_dic_by_value(self.auctionsItems,title,"title",data,value_type)
                self.auctionsItems = self.dbModel.recod_reload_dic_data("items.txt",self.auctionsItems)
        except Exception as err:    
            return updateData
    
    #------search items by field value  itmes:dic : None------
    def auctionItemByValue(self,key,value):
        if self.util.dic_length(self.auctionsItems) > 0:
            items = self.util.search_dic_byValue_lists(self.auctionsItems,key,value)
            return items
        return None
    
    #------update items by field same value True : None------
    def updateAuctionFieldByValue(self,fieldValue,key_type,updateValue):
        itemField = self.util.updateAllfieldByValue(self.auctionsItems,fieldValue,key_type,updateValue)
        self.auctionsItems =self.dbModel.recod_reload_dic_data("items.txt",self.auctionsItems)
        return itemField

    #------update status => True:None------
    def updateAuctionStatus(self,title,data,status):
        if status == "active":
            status = "activte"
        else:
            status= "inactive"
        self.auctionsItems = self.dbModel.recod_reload_dic_data("items.txt",self.auctionsItems)
        return self.updatAuction(title,data,status)

    #------delete =>True:None------
    def deletAuction(self,name):
        if self.util.dic_length(self.auctionsItems)>0:
            # item_list1 = self.util.search_dic_bykey_lists(self.auctionsItems,"title")
            item,i = self.util.dic_search(self.auctionsItems,name,"title")
            
            if item:  
                del self.auctionsItems[i] 
                temp ={}
                id = 0
                for i in self.auctionsItems:
                    id = id +1
                    if self.auctionsItems[i].values:
                        temp.update({id:self.auctionsItems[i]})
                self.auctionsItems = temp
                # item_list2 = self.util.search_dic_bykey_lists(self.auctionsItems,"title")
                # print(f" (Del) {item['title']} <-' Auction : {item_list2}")
                self.auctionsItems =self.dbModel.recod_reload_dic_data("items.txt",self.auctionsItems)
                return True
            # print(f" (!Del) {name} ->! Auction : {item_list1}")
            return None
        else:
            print(f"!No data {self.auctionsItems}")  
            return None 


        
    ########--------------Item client--------------############
    #------Add auction itme client =>True:None------
    def addItemClient(self,itemName,client):
        item,i = self.util.dic_search(self.auctionsItems,itemName,"title")
        if item:
            self.auctionsItems[i]["bider"].append(client)
            print(f" (Add) {client} '-> ({item['title']} :{item['bider']})")
            return True
        print(f" (!Add) {itemName} >! (self.auctionsItems)") 
        return None 
    
    #------Remove item client =>True:None------
    def deleteItemClient(self,itemName,client):
        item,i = self.util.dic_search(self.auctionsItems,itemName,"title")
        if item:
            if len(item["bider"]) > 0:  
                for i in item["bider"]:
                    item["bider"].remove(i)
                    print(f" (Del) {client} <-'({item['title']}:{item['bider']})")
                    return True
                
                print(f" (!Del) {client} ->! ({item['title']} :{item['bider']})")
                return None
        print(f" _ (!Del) {itemName} >! (self.auctionsItems)")   
        return None 


#Start program
if __name__ == "__main__":
    server = Server()
    server.main()