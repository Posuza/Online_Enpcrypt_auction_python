
class dic_util():
    def __init__(self):
        pass
#######-------------General fuctions------------###########

    #--dictory lenght=> 0|int
    def dic_length(self,dic: dict):
        try:
            key =list(dic)[-1]
            return key
        except Exception as err:
            # print(f"No data in dictionary")
            return 0
    
    #--dictory valiue=> data,id|None
    def dic_search(self,dic:dict,value,value_type:str): 
        if self.dic_length(dic) >0:
            for i in dic:
                if dic[i][value_type] == value:
                        return dic[i],int(i)
            print(f" !{value} in dictionary")
            return None,None
        print(f" !data in dictionary")
        return None,None
    
    #------Search by owner|categories|status user => list:None------
    def search_dic_bykey_lists(self,dic,categorie):
        temp = []
        if self.dic_length(dic) > 0:
            try:
                temp = [dic[d][categorie] for d in dic]
                # print(f"( ('{categorie}') ={temp} )")
                return temp    
            except Exception as e: 
                print(f" !invalid, [{e}]") 
            return None
        print(f"!No data dictionary")
        return None 
    
    #------Search by cate of dic => list_dic:None------
    def search_dic_limit_list(self,dic,value_type,value):
        
        temp = {}
        id = 0
        if self.dic_length(dic) > 0:
             
            for i in dic:
                    id = id +1
                    if value_type == "endTime":
                        if dic[i][value_type] > value: 
                            temp.update({id:dic[i]}) 
                    else:
                        if dic[i][value_type] == value:
                            temp.update({id:dic[i]})
        print(f"!No data dictionary")
        return temp
    
    #------Search list of dic value by key sim_name => list:None------
    def search_dic_byValue_lists(self,dic,field_type,sim_value):
        temp = {}
        id = 1
        if self.dic_length(dic) > 0:
            for i in dic:
                if dic[i][field_type] == sim_value:
                    temp.update({id:dic[i]})
                    id = id+1
            return temp
        return None 
    
    # #------Search by owner|categories|status user => user:None------
    # def search_lists(self,dic,categorie):
    #     temp = []
    #     if self.dic_length(dic) > 0:
    #         try:
    #             temp = [dic[d][categorie] for d in dic]
    #             print(f" ('{categorie}') = {temp} ")
    #             return temp
    #         except Exception as e:
    #             print(f" !invalid,[{e}]")
    #         return None 
    #     print(f"No data")
    #     return None 
    
    #------Update dic by name => Ture:None------
    def update_dic_by_value(self,dic,find_data,find_type,value,value_type):
        if self.dic_length(dic) >0:
            item,i = self.dic_search(dic,find_data,find_type)
            if item:  
                dic[i][value_type] = value       
                print(f" {find_data}['{value_type}'] > {dic[i][value_type]} ")
                return True
            print(f"!invalid field in {find_data}['{value_type}']")
            return None
        print("No data in dictionary")
        return None  
    
    #------Update all dic field by value => Ture:None------
    def updateAllfieldByValue(self,dic,fieldValue,key_type,updateValue):
            if self.dic_length(dic) > 0:
                for i in dic:
                        if dic[i][key_type] == fieldValue:
                                dic[i][key_type] = updateValue
                return True
            return None
     #--dictory valiue=> data,id|None
    def dic_search1(self,dic,value,value_type): 
        for i in dic:
            if dic[i][value_type] == value:
                    return dic[i],int(i)
        print(f" !{value} in dictionary")
        return None,None