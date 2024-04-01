import threading
import time
import socket
from datetime import datetime,timedelta
from client_util import utility
import s_encrypt_and_decrypt


class Auction_client():

    def __init__(self):
    #connnection
        self.target_ip = 'localhost'
        self.target_port = 9193
        self.client = None
        
    #Import variables
        self.decrypt = s_encrypt_and_decrypt.A3Decryption()
        self.encrypt = s_encrypt_and_decrypt.A3Encryption()
        self.util = utility()

    #admin variable
        self.users = {}
        self.adminItems = {}

    #variable
        self.auctionItems = {}
        self.user={}

    # threading
        self.bidItem = {}
        self.auctionValue = 0
        self.write = True
        self.receive = True

    #local function
        self.security_Key = None
        self.client = None        


    # Step(1)
    #secrete key
    def getting_key(self):
        security_Key =str( input("::Enter your encryption key To begin..\n -> Key: "))
        return security_Key
        
    #Step(2)
    #Revoke the client
    def client_runner(self):
        client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        client.connect((self.target_ip,self.target_port))
        return client

   #sendEncrp data to sever
    def send_encry_data(self,data):  
        encrypted_data = self.encrypt.start_encryption(data, self.security_Key)
        self.client.send(bytes(encrypted_data, "utf-8"))

    #receive data from sever
    def rev_decry_data(self):
        sms_encrypted = self.client.recv(4096).decode("utf-8")  
        # print("sms Encrypted Data : ", sms_encrypted)
        rec_descript_sms = self.decrypt.startDecryption(sms_encrypted)
        return eval(rec_descript_sms)
    
