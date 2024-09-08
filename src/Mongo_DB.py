
import pymongo 
from pymongo import MongoClient
from AllStrings import myStrings
import gridfs
import numpy as np
import cv2
import base64
import json
from pymongo import MongoClient, errors
import time
import common_fun as cf ## Ajay
import tkinter.messagebox as msg
##import sys
import objcrypt
import os

strObj  = myStrings()

class MyMongoDB:
    
    def __del__(self):
        print("Bye - MyMongoDB")
        self.myCompany_DBName.close()

    def __init__(self):
		# super(Root, self).__init__()
        print("Hi - MyMongoDB")

        self.bIsErrorInDB = False
        # create a timestamp before making API call
        start = time.time()
        try:
            self.MONGODB_HOST = 'localhost'
            self.MONGODB_PORT = 27017
            self.COMPANY_DB_NAME = strObj.strCompanyDBName
            # Establishing a Connection 
            self.myCompany_DBName = pymongo.MongoClient( self.MONGODB_HOST, self.MONGODB_PORT )
            # By specifying this database name and saving data to it
            self.mydbName = self.myCompany_DBName[self.COMPANY_DB_NAME]     

            # All Tables Names
            self.COLLECTION_TABLE_REGISTER_USER = 'Table_Register_User'
            self.COLLECTION_TABLE_STAFF_INFO = 'Table_Staff_Info'
            self.COLLECTION_TABLE_ATTENDANCE = 'Table_Attendance'

            self.myCompany_DBName.server_info() # will throw an exception
        except:
            print ("Mongo DB connection error")
            # print the time difference
            print (time.time() - start)
            self.bIsErrorInDB = True
            msg.showerror( strObj.strMsgTxt_Title, strObj.strMsg_Mongodb_not_run )
            ##sys.exit()
            ##root.quit()
            


    # Table = 1
    def Register_User(self, sUserName, sPW, sEmail):
        print(f"Register_User {sUserName} {sPW} {sEmail}")
        myTable = self.mydbName[self.COLLECTION_TABLE_REGISTER_USER]
        myTable.drop()
        # create dictionary first than save in db
        myDataToStore = { "user_name" : sUserName, "password" : sPW, "email" : sEmail }
        result = myTable.insert_one( myDataToStore ) # insert_many for list
        #print('One post: {0}'.format(result.inserted_ids))    
        # for x in myTable.find():
        #     print(x)

    # Table = 2
    def SaveStaffInfoInDB(self, sEmpFullDetails_Dictionary):
        print("Save employee data in DB")
        myTable = self.mydbName[self.COLLECTION_TABLE_STAFF_INFO ]
        # create dictionary first than save in db
        result = myTable.insert_one( sEmpFullDetails_Dictionary )  
        #print('One post: {0}'.format(result.inserted_ids))    
        # for x in myTable.find():
        #      print(x)

    # Table = 3
    def MarkedAttendanceInDB(self, EmpDetailsforAttendance, emp_Photo ):
        print("Mark employee Attendance in DB")
        myTable = self.mydbName[self.COLLECTION_TABLE_ATTENDANCE ]

        strImage = base64.b64encode(cv2.imencode('.png', emp_Photo)[1]).decode()
        # add image in dictionary before save in db
        EmpDetailsforAttendance["emp_image"] = strImage  

        result = myTable.insert_one( EmpDetailsforAttendance ) # insert_many
        
        # for x in myTable.find():
        #     print(x)

    def GetEmp_Photo_DateWise_During_Attendance_Mark( self, emp_id, emp_name, attendance_month, month_day ):
        myTable = self.mydbName[self.COLLECTION_TABLE_ATTENDANCE ]       
        #attendance_month = str(attendance_month) 
        #month_day = str(month_day)
        if( len(emp_id)  != 0 ):
            # get the Empl meta data
            ##emp_Details = myTable.find_one({'empid':  emp_id })
            emp_Details = myTable.find( { "$and" : [  { "empid" : emp_id }, { 'month' : attendance_month } , { 'month_date' : month_day }  ] } )
        elif( len(emp_name)  != 0 ):
            # get the Emp meta data
            ##emp_Details = myTable.find_one({'name':  emp_name })
            emp_Details = myTable.find( { "$and" : [  { "name" : emp_name }, { 'month' : attendance_month } , { 'month_date' : month_day } ] } )

        empPhoto = ""
        for tmp_data in emp_Details:
            #print(tmp)
            if "emp_image" in tmp_data:
                empPhoto = tmp_data['emp_image'] 
                break
        if( empPhoto != "" ):
            jpg_original = base64.b64decode(empPhoto)
            jpg_as_np = np.frombuffer(jpg_original, dtype=np.uint8)
            ###emp_img_photo = cv2.imdecode(jpg_as_np, flags=1)
            emp_img_photo = cv2.imdecode(jpg_as_np, cv2.IMREAD_COLOR)
            emp_img_photo = cv2.cvtColor(emp_img_photo , cv2.COLOR_BGR2RGB)  
            # to save Emp in folder
            ##cv2.imwrite('.//Emp_Tmp_Image//attendance.png', emp_img_photo)
            strPath = cf.Get_Emp_Tmp_Image_Dir() + "//attendance.png"  ## Ajay
            cv2.imwrite(strPath, emp_img_photo)



    def GetEmp_Photo_During_Attendance_Mark(self, emp_id, emp_name, attendance_month): 
        myTable = self.mydbName[self.COLLECTION_TABLE_ATTENDANCE ]        
        if( len(emp_id)  != 0 ):
            # get the Empl meta data
            ##emp_Details = myTable.find_one({'empid':  emp_id })
            emp_Details = myTable.find( { "$and" : [  { "empid" : emp_id }, { 'month' : attendance_month }  ] } )
        elif( len(emp_name)  != 0 ):
            # get the Emp meta data
            ##emp_Details = myTable.find_one({'name':  emp_name })
            emp_Details = myTable.find( { "$and" : [  { "name" : emp_name }, { 'month' : attendance_month }  ] } )

        empPhoto = ""
        for tmp_data in emp_Details:
            #print(tmp)
            if "emp_image" in tmp_data:
                empPhoto = tmp_data['emp_image'] 
                break
        if( empPhoto != "" ):
            jpg_original = base64.b64decode(empPhoto)
            jpg_as_np = np.frombuffer(jpg_original, dtype=np.uint8)
            ###emp_img_photo = cv2.imdecode(jpg_as_np, flags=1)
            emp_img_photo = cv2.imdecode(jpg_as_np, cv2.IMREAD_COLOR)
            emp_img_photo = cv2.cvtColor(emp_img_photo , cv2.COLOR_BGR2RGB)  
            # to save Emp in folder
            ##cv2.imwrite('.//Emp_Tmp_Image//attendance.png', emp_img_photo)
            strPath = cf.Get_Emp_Tmp_Image_Dir() + "//attendance.png"  ## Ajay
            cv2.imwrite(strPath, emp_img_photo)
 

    def IsAnyUserAlreadyRegister(self):
        # check DB = is any user entry if found than no need to add again new user
        print("check DB = is any user entry if found than no need to add again new user")
        myTable = self.mydbName[self.COLLECTION_TABLE_REGISTER_USER]
        ##myQueryResult = myTable.find()
        myQueryResult_Count = myTable.find().count()
        # for abc in myQueryResult:
        #     print(abc)
        if( myQueryResult_Count > 0 ):
            return True
        else:
            return False

    def GetUserName_PW(self):
        myTable = self.mydbName[self.COLLECTION_TABLE_REGISTER_USER]
        myQueryResult = myTable.find()        
        mydataLst = list()
        for abc in myQueryResult:
            print(abc)
            sUserName = abc["user_name"]
            mydataLst.append(sUserName)
            passWord = abc["password"]
            mydataLst.append(passWord)
            sEmail = abc["email"]
            mydataLst.append(sEmail)
        return mydataLst
  
    def UpdateUserPasswordInDB(self, oldpassword, newPassword ):
        myTable = self.mydbName[self.COLLECTION_TABLE_REGISTER_USER]
        # create dictionary first than save in db
        myOldValue = { "password":  oldpassword }
        myNewValues = { "$set": { "password":  newPassword } }
        myTable.update_one( myOldValue, myNewValues )  
        print("Done")
        #print "customers" after the update:
        # for x in myTable.find():
        #     print(x)

    def CheckEmpIDExistInDB(self, emp_id):
        myTable = self.mydbName[self.COLLECTION_TABLE_STAFF_INFO ] 
        folder_Name = ""
        if( len(emp_id)  != 0 ):
            str_emp_id =  myTable.find({},{ "empid": 1, "department": 1, "name" : 1  })  # Return only the empid as given 1
            for e_id in str_emp_id:
                db_emp_id = e_id["empid"]
                if(emp_id ==  db_emp_id  ):

                    ## folder_Name  = e_id['empid']  + "-" + e_id['name'] + "-" +  e_id['department'] 

                    ## folder name =>used in page_addrecord.py, mongo_db.py, takeempphotopage.py, page_facerecognition.py
                    if( e_id['name'].find(" ") > 0 ):
                        nameTmp = e_id['name'].replace(" ", "_")
                    else:
                        nameTmp = e_id['name'].strip()
                    if( e_id['department'].find(" ") > 0 ):
                        depTmp = e_id['department'].replace(" ", "_")
                    else:
                        depTmp = e_id['department'].strip()
                    folder_Name  = e_id['empid']  + "-" +  nameTmp + "-" +  depTmp  

                    break

            return folder_Name            
        
    def Search_EmpID_OR_EmpName_AlreadyExistsInDB(self, emp_id, emp_name):
        # before adding new record please cross-check emp_id is given to any-body?
        myTable = self.mydbName[self.COLLECTION_TABLE_STAFF_INFO ] 
        if( len(emp_id)  != 0 ):
            # 0 means skip, 1 means show
            str_emp_id =  myTable.find({},{ "empid": 1 })  # Return only the empid as given 1
            bIsEmpIDFound = False
            for e_id in str_emp_id:
                db_emp_id = e_id["empid"]
                if(emp_id ==  db_emp_id  ):
                    bIsEmpIDFound = True
                    break
            return bIsEmpIDFound
        elif( len(emp_name)  != 0 ):
            # 0 means skip, 1 means show
            str_emp_name =  myTable.find({},{ "name": 1 }) # Return only the name as given 1
            bIsEmpNameFound = False
            for e_name in str_emp_name:
                db_emp_name = e_name["name"]
                if(emp_name ==  db_emp_name  ):
                    bIsEmpNameFound = True
                    break
            return bIsEmpNameFound
        else:
            return False

    def Search_EmpID_OR_EmpName_ExistsIn_Attendance_Table(self, emp_id, emp_name):
        myTable = self.mydbName[self.COLLECTION_TABLE_ATTENDANCE ] 
        if( len(emp_id)  != 0 ):
            # 0 means skip, 1 means show
            str_emp_id =  myTable.find({},{ "empid": 1 }) # Return only the empid as given 1
            bIsEmpIDFound = False
            for e_id in str_emp_id:
                db_emp_id = e_id["empid"]
                if(emp_id ==  db_emp_id  ):
                    bIsEmpIDFound = True
                    break
            return bIsEmpIDFound
        elif( len(emp_name)  != 0 ):
            # 0 means skip, 1 means show
            str_emp_name =  myTable.find({},{ "name": 1 }) # Return only the name as given 1
            bIsEmpNameFound = False
            for e_name in str_emp_name:
                db_emp_name = e_name["name"]
                if(emp_name ==  db_emp_name  ):
                    bIsEmpNameFound = True
                    break
            return bIsEmpNameFound
        else:
            return False

    def Search_User_Month_Year_ExistsIn_Attendance_Table(self, emp_id, emp_name, month_value, year_Value ):
        myTable = self.mydbName[self.COLLECTION_TABLE_ATTENDANCE ] 
        if( len(emp_id)  != 0 ):
            #sForCaseInsensitivity = f"/{radio_Value}/i"
            myEmpData =  myTable.find( { "$and" : [  { "empid" : emp_id }, { "month" : month_value }, {"year" : year_Value}  ] } )
            # for item in myEmpData:
            #     print(item)
            return myEmpData
        elif( len(emp_name)  != 0 ):
            #sForCaseInsensitivity = f"/{radio_Value}/i"
            myEmpData =  myTable.find( { "$and" : [  { "name" : emp_name },  { "month" : month_value }, {"year" : year_Value}  ] } )
            # for item in myEmpData:
            #     print(item) 
            return myEmpData     
        
    def Get_User_Month_Year_Attendance_Table(self, empid_value, name_value, month_Value, year_Value):
        myTable = self.mydbName[self.COLLECTION_TABLE_ATTENDANCE ] 
        if( len(empid_value)  != 0 ):
            #sForCaseInsensitivity = f"/{radio_Value}/i"
            myEmpMonthAttendanceData =  myTable.find( {  "empid" : empid_value ,  "month" : month_Value , "year" : year_Value   }  )
            # for item in myEmpMonthAttendanceData:
            #     print(item)
            return myEmpMonthAttendanceData
        elif( len(name_value)  != 0 ):
            #sForCaseInsensitivity = f"/{radio_Value}/i"
            myEmpMonthAttendanceData =  myTable.find( {},  { "name" : name_value ,   "month" : month_Value , "year" : year_Value  } )
            # for item in myEmpMonthAttendanceData:
            #     print(item) 
            return myEmpMonthAttendanceData 

 

           
    def AddZeroInFrontOfIntValue(self, number,decimals) :
        ## Add Zero in int value
        ##--print AddZeroInFrontOfIntValue(1,6) #prints 000001
        return str(number).zfill(decimals)


    def GetNextEmpID(self):
        # before adding new record please cross-check emp_id is given to any-body?
        myTable = self.mydbName[self.COLLECTION_TABLE_STAFF_INFO ] 
        # 0 means skip, 1 means show
        ###db.collectionName.find({}).sort({$natural:-1}).limit(1)
        db_emp_id = 0
        new_emp_id =  myTable.find({}, { "empid" : -1} )  ##.sort({ "empid" : -1}).limit(1)    
        for e_id in new_emp_id:
            db_emp_id = e_id["empid"] 
        next_emp_id = int(db_emp_id) + 1
        if(next_emp_id < 10 ):
            next_emp_id = self.AddZeroInFrontOfIntValue(next_emp_id, 3)
        elif( next_emp_id >= 10 and next_emp_id < 100 ):
            next_emp_id = self.AddZeroInFrontOfIntValue(next_emp_id, 2)
        print(f"new emp id = {next_emp_id}")
        return next_emp_id



    def Check_EmpID_AlreadyExistsInDB(self, emp_id):
        # before adding new record please cross-check emp_id is given to any-body?
        myTable = self.mydbName[self.COLLECTION_TABLE_STAFF_INFO ] 
        # 0 means skip, 1 means show
        str_emp_id =  myTable.find({},{ "empid": 1 })
        bIsEmpIDFound = False
        for e_id in str_emp_id:
            db_emp_id = e_id["empid"]
            if(emp_id ==  db_emp_id  ):
                bIsEmpIDFound = True
                break
        return bIsEmpIDFound
     
    def Decrypt_Data(self, keyfilePath ):
        crypter = objcrypt.Crypter('key', 'cbc')
        ##Read file to decrypt
        read_file_data = dict()
        with open( keyfilePath ) as f_data:
            read_file_data = json.load( f_data )
        # decrypt now
        dec_dict = crypter.decrypt_object(read_file_data)
        print("Decrypt_Data done")
        return dec_dict 

    def Check_KeyFile_Before_AddNewData(self):
        ### check total number of employee as per key allotted
        strKeyDirPath = cf.GetKeyDirPath()
        keyfilePath =  strKeyDirPath + "key.key"
        if os.path.exists(keyfilePath):
            file_data = self.Decrypt_Data(keyfilePath) 
            my_dbkey = file_data['key']
            exp_date = file_data['key2']
            total_emp_no_as_per_key_allowed = int( file_data['key3'] )
             

            myTable = self.mydbName[self.COLLECTION_TABLE_STAFF_INFO ]            
            # check total number of live/ working employe in DB
            total_live_emp_no = 0 
            ##check in db==============add code live/ working count========================
            myEmpData =  myTable.find( { "$and" : [  { "emp_status" : 'working' }   ] } )
            for eid in myEmpData:
                value = eid['empid']
                if( value != ''):
                    total_live_emp_no += 1
            print(f" Total Working  Emp = {total_live_emp_no}")
            if(  total_live_emp_no >= total_emp_no_as_per_key_allowed ):
                return False
            else:
                return True


    ########### start new function to ##########
    # To encode for JSON:
    def Add_Emp_NewRecordInDb_With_Photo(self, empDetails, empPhoto):
        myTable = self.mydbName[self.COLLECTION_TABLE_STAFF_INFO ]    

        ####---check total number of employee as per key allotted------------------------------
        if(False == self.Check_KeyFile_Before_AddNewData() ):
            print("As per allotted key user can not allow to add more employee")
            return False
        ###----------------------------------

        strImage = base64.b64encode(cv2.imencode('.png', empPhoto)[1]).decode()
        # add image in dictionary before save in db
        empDetails["emp_image"] = strImage  
        result = myTable.insert_one( empDetails )
        # for x in myTable.find():
        #     print(x)
        return True


    #To decode back to np.array:
    def GetEmpDataFromDB(self, emp_name, emp_id):
        myTable = self.mydbName[self.COLLECTION_TABLE_STAFF_INFO ]        
        if( len(emp_name)  != 0 ):
            # get the Empl meta data
            emp_Details = myTable.find_one({'name':  emp_name }) # ['emp_image'][0]
        elif( len(emp_id)  != 0 ):
            # get the Emp meta data
            emp_Details = myTable.find_one({'empid':  emp_id }) # ['emp_image'][0]
        empPhoto = emp_Details['emp_image']
        jpg_original = base64.b64decode(empPhoto)
        jpg_as_np = np.frombuffer(jpg_original, dtype=np.uint8)
        ###emp_img_photo = cv2.imdecode(jpg_as_np, flags=1)
        emp_img_photo = cv2.imdecode(jpg_as_np, cv2.IMREAD_COLOR)
        emp_img_photo = cv2.cvtColor(emp_img_photo , cv2.COLOR_BGR2RGB)  
        # to save Emp in folder
        strPath = cf.Get_Emp_Tmp_Image_Dir() + "//0.png"  ## Ajay
        cv2.imwrite(strPath, emp_img_photo)
        return emp_Details
    ########### End new function to ##########

    def UpdateEmployeInfo(self, oldData, newData):
        print("Update employee information in DB")
        myTable = self.mydbName[self.COLLECTION_TABLE_STAFF_INFO ]        
        myTable.update_one( oldData, newData )  
        print("Done")

        
    def Get_AllEmpData_Month_Year_Attendance(self, month_Value, year_Value):
        myTable = self.mydbName[self.COLLECTION_TABLE_ATTENDANCE ] 
        # try to store all emp. data of this month and year
        # empid = from start to end
        AllEmpData = dict()
        tbleClmName = "empid"
        all_emp_id =  myTable.distinct( tbleClmName )
        for empid_value in all_emp_id:
            print (empid_value)            
            if( len(empid_value)  != 0 ):
                #sForCaseInsensitivity = f"/{radio_Value}/i"
                myAllEmpMonthAttendanceData =  myTable.find( {  "empid" : empid_value ,  "month" : month_Value , "year" : year_Value   }  )
                AllEmpData[empid_value] = myAllEmpMonthAttendanceData

                # print( type(myAllEmpMonthAttendanceData) )
                # for item in AllEmpData[empid_value]:
                #    print(item)

                # for emp_info in myAllEmpMonthAttendanceData:
                #     # AllEmpData[empid_value] = myAllEmpMonthAttendanceData
                #     print(emp_info['empid']  )  
                #     print(emp_info['name']  )  
                #     print(emp_info['department']  ) 
                #     print(emp_info['month']  )  
                #     print(emp_info['year']  )  
                #     print(emp_info['weekday_name']  )
                #     print(emp_info['complete_date'] )
                #     print(emp_info['time']  )  
                #     print(emp_info['emp_status'] )  
                #     print(emp_info['camera_id'] )  
                #     print(emp_info['month_date']  ) 
               

        # for eid in AllEmpData:    
        #     # pymongo.cursor.Cursor
        #     for item in AllEmpData[eid]:
        #         print(item)

        return AllEmpData



