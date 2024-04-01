
class utility():
    def __init__(self) -> None:
        pass
    #update user information
    #delet account
    def account_delete(self,user_info):
            print(user_info["email"]," try to delete")
            while True:
                confirm = input("Type \'yes\' to confirm or \'no\' to cancel: >")
                if confirm == "no":
                    print("@You have cancel the confirmation..")
                    self.user_authenticated(user_info)
                    break

                elif confirm == "yes":
                    data_form = "delete_user" + " " + user_info["email"]
                    sms = self.sending_encrypted(data_form) 
                    print(sms)
                    self.client_menu()

    #UserRegisteration
    def register(self):
        print("\n  @registration Form... ")
        r_email = ''
        while True:
            r_email = input("Enter \'email\' for registration: or \nEnter \'login\' to go back: >")
            if r_email=="login":
                self.login("login")
            flag = self.email_validation(r_email)  # 1 or -1

            if flag == 1:
                break
            else:
                print("Email Form Invalid\nTry Again! ")

        print("Email From Valid ")
        self.user_register(r_email)

    #Register voter
    def user_register1(self, r_email):
        print("\n::--------------------- Register --------------------::")
        if self.email_checking_inDB(r_email) == 1:
            try:
                username = self.username_check("Enter your username:")

                pass1 = self.password_check("Enter your password to register:")
                pass2 = input("Enter your password Again  to register:")

                if pass1 == pass2:
                
                    print("Password Was match!")
                    phone =self.phoneVali("Enter Your phone no or \'skip\' to skip :> ",99999999)

                    data_list = [username,r_email, pass1, phone]
                    print(data_list)
                    self.final_registration(data_list)

                else:
                    print("Password not match:")
                    self.user_register(r_email)


            except Exception as err:
                print(err)

        else:

            print("Your email was already register!")
            self.register()


    ##-----------Register admin
    def admin_register(self):
            print("\n::--------------------- Register --------------------::")
            username =self.inputValidator("","userName","String","")
            
            email = self.email_check(" -> : Enter your email >")

            phone =self.phoneVali("Enter Your phone no or \'skip\' to skip :> ",99999999)

            pass1 = self.password_check(" -> : Enter your password >")

            pass2 = self.inputValidator("","password Again","String","")

            if pass1 == pass2:
            
                # print("Password Was match!")
                user ={"userName":username,"email":email,"password":pass1,"phone":phone,
                       "role":"admin"}
                return user                            
            else:
                print("????Password not match.....")
                return self.user_register()
            
    ##-----------Register voter
    def createUser(self):
            print("\n::---------------------Create New user --------------------::")
            username =self.inputValidator("","Name","String","")
            
            email = self.email_check(" -> : Enter user email >")

            pass1 = self.password_check(" -> : Enter your password >")
            phone =self.phoneVali("Enter user phone no or \'skip\' to skip :> ",99999999)
            
            role = self.roleChek()
            
                # print("Password Was match!")
            user ={"userName":username,"email":email,"password":pass1,"phone":phone,"role":role}
            return user                            


    ##-----------Register voter
    def user_register(self):
            print("\n::--------------------- Register --------------------::")
            username =self.inputValidator("","userName","String","")
            
            email = self.email_check(" -> : Enter your email >")

            phone =self.phoneVali(" -> : Enter Your phone no or \'skip\' to skip :> ",99999999)
            
            pass1 = self.password_check(" -> : Enter your password >")
            pass2 = self.inputValidator("","password Again","String","")

            if pass1 == pass2:
            
                # print("Password Was match!")
                user ={"userName":username,"email":email,"password":pass1,"phone":phone,"role":"user"}
                return user                            
            else:
                print("????Password not match.....")
                return self.user_register()
            
            
   
    #--------phone numbe validation
    def phoneVali(self,text,old_phone):
            
            digits = "0123456789"
            found = 0
            phone = input(""+ text)
            if phone == "skip":
                return old_phone
            if phone != '':
                lenght = len(phone)
                for b in phone:
                    for digit in digits:
                        if digit == b:   
                            found += 1 
                if lenght == found and lenght >= 8 and lenght <= 15:
                    return int(phone)
                else:
                    print("phone must contain only number and \n should not be under 8 or more than 15")
                    return self.phoneVali(text,old_phone)
            else:
                return int(old_phone)   


    #------Pssword checking
    def password_check(self,text):
        while True:
            password =input(f"{text}")
            result =self.password_valid(password)
            if password == result:
                # print(password)
                return password

    #P------ssword vlid
    def password_valid(self,password):
        if len(password) < 8:
            print("@Password must be more than 8 and contain different character types..")
            return -1
        check = {"number" : 0,
                "uppercase" : 0,
                "lowercase" : 0,
                "special_character" : 0}
        count = 0
        found = 0
    #  special_character = ["!","#","$","%","&","*",".", ",","/",":",";","?","@","\","_","|","~"]
        special_characters = [33,35,36,37,38,42,44,46,47,58.59,63,64,92,95,124,126]
        for i in range(len(password)):
                aChar = password[i]
                if  (ord(aChar) >47 and ord(aChar) < 58): #1241235
                    check["number"]= 1

                elif (ord(aChar) >64 and ord(aChar) < 91): #ASFGDNJ
                    check["uppercase"]= 1

                elif (ord(aChar) >95 and ord(aChar) < 123): #asfshcb   
                    check["lowercase"]= 1

                else:
                    found = found+1
                    for j in special_characters:
                        if ord(aChar) == j:
                            count = count+1
                            break
        # print(count,"count")
        # print(found,"found")
        if count != 0 and count == found :
            check["special_character"] = 1
        else:
            print("disallow special_character")

        counter = 3
        for i in check:
            if check[i] == 0:
                print("password must contain a",i)
                counter = -1

        if counter == 3:
            return password
        else:
            return -1


    #-----email checking
    def email_check(self,text):
        while True:
            email =input(f"{text}")
            result =self.email_validation(email)
            # print(email, result)
            if email == result:
                # print("valid email format")
                # print(email)
                return email

    #------email check
    def email_validation(self, r_email):
        name_counter = 0
        for i in range(len(r_email)):
            if r_email[i] == '@':
                # print("Name End Here")
                break
            name_counter += 1

        # print("Name counter: ", name_counter)

        email_name = r_email[0:name_counter]
        email_form = r_email[name_counter:]

        # print(email_name)
        # print(email_form)

        # checking for name
        name_flag = 0
        email_flag = 0
        for i in range(len(email_name)):
            aChar = email_name[i]
            if (ord(aChar) > 31 and ord(aChar) < 48) or (ord(aChar) > 57 and ord(aChar) < 65) or (
                    ord(aChar) > 90 and ord(aChar) < 97) or (ord(aChar) > 122 and ord(aChar) < 128):
                name_flag = -1
                break

        domain_form = ["@facebook.com", "@ncc.com", "@mail.ru", "@yahoo.com", "@outlook.com", "@apple.com", "@zoho.com",
                       "@gmail.com"]

        for i in range(len(domain_form)):

            if domain_form[i] == email_form:
                email_flag = 1
                break

        if name_flag == -1 or email_flag == 0:
            print("invalid email format")
            return -1

        else:
            return r_email


    #InputField validator both text and number
    #This will return Interger validare is : numbers/ return String if :other/ #range can be from 0 to "range " /or "" for returning String
    #-------------
    def inputValidator(self,promp_text,keyword,validate,range):
        try:
            if validate == "numbers":
                i = int(input(f"{promp_text}\n -> : Enter {keyword} > "))
            else:
                i = input(f"{promp_text}\n -> : Enter {keyword} > ")
            if range:
                if i !="":
                        if -1<i<=range:
                            return i
                        print(f"\n???invalid {keyword} .. !")

                else:
                        print(f"\n???{keyword} should'nt be null !")
                        
                return self.inputValidator(promp_text,keyword,validate,range)
            else:
                if i !="":
                        return i
                else:
                        print(f"\n???{keyword} should'nt be null !")
                return self.inputValidator(promp_text,keyword,validate,range)
        except Exception as err:
            print(f"\n???{keyword} should be numbers ..")
            return self.inputValidator(promp_text,keyword,validate,range)

    #------limit Selector will limit nubmer of try
    def limit_selector(self,list_data,text,count):
        value =None
        try:
            count = count -1
            text_input =int(input(f"0: to canceel\n::Choose {text} _> "))
            if -1 < text_input-1 < len(list_data):
                value = list_data[text_input-1]
                print(f"::({value}) is selectd\n <-'")
                return value
            elif text_input == 0:
                print(f"cancle a {text} chose") 
                return value
            else:
                if count<0:
                    print("invalid try later")
                    return value
                print(f"invalid {text} {count} Try left")  
            self.limit_selector(list_data,text,count)
        except Exception as err:
            if count<0:
                print("invalid try later")
                return value
            print(f"invlid number {count} try ",err)
            return self.limit_selector(list_data,text,count)

    #--------dateTime validation
    def dateTimeValidator(self,keyword):
        time = 0
        try:
            key = input(f"Enter {keyword} :\n eg: 1d or 1h or 1m\n eg: 1d:2h:3m(no second)> ")
            sep = key.split(":")

            if len(sep) > 1:
                for i in sep:
                    if i[-1] == "d":
                        time = time+int(i[:-1])*1440
                    elif i[-1] == "h":
                        time = time+int(i[:-1])*60
                    elif key[-1] == "m":
                        time = time+int(i[:-1])
                    else:
                        time = time + int(key)
            else:
                if key[-1] == "d" :
                        time = time+int(key[:-1])*1440
                elif key[-1] == "h" :
                    time = time+int(key[:-1])*60
                elif key[-1] == "m":
                    time = time+int(key[:-1])
                else:
                    time = time + int(key)
            return time
        except Exception as err:
            print(err,f"\n???{keyword} should be numbers ..")
            return self.dateTimeValidator(keyword)
    
    #-------- status check
    def statusChek(self):
            key = self.inputValidator("::Status Option:\n + 1:Active\n + 2:Inactivae ","status","numbers",2)
            if key == 1 :
                return "active"
            else:
                return "Inacitve"
            
    #-------- role check
    def roleChek(self):
            key = self.inputValidator("::Role Option:\n + 1:User\n + 2:Admin ","status","numbers",2)
            if key == 1 :
                return "user"
            else:
                return "admin"
                
        #-------- status check
    def userStatus(self):
            key = self.inputValidator("::Status Option:\n + 1:login\n + 2:logOut ","status","numbers",2)
            if key == 1 :
                return "login"
            else:
                return "logOut"
            