#-------------------------------Menu--------------------------

    #Step(3)   
    #Main Meum
    def main_Menu(self):
        if not self.security_Key:
            self.security_Key = self.getting_key()
            self.client = self.client_runner()
            message = self.client.recv(1024).decode("utf-8")
            print(f"\n >>> {eval(message)[ 'body']} <<<")
        mainOption_text= "\n::----------------- Main Options -------------::\n + 1:[login] \n + 2:[Register]\n + 0:[exit]"
        user_data = self.util.inputValidator(mainOption_text,"option","numbers",2)

        if user_data == 1:
            self.login()

        elif user_data == 2:
            self.register()     
        else:
            exit(1)
    
    #Userlogin
    def login(self):
                print("\n::--------------------- Login --------------------::")
                confirm = " + 1: continue\n + 0: go back"
                confirm = self.util.inputValidator(confirm,"continue","numbers",1)
                if confirm == 0:
                    self.main_Menu()
            
                login_Email =self.util.email_check("::::::\n  >: Enter Your Email > ")

                #Username Text validation
                login_Password = self.util.password_check("  >: Enter password  > ")

                #confirm to loign
                confirm = "\n::---------Opion--:\n + 1: confirmn\n + 0: cancel"
                confirm = self.util.inputValidator(confirm,"confirm","numbers",1)
                if confirm == 0:
                    self.main_Menu()
                send_sms = {"header":"+login",
                            "body":{"email":login_Email,"password":login_Password}}
                self.send_encry_data(f"{send_sms}")

                sms = self.rev_decry_data()

                print(f"\n{sms['body']['info']} \n")
                #from sever
                #sms = [header]= auth,[info] = "informaton", ["user"] = user.value
                if sms["body"]["user"]:
                    self.user = sms["body"]["user"]
                    self.user_authenticated_Menu()
                else:
                    self.login()

    #User Authenticated
    def user_authenticated_Menu(self):
        if self.user["role"] == "admin":
            auth_menu_tex=f"\n::---------------Oline_Auction-------------::\n:: welcome --> {self.user['userName']}\n::Option:\n + 1: Auction \n + 2: Profile \n + 3: users(CRUD) \n + 4: Items(CRUD)\n + 0: Logout"
            key = self.util.inputValidator(auth_menu_tex,"option","numbers",6)
        else:
            auth_menu_tex=f"\n::---------------Oline_Auction-------------::\n:: welcome --> {self.user['userName']}\n::Option:\n + 1: Auction \n + 2: Profile \n + 0: Logout"
            key = self.util.inputValidator(auth_menu_tex,"option","numbers",3)
        if key == 1:
            #auction
            self.auction_menu()
        elif key == 2:
            # Profile 
            self.profile()
        elif key == 3:
            # user(crud) 
            self.userManagement()
        elif key == 4:
            #itme(crud) 
            self.itemsManagement()
        else:
            self.user = None
            self.auctionItem = None
            self.friends = None
            client.close()
            exit(1)

    #itme management
    def itemsManagement(self):
        no = 1
        text = ""
        send_sms = {"header":"+req_items","body":{"info":"auction_items"}}
        self.send_encry_data(f"{send_sms}")
        # reeve item
        sms = self.rev_decry_data()
        print(sms["body"]["info"])
        # self,title,owner,status,endTime,buyer,price
        items ={}
        if sms["body"]["items"]:
            # self.adminItems = sms["body"]["items"]
            items = sms["body"]["items"]
            for i in items:
                    text = text +f"\n + {no}: {items[i]['title']} > ({items[i]['owner']}) | {items[i]['status'] } | {items[i]['buyer']} | {items[i]['price']} | {items[i]['endTime']}"
                    no = no +1
        itemsCRUD_text=f"::------------Items Management------------::\n::---NAME    OWNER   STATUS    BUYER   PRICE  ENDTIME---------::\n{text}\n + {no}: create new item \n + 0: <-back "
        select = self.util.inputValidator(itemsCRUD_text,"optoin","numbers",no)
        if 0< select < no:
            self.itemDetil(items[select],"admin")
        elif select == 0:  
            # go back  
            self.user_authenticated_Menu()
        else:
            self.creatNewAuctionItem("admin")

    #user Management
    def userManagement(self):
        no = 1
        text = ""
        send_sms = {"header":"+req_users","body":{"info":f"requesting user for crud"}}
        self.send_encry_data(f"{send_sms}")
        # reeve item
        sms = self.rev_decry_data()
        print(sms["body"]["info"])
        if sms["body"]["users"]:
            self.users = sms["body"]["users"]
            # userName,email,password,phone,bio,role,status,client
            for i in self.users:
                    user = self.users[i]
                    text = text +f"\n + {no}: {user['userName']} | {user['email']} | {user['phone'] }  | {user['role']} | {user['status']} "
                    no = no +1

        usersCRUD_text=f"::------------------User Management------------::\n   USERNAME:   EMAIL:   PHONE:   ROLE:   STATUS{text}\n + {no}: create new user \n + 0: <-back "
        select = self.util.inputValidator(usersCRUD_text,"optoin","numbers",no)
        if 0< select < no:
            self.update_information(self.users[select],"admin")
        elif select == 0:  
            # go back  
            self.user_authenticated_Menu()
        else:
            self.adminCreateUser()
        
    #Admin creat user
    def adminCreateUser(self):
        newUser = self.util.createUser()
        text = "::-------\n + 1: confirmn\n + 0: cancel"
        confirm = self.util.inputValidator(text,"confirm","numbers",1)
        if confirm == 0:
            self.userManagement() 

        send_sms = {"header":"+creatUser","body":{"user":newUser}}
        self.send_encry_data(f"{send_sms}")

        sms = self.rev_decry_data()
        print(sms)

        if sms["header"] == "#creatUser":

            self.userManagement()
        else:
            print(" ??? Failed to create user ..")
            text = "\n + 1: continue\n + 0: cancel"
            confirm = self.util.inputValidator(text,"option","numbers",1)
        if confirm == 1:
            self.adminCreateUser()
        else:
            self.userManagement() 