if __name__ == "__main__":
    obj = MyMongoDB()

    # obj.Get_AllEmpData_Month_Year_Attendance( 'September', '2020')

    ##obj.Search_User_Month_Year_ExistsIn_Attendance_Table("", "Rinku", "month", "may")
    
    ###obj.Check_EmpID_AlreadyExistsInDB("009")

    # sUserName, sPW, sEmail
    #obj.Register_User( "ajay", "pass_ajay", "op@op.com")
    #obj.IsAnyUserAlreadyRegister()
    #obj.GetUserName_PW()
    #obj.UpdateUserPasswordInDB("pass_ajay", "ved123")


    # To save info iin DB
    import cv2
    # 1. emp full data
    sEmpFullDetails_Dictionary = {
        "empid" : "008",
        "name" : "Tanishka",
        "department" : "class6",
        "address" : "20 vvp",
        "mobile" : "0000",
        "email" : "ttta@ttta.com",
        "designation" : "tttttt",
        "doj" : "26Oct09",
        "gender" : "Female",
        "dob": "2222aug"        
    }
    # 2. emp image
    sImg = "D:\\MyAllProjects\\FaceRecognition\\staffImages\\Class6-Tanishka-EmpID8\\6.jpg"
    # read the image and convert it to RGB
    emp_image = cv2.imread(sImg, 1)
    ##emp_image = cv2.cvtColor(emp_image, cv2.COLOR_BGR2RGB)
    emp_image = cv2.cvtColor(emp_image, cv2.COLOR_BGR2GRAY  )
     
    # 3. save in db
    obj.Add_Emp_NewRecordInDb_With_Photo(sEmpFullDetails_Dictionary, emp_image)
    ##obj.Update_Emp_ExistingRecordInDb(sEmpFullDetails_Dictionary)
    
    ##-------------------------------------------------------
    # to Get emp info from db
    # emp_name = "Tanishka"
    # emp_id = "008"
    # emp_data = obj.GetEmpDataFromDB(emp_name, emp_id)    
    # for x in emp_data:
    #     print(f"{x} = {emp_data[x]} " )      
    ##-------------------------------------------------------


'''
Very - very Imp in MongoDB Query during find()

{ "empid" :  "001", "month" : /june/i} // Note the 'i' flag for case-insensitivity  
{ "empid" :  "001", "month" : "june" } // Case-sensitive

db.articles.find( { $text: { $search: "coffee",$caseSensitive :true } } )  //FOR SENSITIVITY
db.articles.find( { $text: { $search: "coffee",$caseSensitive :false } } ) //FOR INSENSITIVITY

after insert
db.articles.createIndex( { subject: "text" } )
createIndex( { "empid": "text" } )

'''
 