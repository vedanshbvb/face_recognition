#from tkinter import Tk, Label, Button

from tkinter import *
from AllStrings import myStrings
import common_fun as cf 
import tkinter.messagebox as msg
import time
import tkinter.font as font
import tkinter as tk
import cv2
import os
import numpy as np
import math
from PIL import Image, ImageDraw 
import threading
from PIL import Image
from PIL import ImageTk
import datetime
from os.path import exists
import shutil
from Mongo_DB import MyMongoDB
from datetime import *


 
myAppBGColor =  "lavender blush" #  "grey" 
myFont = "Helvetica"
myHeadingTxtFontSize = 15
myTxtFontSize = 10
myTxtColor = "black" #  "white"
myBtnBGColor= "lavender blush" # "Green"
myBorderColor = "medium violet red"
myBtnTxtColor = "white"


strObj  = myStrings()
imgPath = cf.GetAppImageDirPath() 

class MyEditRecordPage(tk.Frame):
    def __del__(self):
        print("Bye MyEditRecordPage-3")

    def __init__(self, tkFrame, Parent=None):
        print("Hi MyEditRecordPage-3")

        #self._frame = None
        tk.Frame.__init__(self, tkFrame, Parent)

        self.myParent = Parent

        #self._frame = tkFrame
        self.myroot = tkFrame

        # define font - weight − "bold" for boldface, "normal" for regular weight
        #self.myFont = font.Font(family='Helvetica', size=13, weight='normal')

        self.frame = tk.Frame(tkFrame, width=385, height=460, borderwidth=0, bg= myAppBGColor , relief=SUNKEN   )
        #self.frame.pack(side = LEFT, anchor = "nw", fill=Y, expand=YES)
        self.frame.place(x=200-4, y=1, anchor="nw", width=758+6, height=621-1)

        #self.myframe2 = self.frame
        self.panel = None

        self.CreateEditRecPageGUI()

        
    def CreateEditRecPageGUI(self):
        self.myroot.grid_columnconfigure((0,1), weight=1)

        # create a Form Heading label 
        xLblVal = 80
        yVal = 32
        ctrlHeight = 3
        ctrlWidth = 80

        # Heading...
        self.heading = Label(self.frame, text=strObj.strHeadingEditRecord , fg=myTxtColor, bg=myAppBGColor, font=(myFont, myHeadingTxtFontSize), compound="left" , justify=LEFT, anchor=W )
        self.heading.configure(height=ctrlHeight, width=ctrlWidth)
        self.heading.place(x=xLblVal,y=32)  #.pack(expand=YES, fill=BOTH)     


        yVal += 85 
        xEdtVal = 230
        ctrlHeight = 1 
        ctrlWidth = 20

        global radioValueEdit_RFD
        radioValueEdit_RFD = IntVar()
        # 1. Radio - emp_id
        self.emp_id = Radiobutton(self.frame, text=strObj.strEmpID,  bg=myAppBGColor, font=(myFont, myTxtFontSize), compound="left", variable=radioValueEdit_RFD, value=1, command=self.onClickRadioBtnEdit_RFD, activeforeground= myTxtColor, activebackground = myAppBGColor)
        self.emp_id.configure(height=ctrlHeight, width=ctrlWidth, selectcolor = "light pink" )
        self.emp_id.place(x=xLblVal,y=yVal) 
        self.emp_id.select()

        self.entry_text_empid  = StringVar()
        self.empid_field = Entry(self.frame, width=ctrlWidth+20, textvariable=self.entry_text_empid , highlightbackground=myBorderColor, highlightcolor=myBorderColor, highlightthickness=1 , bd= 0  )
        self.empid_field.place(x=xEdtVal, y=yVal) 
        self.empid_field.focus() 
        #self.empid_field.bind("<Return>", self.empid_focus)
        yVal += 35

        # 2. Radio - emp_name
        self.emp_name = Radiobutton(self.frame, text=strObj.strEmpName,  bg=myAppBGColor, font=(myFont, myTxtFontSize), compound="left", variable=radioValueEdit_RFD, value=2, command=self.onClickRadioBtnEdit_RFD, activeforeground= myTxtColor, activebackground = myAppBGColor)
        self.emp_name.configure(height=ctrlHeight, width=ctrlWidth, selectcolor = "light pink" )
        self.emp_name.place(x=xLblVal-8,y=yVal) 

        self.entry_text_name  = StringVar()
        self.name_field = Entry(self.frame, width=ctrlWidth+20, textvariable=self.entry_text_name , highlightbackground=myBorderColor, highlightcolor=myBorderColor, highlightthickness=1 , bd= 0  )
        self.name_field.place(x=xEdtVal, y=yVal)
        #self.name_field.bind("<Return>", self.name_focus) 
        self.name_field['state'] = 'disable'       
        yVal += 35

        # rounded_btn_dark.png        
        btnImg_N0 = imgPath + "rounded_btn.png"
        self.img_N0=PhotoImage(file=btnImg_N0 ) 
        ctrlHeight_New = 36
        ctrlWidth_New = 180

        self.btnSearch = Button(self.frame, image=self.img_N0, text= strObj.strBtnSearch, command=self.onBtnClickSearchRecord   , justify = RIGHT, fg=myBtnTxtColor, font=(myFont, myTxtFontSize) , bg=myBtnBGColor , border=0,   highlightthickness = 0, borderwidth = 0)
        self.btnSearch.configure(height=ctrlHeight_New, width=ctrlWidth_New, compound=CENTER)
        self.btnSearch.place(x=xLblVal  , y=yVal)

        btnImg_N01 = imgPath + "rounded_btn_dark.png"
        self.img_N01=PhotoImage(file=btnImg_N01 ) 

        self.btnClearInfo = Button(self.frame, image=self.img_N01, text= strObj.strBtnClearInfo, command=self.onBtnClickClearInfo   , justify = RIGHT, fg=myBtnTxtColor, font=(myFont, myTxtFontSize) , bg=myBtnBGColor , border=0,   highlightthickness = 0, borderwidth = 0)
        self.btnClearInfo.configure(height=ctrlHeight_New, width=ctrlWidth_New, compound=CENTER)
        self.btnClearInfo.place(x=xLblVal + 190 , y=yVal)
        yVal += 35 + 40

        
        # 3. Row 3 - Dept
        self.dept = Label(self.frame, text=strObj.strDept, fg=myTxtColor, bg=myAppBGColor, font=(myFont, myTxtFontSize), justify=LEFT, anchor=W)
        self.dept.configure(height=ctrlHeight, width=ctrlWidth)
        self.dept.place(x=xLblVal,y=yVal) 

        self.entry_text_dept  = StringVar()
        self.dept_field = Entry(self.frame, width=ctrlWidth+20, textvariable=self.entry_text_dept , highlightbackground=myBorderColor, highlightcolor=myBorderColor, highlightthickness=1 , bd= 0  )        
        self.dept_field.place(x=xEdtVal, y=yVal)
        #self.dept_field.bind("<Return>", self.dept_field)
        yVal += 35

        # 4. Row 4 - Address
        self.myAdd = Label(self.frame, text=strObj.strAddress, fg=myTxtColor, bg=myAppBGColor, font=(myFont, myTxtFontSize), justify=LEFT, anchor=W)
        self.myAdd.configure(height=ctrlHeight, width=ctrlWidth)
        self.myAdd.place(x=xLblVal,y=yVal) 

        self.entry_text_myAdd	 = StringVar()
        self.myAdd_field = Entry(self.frame, width=ctrlWidth+20, textvariable=self.entry_text_myAdd , highlightbackground=myBorderColor, highlightcolor=myBorderColor, highlightthickness=1 , bd= 0  )        
        self.myAdd_field.place(x=xEdtVal, y=yVal)
        yVal += 35

        # 5. Row 5 - Mobile No
        self.myMno = Label(self.frame, text=strObj.strMobileNo, fg=myTxtColor, bg=myAppBGColor, font=(myFont, myTxtFontSize), justify=LEFT, anchor=W)
        self.myMno.configure(height=ctrlHeight, width=ctrlWidth)
        self.myMno.place(x=xLblVal,y=yVal) 

        self.entry_text_myMno	 = StringVar()
        self.myMno_field = Entry(self.frame, width=ctrlWidth+20 , textvariable=self.entry_text_myMno , highlightbackground=myBorderColor, highlightcolor=myBorderColor, highlightthickness=1 , bd= 0  )        
        self.myMno_field.place(x=xEdtVal, y=yVal)
        self.entry_text_myMno.trace('w', self.validate_num_field)
        yVal += 35

        # 6. Row 6 - Email
        self.myEmail = Label(self.frame, text=strObj.strEmpEmail, fg=myTxtColor, bg=myAppBGColor, font=(myFont, myTxtFontSize), justify=LEFT, anchor=W)
        self.myEmail.configure(height=ctrlHeight, width=ctrlWidth)
        self.myEmail.place(x=xLblVal,y=yVal) 

        self.entry_text_myEmail	 = StringVar()
        self.myEmail_field = Entry(self.frame, width=ctrlWidth+20, textvariable=self.entry_text_myEmail , highlightbackground=myBorderColor, highlightcolor=myBorderColor, highlightthickness=1 , bd= 0  )        
        self.myEmail_field.place(x=xEdtVal, y=yVal)
        yVal += 35

        # 7. Row 7 - Post
        self.myPost = Label(self.frame, text=strObj.strEmpPost, fg=myTxtColor, bg=myAppBGColor, font=(myFont, myTxtFontSize), justify=LEFT, anchor=W)
        self.myPost.configure(height=ctrlHeight, width=ctrlWidth)
        self.myPost.place(x=xLblVal,y=yVal) 

        self.entry_text_myPost	  = StringVar()
        self.myPost_field = Entry(self.frame, width=ctrlWidth+20, textvariable=self.entry_text_myPost , highlightbackground=myBorderColor, highlightcolor=myBorderColor, highlightthickness=1 , bd= 0  )        
        self.myPost_field.place(x=xEdtVal, y=yVal)
        yVal += 35

        # 8. Row 8 - DOJ
        self.myDOJ = Label(self.frame, text=strObj.strEmpDOJ, fg=myTxtColor, bg=myAppBGColor, font=(myFont, myTxtFontSize), justify=LEFT, anchor=W)
        self.myDOJ.configure(height=ctrlHeight+1, width=ctrlWidth)
        self.myDOJ.place(x=xLblVal,y=yVal) 

        self.entry_text_myDOJ	 = StringVar()
        self.myDOJ_field = Entry(self.frame, width=ctrlWidth+20, textvariable=self.entry_text_myDOJ , highlightbackground=myBorderColor, highlightcolor=myBorderColor, highlightthickness=1 , bd= 0  )        
        self.myDOJ_field.place(x=xEdtVal, y=yVal)
        self.entry_text_myDOJ.trace('w', self.validate_DOJ_field)
        yVal += 35 + 5

        # 9. Row 8 - DOB
        self.myDOB = Label(self.frame, text=strObj.strEmpDOB, fg=myTxtColor, bg=myAppBGColor, font=(myFont, myTxtFontSize), justify=LEFT, anchor=W)
        self.myDOB.configure(height=ctrlHeight+1, width=ctrlWidth)
        self.myDOB.place(x=xLblVal,y=yVal) 

        self.entry_text_myDOB = StringVar()
        self.myDOB_field = Entry(self.frame, width=ctrlWidth+20 , textvariable=self.entry_text_myDOB  , highlightbackground=myBorderColor, highlightcolor=myBorderColor, highlightthickness=1 , bd= 0  )        
        self.myDOB_field.place(x=xEdtVal, y=yVal)
        self.entry_text_myDOB.trace('w', self.validate_dateOfBirth_field)
        yVal += 35 +8

        # 9. Row 9 - Gender
        self.gender = Label(self.frame, text=strObj.strEmpGender, fg=myTxtColor, bg=myAppBGColor, font=(myFont, myTxtFontSize), justify=LEFT, anchor=W)
        self.gender.configure(height=ctrlHeight, width=ctrlWidth)
        self.gender.place(x=xLblVal,y=yVal) 
        
        global radioValue
        radioValue = IntVar()
        # Male
        self.male = Radiobutton(self.frame, text=strObj.strEmpMale, variable=radioValue, value=1, command=self.onClickRadioBtn , bg=myAppBGColor, font=(myFont, myTxtFontSize), compound="left", activeforeground= myTxtColor, activebackground = myAppBGColor)
        self.male.configure(height=ctrlHeight, width=ctrlWidth-10 , selectcolor = "light pink" )
        self.male.place(x=xEdtVal,y=yVal) 
        # FeMale
        # yVal += 35
        self.female = Radiobutton(self.frame, text=strObj.strEmpFemale, variable=radioValue, value=2, command=self.onClickRadioBtn , bg=myAppBGColor, font=(myFont, myTxtFontSize), compound="left", activeforeground= myTxtColor, activebackground = myAppBGColor)
        self.female.configure(height=ctrlHeight, width=ctrlWidth-10 , selectcolor = "light pink" )
        self.female.place(x=xEdtVal+100,y=yVal) 

        ##----add new control---
        yVal += 35
        # 10. Row 10 - Employee Status
        self.EmpStatus = Label(self.frame, text=strObj.strEmpStatus, fg=myTxtColor, bg=myAppBGColor, font=(myFont, myTxtFontSize), justify=LEFT, anchor=W)
        self.EmpStatus.configure(height=ctrlHeight, width=ctrlWidth)
        self.EmpStatus.place(x=xLblVal,y=yVal) 
        
        global radioValue_EmpStatus
        radioValue_EmpStatus = IntVar()
        # Working
        self.working = Radiobutton(self.frame, text=strObj.strEmpWorking, variable=radioValue_EmpStatus, value=1, command=self.onClickRadioBtn_EmpStatus , bg=myAppBGColor, font=(myFont, myTxtFontSize), compound="left", activeforeground= myTxtColor, activebackground = myAppBGColor)
        self.working.configure(height=ctrlHeight, width=ctrlWidth-10 , selectcolor = "light pink" )
        self.working.place(x=xEdtVal+10,y=yVal) 
        # Ex_Emp
        # yVal += 35
        self.Ex_Emp = Radiobutton(self.frame, text=strObj.strEx_Emp , variable=radioValue_EmpStatus, value=2, command=self.onClickRadioBtn_EmpStatus , bg=myAppBGColor, font=(myFont, myTxtFontSize), compound="left", activeforeground= myTxtColor, activebackground = myAppBGColor)
        self.Ex_Emp.configure(height=ctrlHeight, width=ctrlWidth-10 , selectcolor = "light pink" )
        self.Ex_Emp.place(x=xEdtVal+115,y=yVal) 


        #Display Image in Label
        imgHeight = 240
        imgWidth = 200
        xImgLblVal = 505
        yImgVal = 145
        myPhotofrm = PhotoImage(file = imgPath + 'img.png' )
        self.myImage = Label(self.frame , text="Image", image=myPhotofrm , fg=myTxtColor, bg=myAppBGColor, font=(myFont, myTxtFontSize), justify=LEFT, anchor=W)
        self.myImage.image = myPhotofrm
        self.myImage.pack()
        self.myImage.configure(height=imgHeight, width=imgWidth)
        self.myImage.place(x=xImgLblVal,y=yImgVal) 

         
        # rounded_btn_dark.png        
        btnImg_N2 = imgPath + "rounded_btn.png"
        self.img_N2=PhotoImage(file=btnImg_N2 ) 
        ctrlHeight = 36
        ctrlWidth = 180

        xbtnVal = 305
        yBtnVal = 575
        # self.btnDeleteRecord = Button(self.frame, text=strObj.strBtnDelete, command=self.onBtnClickDeleteRecord , justify = RIGHT, fg=myTxtColor, font=(myFont, myTxtFontSize) , bg=myBtnBGColor)
        # self.btnDeleteRecord.configure(height=ctrlHeight, width=ctrlWidth)
        # self.btnDeleteRecord.place(x=xbtnVal, y=yBtnVal)        
      
        # create a Submit Button and place into the root window
        xbtnVal += 240
        self.btnUpdateRecord = Button(self.frame, image=self.img_N2, text= strObj.strBtnUpdate, command=self.onBtnClickUpdateRecord  , justify = RIGHT, fg=myBtnTxtColor, font=(myFont, myTxtFontSize) , bg=myBtnBGColor , border=0,   highlightthickness = 0, borderwidth = 0)
        self.btnUpdateRecord.configure(height=ctrlHeight, width=ctrlWidth, compound=CENTER)
        self.btnUpdateRecord.place(x=xbtnVal, y=yBtnVal)

 
        #self.btnDeleteRecord['state'] = "disable"
        self.btnUpdateRecord['state'] = "disable"

    def validate_num_field(self, *args):
        value = self.entry_text_myMno.get()
        if not value.isdigit():
            self.entry_text_myMno.set(''.join(x for x in value if x.isdigit()))

    def validate_DOJ_field(self, *args):
        pattern = ['-', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        value = self.entry_text_myDOJ.get()  
        if value != '':
            last_chr = value[-1]
            match = last_chr in pattern
            if match == False:
                self.entry_text_myDOJ.set(  value.replace( last_chr , ''  )  )

    def validate_dateOfBirth_field(self, *args):
        pattern = ['-', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        value = self.entry_text_myDOB.get()
        if value != '':
            last_chr = value[-1]
            match = last_chr in pattern
            if match == False:
                self.entry_text_myDOB.set(  value.replace( last_chr , ''  )  )        


    def onBtnClickClearInfo(self):
        self.empid_field['state'] = 'normal'
        self.empid_field.delete(0, END)
        self.name_field['state'] = 'normal'
        self.name_field.delete(0, END)
        self.clear_txt()
        self.onClickRadioBtnEdit_RFD()  

    def onClickRadioBtnEdit_RFD(self):        
        # print(f"You selected the option { str(radioValueEdit_RFD.get()) } ")
        if( radioValueEdit_RFD.get() == 1 ):
            #print("Radio emp_id")
            self.name_field.delete(0, END) 
            self.empid_field['state'] = 'normal'
            self.name_field['state'] = 'disable'
            self.empid_field.focus()
        elif(radioValueEdit_RFD.get() == 2 ):
            #print("Radio emp_name")
            self.empid_field.delete(0, END)
            self.empid_field['state'] = 'disable'
            self.name_field['state'] = 'normal'
            self.name_field.focus()

    def onClickRadioBtn(self):        
        print(f"You selected the option { str(radioValue.get()) } ")

    def onClickRadioBtn_EmpStatus(self):
        print(f"You selected the option { str(radioValue_EmpStatus.get()) } ")

    def onBtnClickSearchRecord(self):
        #print("onBtnClickSearchRecord")
        empid_value = self.empid_field.get()
        name_value = self.name_field.get()

        if ( (empid_value.strip() == "" ) and ( name_value.strip() == "")  ):
            print("empty input") 
            msg.showinfo(strObj.strMsgTitel, strObj.strFillAtleastOneOption)
        else:
            # to Get emp info from db
            obj = MyMongoDB()

            # first of all check - emp. is exist or not
            bIsEmpExist = obj.Search_EmpID_OR_EmpName_AlreadyExistsInDB(empid_value.strip(), name_value.strip() )
            if(False == bIsEmpExist):
                msg.showinfo(strObj.strMsgTitel, strObj.strMsgSearchUserNotExist )
                return 

            emp_data = obj.GetEmpDataFromDB(name_value.strip(), empid_value.strip())    
            # for x in emp_data:
            #     print(f"{x} = {emp_data[x]} " )
            
            self.entry_text_empid.set(emp_data["empid"] )
            self.entry_text_name.set( emp_data["name"] )
            self.entry_text_dept.set( emp_data["department"] )
            self.entry_text_myAdd.set( emp_data["address"] )
            self.entry_text_myMno.set( emp_data["mobile"] )
            self.entry_text_myEmail.set( emp_data["email"] )
            self.entry_text_myPost.set( emp_data["designation"] )
            self.entry_text_myDOJ.set( emp_data["doj"] ) 
            self.entry_text_myDOB.set( emp_data["dob"] )
            strGenderTxt =  emp_data["gender"]    
            strGenderTxt = strGenderTxt.lower()    
            if( strGenderTxt == "male" ):
                self.male.select()   
            elif( strGenderTxt == "female" ):
                self.female.select()  
            strEmpStatusTxt =  emp_data["emp_status"]    
            strEmpStatusTxt = strEmpStatusTxt.lower()    
            if( strEmpStatusTxt == "working" ):
                self.working.select()   
            elif( strEmpStatusTxt == "ex_emp" ):
                self.Ex_Emp.select()    
            

            ## imgPath = ".\\Emp_Tmp_Image\\0.png"
            imgPath = cf.Get_Emp_Tmp_Image_Dir() + "//0.png"  ## Ajay
            myPhotofrm = PhotoImage(file = imgPath  )
            self.myImage.image = myPhotofrm  
            self.myImage.configure( image = myPhotofrm  )
            #self.btnDeleteRecord['state'] = "normal"
            self.btnUpdateRecord['state'] = "normal"

            # here we store all old values becz if user want to update the changed details of Employee in DB
            self.Save_AllOldInfoOfEmploye()

    def Save_AllOldInfoOfEmploye(self):
        # here we store all old values becz if user want to update the changed details of Employee in DB
        self.old_EmpDetails_Dictionary = dict() 

        old_empid_value = self.empid_field.get()
        old_name_value = self.name_field.get()
        old_dept_value = self.dept_field.get()
        old_myAdd_value = self.myAdd_field.get()
        old_myMno_value = self.myMno_field.get()
        old_myEmail_value = self.myEmail_field.get()
        old_myPost_value = self.myPost_field.get()
        old_myDOJ_value = self.myDOJ_field.get()
        old_myDOB_value = self.myDOB_field.get() 
        old_emp_gender_value = ""
        if( str(radioValue.get()) == "1" ):
            old_emp_gender_value = "male"
        elif( str(radioValue.get()) == "2" ):
            old_emp_gender_value = "female"
        old_emp_status_value = ""
        if( str(radioValue_EmpStatus.get()) == "1" ):
            old_emp_status_value = "working"
        elif( str(radioValue_EmpStatus.get()) == "2" ):
            old_emp_status_value = "ex_emp"            

        self.old_EmpDetails_Dictionary["empid"] = old_empid_value.strip()
        self.old_EmpDetails_Dictionary["name"] =  old_name_value.strip()
        self.old_EmpDetails_Dictionary["department"] =  old_dept_value.strip()
        self.old_EmpDetails_Dictionary["address"] =  old_myAdd_value.strip()
        self.old_EmpDetails_Dictionary["mobile"] =  old_myMno_value.strip()
        self.old_EmpDetails_Dictionary["email"] = old_myEmail_value.strip()
        self.old_EmpDetails_Dictionary["designation"] =  old_myPost_value.strip()
        self.old_EmpDetails_Dictionary["doj"] = old_myDOJ_value.strip()
        self.old_EmpDetails_Dictionary["gender"] =  old_emp_gender_value.strip()
        self.old_EmpDetails_Dictionary["emp_status"] =  old_emp_status_value.strip()
        self.old_EmpDetails_Dictionary["dob"] =    old_myDOB_value.strip()

    # Define a function for for validating an Email 
    def valideEmail(self, email):  
        # Make a regular expression for validating an Email 
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        # for custom mails use: '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'

        # pass the regular expression 
        # and the string in search() method 
        if(re.search(regex,email)):  
            print("Valid Email")  
            return True            
        else:  
            print("Invalid Email")  
            return False    

    def GetAll_Updated_InfoOfEmploye(self):
        bIsWorkDone = False
        new_EmpFullDetails_Dictionary = dict() 
        emp_tmp_dic = dict()

        empid_value = self.empid_field.get()
        name_value = self.name_field.get()
        dept_value = self.dept_field.get()
        myAdd_value = self.myAdd_field.get()
        myMno_value = self.myMno_field.get()
        myEmail_value = self.myEmail_field.get()
        myPost_value = self.myPost_field.get()
        myDOJ_value = self.myDOJ_field.get()
        myDOB_value = self.myDOB_field.get()
        myEmailIsValid = self.valideEmail( myEmail_value.strip() )

        now_dd, now_mm, now_yy = datetime.now().strftime("%d-%m-%Y").split('-')
        NowDate_Info = date( int(now_yy), int(now_mm), int(now_dd) )
        doj_day, doj_month, doj_year = myDOJ_value.split('-') 

        isValidDate_DOJ = True
        try :
            date(int(doj_year),int(doj_month),int(doj_day))
        except ValueError :
            isValidDate_DOJ = False         
        if isValidDate_DOJ :
            enter_date_Info = date( int(doj_year), int(doj_month), int(doj_day) )
            if enter_date_Info > NowDate_Info:
                msg.showinfo(strObj.strMsgTitel, strObj.strJoinDateNotGreatThanNow  ) 
                return

        dob_day, dob_month, dob_year = myDOB_value.split('-')  
        isValidDate_DOB = True
        try :
            date(int(dob_year),int(dob_month),int(dob_day))
        except ValueError :
            isValidDate_DOB = False
        if isValidDate_DOB :
            enter_date_Info = date( int(dob_year), int(dob_month), int(dob_day) )
            if enter_date_Info > NowDate_Info:
                msg.showinfo(strObj.strMsgTitel, strObj.strDOBDateNotGreatThanNow  )
                return

        emp_gender_value = ""
        if( str(radioValue.get()) == "1" ):
            emp_gender_value = "male"
        elif( str(radioValue.get()) == "2" ):
            emp_gender_value = "female"
        emp_status_value = ""
        if( str(radioValue_EmpStatus.get()) == "1" ):
            emp_status_value = "working"
        elif( str(radioValue_EmpStatus.get()) == "2" ):
            emp_status_value = "ex_emp"

        if (  (empid_value.strip() == "" ) or ( name_value.strip() == "")  or ( dept_value.strip() == "" )   or
            ( myAdd_value.strip() == "") or ( myMno_value.strip() == "") or ( myEmail_value.strip() == "") or
            (myPost_value.strip() == "") or ( myDOJ_value.strip() == "") or ( myDOB_value.strip() == "")    
        ):
            print("empty input") 
            msg.showinfo(strObj.strMsgTitel, strObj.strFillAllFileds)
        elif(   emp_gender_value.strip() == ""  ):
            msg.showinfo(strObj.strMsgTitel, strObj.strMsgSelectGender )
        elif(   emp_status_value.strip() == ""  ):
            msg.showinfo(strObj.strMsgTitel, strObj.strMsgSelectEmpStatus )            
        elif( False ==  myEmailIsValid ): 
            msg.showinfo(strObj.strMsgTitel, strObj.strEmailNotValid  )
        elif(False == isValidDate_DOJ ):
            msg.showinfo(strObj.strMsgTitel, strObj.strInValid_DOJ  )
        elif(False == isValidDate_DOB ):
            msg.showinfo(strObj.strMsgTitel, strObj.strInValid_DOB  )            
        else:
            # 1. emp full data
            emp_tmp_dic["empid"] = empid_value.strip()
            new_EmpFullDetails_Dictionary["$set"]  =  emp_tmp_dic
            
            emp_tmp_dic["name"] =  name_value.strip()
            new_EmpFullDetails_Dictionary["$set"]  =  emp_tmp_dic

            emp_tmp_dic["department"] =  dept_value.strip()
            new_EmpFullDetails_Dictionary["$set"]  =  emp_tmp_dic

            emp_tmp_dic["address"] =  myAdd_value.strip()
            new_EmpFullDetails_Dictionary["$set"]  =  emp_tmp_dic

            emp_tmp_dic["mobile"] =  myMno_value.strip()
            new_EmpFullDetails_Dictionary["$set"]  =  emp_tmp_dic

            emp_tmp_dic["email"] = myEmail_value.strip()
            new_EmpFullDetails_Dictionary["$set"]  =  emp_tmp_dic

            emp_tmp_dic["designation"] =  myPost_value.strip()
            new_EmpFullDetails_Dictionary["$set"]  =  emp_tmp_dic

            emp_tmp_dic["doj"] = myDOJ_value.strip()
            new_EmpFullDetails_Dictionary["$set"]  =  emp_tmp_dic

            emp_tmp_dic["gender"] =  emp_gender_value.strip()
            new_EmpFullDetails_Dictionary["$set"]  =  emp_tmp_dic

            emp_tmp_dic["emp_status"] =  emp_status_value.strip()
            new_EmpFullDetails_Dictionary["$set"]  =  emp_tmp_dic            

            emp_tmp_dic["dob"] =    myDOB_value.strip()
            new_EmpFullDetails_Dictionary["$set"]  =  emp_tmp_dic

            bIsWorkDone = True
            return (bIsWorkDone, new_EmpFullDetails_Dictionary)

        return (bIsWorkDone, new_EmpFullDetails_Dictionary)

                
    def SetImageInLabel(self, sImgPath):
        if(os.path.exists( sImgPath )):
            original = Image.open(sImgPath)
            resized = original.resize((200, 225) ,Image.ANTIALIAS)
            img = ImageTk.PhotoImage( resized )
            self.myImage.configure( image = img )
            self.myImage.image = img

    # Function for clearing the contents of text entry boxes 
    def clear_txt(self):         
        self.empid_field.delete(0, END)
        self.name_field.delete(0, END) 
        self.dept_field.delete(0, END) 
        self.myAdd_field.delete(0, END)
        self.myMno_field.delete(0, END)
        self.myEmail_field.delete(0, END)
        self.myPost_field.delete(0, END)
        self.myDOJ_field.delete(0, END)
        self.myDOB_field.delete(0, END)
           
        imgPath = cf.GetAppImageDirPath()    
        self.SetImageInLabel(imgPath + 'img.png')
        ## imgTmp = './/Emp_Tmp_Image//0.png'
        imgTmp = cf.Get_Emp_Tmp_Image_Dir() + "//0.png"  ## Ajay
        if os.path.isfile(imgTmp):
            os.remove(imgTmp)      

        #self.btnDeleteRecord['state'] = "disable"
        self.btnUpdateRecord['state'] = "disable"

        #self.male.set(None)
        #self.female.set(None)
        #self.radioValue.set("")

    def onBtnClickUpdateRecord(self):
        #### Note => Employe - Photo image are also not update here.
        #### Note => Update "emp_id" or "emp_name" only ONE at a single time

        # 1. Show Msg Box to confirm the updation
        MsgBox_Res = msg.askyesno(strObj.strMsgTitel, strObj.strMsgConfirm_UpdateUser, icon = 'warning')
        if( MsgBox_Res ):        
            print("onBtnClickUpdateRecord")
            
            # employee old data 
            old_EmpInfo_Dic = self.old_EmpDetails_Dictionary
            bIsWorkDone, new_EmpInfo_Dic = self.GetAll_Updated_InfoOfEmploye()
            if(bIsWorkDone):
                print("YES work is done")
                # Update data in DB
                obj = MyMongoDB()
                obj.UpdateEmployeInfo(old_EmpInfo_Dic, new_EmpInfo_Dic)

                msg.showinfo(strObj.strMsgTitel, strObj.strUpdateEmpDataInDB)

                # Also Update Image Folder Name from "old_Dept_name-old_emp_name-old_emp_id" TO ==> "new_Dept_name-new_emp_name-new_emp_id"
                old_Dept_name = old_EmpInfo_Dic.get( 'department' )
                old_emp_name = old_EmpInfo_Dic.get('name' )
                old_emp_id = old_EmpInfo_Dic.get('empid' )
                imgFolderPath = cf.GetStaffImageDirPath()
                src_old_file_name =  f"{imgFolderPath}{old_emp_id}-{old_emp_name}-{old_Dept_name}"

                new_Dept_name = new_EmpInfo_Dic['$set'].get('department' )
                new_emp_name = new_EmpInfo_Dic['$set'].get('name' )
                new_emp_id = new_EmpInfo_Dic['$set'].get('empid' )
                dest_new_file_name =  f"{imgFolderPath}{new_emp_id}-{new_emp_name}-{new_Dept_name}"

                os.rename(src_old_file_name, dest_new_file_name)

                # 3. if any change in emp_id or emp_name or department - Show Msg Box to Tain System again if any three option are edited in db
                msg.showinfo(strObj.strMsgTitel, strObj.strMsgPlsTrainTheSystem)

                # 4. call the clear() function 
                self.clear_txt()

            else:
                print("No work is NOT done")
 
                  

           


    # def onBtnClickDeleteRecord(self):
    #     print("onBtnClickDeleteRecord")
        
    #     # 1. Show Msg Box to confirm to delete record, this option will not be undo in any case

    #     # 2. delete record from DB

    #     # 3. Also delete User Image folder from Staffimage folder = "staffImages"

    #     # 4. Show Msg Box to Tain System again After any modification is DB
    #     msg.showinfo(strObj.strMsgTitel, strObj.strMsgPlsTrainTheSystem)

     


def myEditRecordsMain(root):
    
    MyEditRecordPage(root)
    

if __name__ == "__main__" :
    root = Tk()
    root.geometry("960x640")
    root.title( "strApptitle" )     
    root.resizable(False, False)
    root.configure(background="black" )

    myEditRecordsMain(root)

    root.mainloop()