#---------------------------------Self-------------------------       
    # Profile
    def profile(self):
        print(f"\n::-----------------Profile---------------::\n  :Name     >>> {self.user['userName']}\n  :Email    >>> {self.user['email']}\n  :Phone    >>> {self.user['phone']}\n  :Password >>> {self.user['password']}\n  :Bio      >>> {self.user['bio']}")

        key = self.util.inputValidator(f"::::\n + 1:update account\n + 2:Delete account\n + 0:Go Back","option","numbers",2)
        if key == 1:
            #update account
            self.update_information(self.user,"")
        elif key == 2:
            self.delete_account(self.user,"")
        else:
            self.user_authenticated_Menu()

    # deleting account
    def delete_account(self,user1,admin):
        user = user1
        send_sms = {"header":"+deleUser","body":{"info":f"delete user account","userName":user["userName"]}}
        if user["userName"] == self.user["userName"]:
            key = self.util.inputValidator("\n::You deleted your account\n + 1:confirm \n + 0:Cancle >","confirm","numbers",1)
            if key == 0:
                self.update_information(user,admin)
            else:
                self.send_encry_data(f"{send_sms}")
        else:
            self.send_encry_data(f"{send_sms}")
        # reeve item
        sms = self.rev_decry_data()
        if sms["header"] == "#deleUser":
            if admin:
                if user["userName"] == self.user["userName"]:
                    print("???You deleted your account !!!")
                    self.user = None
                    self.auctionItem = None
                    self.friends = None
                    self.login()
                else:
                    print(f"{sms['body']['info']}")
                    self.userManagement()
            else:
                print(f"{sms['body']['info']}")
                self.user = None
                self.auctionItem = None
                self.friends = None
                self.login()
        else:
            print(f"{sms['body']['info']}")
            self.update_information(user1,admin)

    #update Profile
    def update_information(self,user,admin):
            # userName,email,password,phone,bio,role,status,client
            if admin:
                key = self.util.inputValidator(f"\n::-----------------update Profile=---------------::\n + 1:Name      >>> {user['userName']}\n + 2:Email     >>> {user['email']}\n + 3:Phone     >>> {user['phone']}\n + 4:Password  >>> {user['password']}\n + 5:Bio       >>> {user['bio']}\n + 6:Role      >>> {user['role']}\n + 7:Status    >>> {user['status']}\n + 8:Delete\n + 0:GoBack ","option","numbers",8)

            else:
                key = self.util.inputValidator(f"\n::-----------------update Profile=---------------::\n + 1:Name      >>> {user['userName']}\n + 2:Email     >>> {user['email']}\n + 3:Phone     >>> {user['phone']}\n + 4:Password  >>> {user['password']}\n + 5:Bio       >>> {user['bio']}\n + 0:GoBack","option","numbers",5)
            if key == 1:
                #newuserName
                newUserName= self.util.inputValidator("","new userName","","")
                self.update_inDB("userName",user["userName"],newUserName,admin)
            elif key == 2:
                #emai
                newEmail= self.util.email_check("Enter new email. > ")
                self.update_inDB("email",user["userName"],newEmail,admin)
            elif key == 3:
                #phone
                newPhone= self.util.phoneVali("Enter your new phone >",999999999)
                self.update_inDB("phone",user["userName"],newPhone,admin)
            elif key == 4:
                #pass
                newPassword= self.util.password_check("Enter your new password >")
                self.update_inDB("password",user["userName"],newPassword,admin)
            elif key == 5:
                #bio
                newBio= self.util.inputValidator("","new bio","","")
                self.update_inDB("bio",user["userName"],newBio,admin)
            elif key == 6:
                    #role
                    role= self.util.roleChek()
                    self.update_inDB("role",user["userName"],role,admin)
            elif key == 7:
                #status
                status= self.util.userStatus()
                self.update_inDB("status",user["userName"],status,admin)
            elif key == 8:
                print(user["userName"])
                self.delete_account(user,admin)
            else:
                if admin:
                   self.userManagement() 
                #userProfile or admin for user
                self.profile()

    #userNameChekcer in Db 
    def update_inDB(self,data_type,username,data,admin):
        send_sms = {"header":"+upDateUserInfo","body":{"info":f"update user {data_type}..","request":f"+update{data_type}","upValue":data,"userName":username}}
        # print("here",send_sms)
        self.send_encry_data(f"{send_sms}")
        # reeve item
        sms = self.rev_decry_data()
        if sms["header"] == f"#upDateUserInfo":
            print(sms["body"]["info"])
            if not admin:
                self.user = sms["body"]["user"]
                
        else:
            print(f"{sms['body']['info']}")
        self.update_information(sms["body"]["user"],admin)

    #user register
    def register(self):
            user= self.util.user_register()
            #confirm to register
            confirm = "\n::--------Opion--:\n + 1: confirmn\n + 0: cancel"
            confirm = self.util.inputValidator(confirm,"confirm","numbers",1)
            if confirm == 0:
                self.main_Menu() 
            
            send_sms = {"header":"+creatUser","body":{"user":user}}
            self.send_encry_data(f"{send_sms}")
            sms = self.rev_decry_data()

            if sms["header"] == "#creatUser":
                print(sms["body"]["info"])
                self.login()
            else:
                print(sms["body"]["info"])
                confirm = "\n::---------Opion--:\n + 1: continue\n + 0: MainMenu"
                confirm = self.util.inputValidator(confirm,"confirm","numbers",1)
                if confirm == 0:
                    self.main_Menu()
                return self.register()
        