#---------------------Inrelated def-----------------
    #checking Email in DB 
    def email_checking_inDB(self, email):
        data = "email" + " " + email
        sms = self.sending_encrypted(data)
        print(sms)

        if sms == "notExist":
            return 1
        else:
            return -1  


    #Username checking from
    def username_check_Db(self,text):
        while True:
            userName =input(text)
            if userName !="":
                result =self.userName_checking_inDB(userName) #return 1 & -1
                if result == userName :
                    return userName
                else:
                    print("This username was alredy existed pls try another")
            else:
                print("Username must not be empty!")   

    #checking username in DB 
    def userName_checking_inDB(self, userName):
        data = "name" + " " + userName
        sms = self.sending_encrypted(data)
        print(sms)

        if sms == "notExist":
            return userName
        else:
            return -1      

    #Registeration confirmation
    def final_registration(self, data_list):
        while True:
            confirm = input("Type \'yes\' to confirm or \'no\' to cancel: >")
            if confirm == "no":
                print("@You have cancel the confirmation..")
                self.register()
                break
            elif confirm == "yes":
                data_form = "candidate_register" + " " + data_list[0] + " " + data_list[1] + " " + data_list[2] + " " + str(data_list[3]) + " " + "Update_your_user_info" + " " + "0"
                print(data_form)

                sms = self.sending_encrypted(data_form) 

                if sms:
                    print("Registration Success!",sms)
                    info="login"
                    self.login(info)
                    break
            else:
                print("@Invalid input for the confirmation..")