#--------------------------------itme==------------------------------
   #auction menue
    def auction_menu(self):
        no = 1
        text = ""
        # "request aution"
        send_sms = {"header":"+activeItem","body":{"info":"auction_items"}}
        self.send_encry_data(f"{send_sms}")
        # reeve item
        sms = self.rev_decry_data()
        print(f"\n{sms['body']['info']} \n")

        if sms["body"]["items_list"]:
            self.auctionItems = sms["body"]["items_list"]           
            for i in self.auctionItems:
                    d1= datetime.strptime(self.auctionItems[i]["endTime"],'%Y-%m-%d (%H:%M:%S)')
                    d2 = d1- datetime.now()
                    f = str(d2).split('.')[0]
                    if f[0][0] != "-":
                        if self.auctionItems[i]["owner"] == self.user["userName"]:
                            text = text +f"\n + {no}: {self.auctionItems[i]['title']} (own) _ {self.auctionItems[i]['price'] } _ {self.auctionItems[i]['buyer']} | {self.auctionItems[i]['endTime']}"
                        else:
                            text = text +f"\n + {no}: {self.auctionItems[i]['title']} _ {self.auctionItems[i]['price'] } _ {self.auctionItems[i]['buyer']} | {self.auctionItems[i]['endTime']}"
                        no = no +1
    
        aution_text=f"::------------Avaliable_Auctions_items------------::\n::Option:{text}\n + {no}: your items \n + 0: <-back "
  
        select = self.util.inputValidator(aution_text,"option","numbers",no)

        if 0< select < no:
            item = self.auctionItems[select]
            self.bidItem = item
#>>>> threading passess
            self.write = True
            self.receive = True
            recv_sms_thread = threading.Thread(target=self.receive_message1)
            write_sms_thread = threading.Thread(target=self.write_message1)   
            recv_sms_thread.start()
            write_sms_thread.start()
        elif select == 0:  
            # go back  
            self.user_authenticated_Menu()
        else:
            self.yourAuctionItem()

    #your items  auction item
    def yourAuctionItem(self):
        no = 1
        text = ""
        items = []
    
        # request own 
        send_sms = {"header":"+ownItems","body":{"owner":self.user["userName"],"info":f"request own auctio item "}}

        self.send_encry_data(f"{send_sms}")
        # reeve item
        sms = self.rev_decry_data()
        print(f"\n{sms['body']['info']} \n")

        if sms["header"] == "#ownItems":
            items = sms["body"]["list_items"]
            
            for i in items:
                    text = text +f"\n + {no}: {items[i]['title']} _ {items[i]['status']} _ {items[i]['price'] } _ {items[i]['buyer']} | {items[i]['endTime']}"
                    no = no +1
        own_auction_text=f"::-----------------Your_Auctions_itmes------------------::\n::Option:{text}\n------------\n + {no}: create new items \n + 0: <-back "
        
        select = self.util.inputValidator(own_auction_text,"optoin","numbers",no)
        
        if 0< select < no:
            self.itemDetil(items[select],"")
        elif select == 0:  
            # go back  
            self.auction_menu()
        else:
            self.creatNewAuctionItem("")

    #Itme deatil update or deletion  both (user) and (admin)
    def itemDetil(self,item1,admin):
        item = item1
        send_header = "+upDateItem"
        request = ""
        select = None
        update_value = ""
        if admin: 
            # ,title,catgories,owner,status,endTime,buyer,price
            itemDatial_text=f"::------------Detail of ( {item['title']} )------------::\n::Update:\n  + 1: Title = {item['title']}\n  + 2: Status = {item['status']}\n  + 3: EndTime = {item['endTime']}\n  + 4: Bider = {item['buyer']}\n  + 5: Value = {item['price']}\n  + 6: Owner = {item['owner']}\n  + 7: delete \n  + 0: <- Go Back "
            select = self.util.inputValidator(itemDatial_text,"optoin","numbers",7)
        else:
            # title,catgories,owner,status,endTime,
            itemDatial_text=f"::------------Detail of ( {item['title']} )------------::\n::Update:\n  + 1: Title = {item['title']}\n  + 2: Status = {item['status']}\n  + 3: EndTime = {item['endTime']}\n  + 4: delete \n  + 0: <-back "
            select = self.util.inputValidator(itemDatial_text,"optoin","numbers",4)

        if select == 0:
             # go back
            if admin :
                self.itemsManagement()
            self.yourAuctionItem()

        elif select == 1:
            #update title
            update_value = self.util.inputValidator("","newTile","","")
            request = "+updateTitle"     
            info = "update title"

        elif select == 2 :
            #update status
            update_value = self.util.statusChek()
            request = "+updateStatus"
            info = "update status"

        elif select == 3:
            #update time
            moreTime = self.util.dateTimeValidator("Add more time")
            # change to time object 
            d1= datetime.strptime(item["endTime"],'%Y-%m-%d (%H:%M:%S)')

            d2 = d1- datetime.now()
            f = str(d2).split('.')[0]
            if f[0][0] == "-":
                time_object = datetime.now()+timedelta(minutes=moreTime)
            else:
                time_object = d1+timedelta(minutes=moreTime)
            strtime2 = f"{time_object:%Y-%m-%d (%H:%M:%S)}"
            update_value = strtime2

            request = "+updateTime"
            info = "add more time "
            
        elif select == 4 :
            #update Buyer
            if admin:           
                update_value = self.util.inputValidator("","new Bider","","")
                request = "+updateBider"     
                info = "update bider"
            else:
                print("deele")
                send_header = "+deleItem"
                info = "delete"

        elif select == 5 :
            #update Price
            if admin:            
                update_value = self.util.inputValidator("","new Price","numbers","")
                request = "+updatPrice"     
                info = "update Price" 

        elif select == 6 :
            #update owner
            if admin:            
                update_value = self.util.inputValidator("","new Øwnwer","","")
                request = "+updateOwner"     
                info = "update Owner"
        else:
            send_header = "+deleItem"
            info = "delete"
        
        #if value == oldvalue
        # field_type = ("title,owner,status,endTime,buyer,price").split(",")
        # for i in field_type:
        #     if update_value == item[i]:
        #         print(f"{i} is same as earlier")
        #         self.itemDetil(item,admin)
        # request own 
        if send_header == "+deleItem":
            print("here dekete")
   
            send_sms ={"header":send_header,"body":{"itemName":f"{item['title']}","info":f"request to {info} item "}}
        else:
            send_sms = {"header":send_header,"body":{"itemName":f"{item['title']}","upValue":f"{update_value}","request":request, "info":f"request to {info} item "}}
        print(send_sms)

        self.send_encry_data(f"{send_sms}")
        # reeve item
        sms = self.rev_decry_data()

        print(sms["header"],sms["body"]["info"])

        if sms["header"] == "#deleItem":
            if admin:
                self.itemsManagement()
            else:
                self.yourAuctionItem()                 
        self.itemDetil(sms["body"]["newItem"],admin)
        
    #creart new auction item both (user) and (admin)
    def creatNewAuctionItem(self,admin):
        print("::------------craeate your auctin item---------------::")
        self.bidItem = self.util.inputValidator("","Item name","","")
        addMin = self.util.dateTimeValidator("EndTime")
        time_object = datetime.now()+timedelta(minutes=addMin)
        strTime = f"{time_object:%Y-%m-%d (%H:%M:%S)}"
        send_sms = {"header":"+createNewItem","body":{"title":self.bidItem,"owner":self.user["userName"],"endTime":strTime}}

        self.send_encry_data(f"{send_sms}")
        # reeve item
        sms = self.rev_decry_data()
        print(sms["body"]["info"])
    
        if sms["header"]=="#createself.bidItem":
            if admin:
                self.itemsManagement()
            else:
                self.yourAuctionItem()
        else:
            confirm = "\n::------Continue create item--:\n + 1: continue\n + 0: go back"
            confirm = self.util.inputValidator(confirm,"confirm","numbers",1)
            if confirm == 0:
                self.yourAuctionItem()
            else:
                self.creatNewAuctionItem(admin)


    def receive_message1(self):
        while self.receive:
                
                send_sms = {"header":"+bidingItem","body":{"auctItem":self.bidItem["title"],"info":"reqest to auction"}}

                self.send_encry_data(f"{send_sms}")   
                sms = self.rev_decry_data()
                header = sms["header"]
                body = sms["body"]                    
                if header == "#bidingItem":
                    if body["bidingItem"] != None:
                        self.bidItem = sms["body"]["bidingItem"]
                        d1= datetime.strptime(self.bidItem["endTime"],'%Y-%m-%d (%H:%M:%S)')
                        d2 = d1- datetime.now()
                        f = str(d2).split('.')[0]
                        if f[0] != "-":
                            print(f".: {self.bidItem['title']} -> Bider:({self.bidItem['buyer']})-${self.bidItem['price']} | Remaining:{f[0:]}")
                    else:
                        self.write = False
                        self.receive = False 
                        return self.auction_menu()
                header = None                 
                body =None
                time.sleep(4)

    # Main Send message to sever Thread 
    def write_message1(self):
        while self.write:
            item = self.bidItem
            key =input("")
            try:
                money =int(input(f"::Option:\n + 0: go back \n + $:{self.auctionValue} > +:"))
                if money == 0:
                    self.write = False
                    self.receive = False 
                    return self.auction_menu()
                elif money > int(self.auctionValue):
                    sms = {"header":"+itemBidValue","body":{"title":f"{item['title']}","bider":f"{self.user['userName']}","price":f"{money}","info":"this is autioning"}}
                    self.send_encry_data(f"{sms}")
                else:
                     print(f"value must be > {self.auctionValue}")
            except Exception as err:
                print(err)
                print("value must be number")
                
            

if __name__ == "__main__":
    client =  Auction_client()
    client.main_Menu()
    