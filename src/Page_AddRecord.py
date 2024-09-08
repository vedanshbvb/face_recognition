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
#import Tkinter as tki
import datetime
 
from os.path import exists
import shutil
###import AutoCaptureFaceForTraining as start
from Mongo_DB import MyMongoDB
from datetime import *

# import imutils
# from imutils.video import VideoStream
# import sys 
# import trace 
# import ctypes 
# import multiprocessing
# from multiprocessing import Process


myAppBGColor = "lavender blush" # "white smoke" #  "grey" 
myFont = "Helvetica"
myHeadingTxtFontSize = 15
myTxtFontSize = 10
myTxtColor =  "black" # "white"
myBtnBGColor="lavender blush" # "white smoke" # "Green"
myBorderColor = "medium violet red"
myBtnTxtColor = "white"

strObj  = myStrings()
imgPath = cf.GetAppImageDirPath() 


class MyAddRecordPage(tk.Frame):
    #def __init__(self, vs, master):

    def __del__(self):
        #self.onClose()
        #msg.showinfo("Title 2 ", "Add Records close destroy....") 
        #self.onClose()
        print("Bye MyAddRecordPage-2")
         

    def __init__(self, tkFrame, Parent=None ):
        print("Hi MyAddRecordPage-2")
        #self._frame = None
        tk.Frame.__init__(self, tkFrame, Parent)

        self.myParent = Parent

        #self._frame = tkFrame
        self.myroot = tkFrame
 

        #self.stop_btn = False
        #time.sleep(1.0)
 
               
        #global bIsClose
        #bIsClose = BooleanVar()

        # define font - weight − "bold" for boldface, "normal" for regular weight
        #self.myFont = font.Font(family='Helvetica', size=13, weight='normal')

        self.frame = tk.Frame(tkFrame, width=385, height=460, borderwidth=0, bg= myAppBGColor , relief=SUNKEN   )
        #self.frame.pack(side = LEFT, anchor = "nw", fill=Y, expand=YES)
        self.frame.place(x=200-4, y=1, anchor="nw", width=758+6, height=621-1)

        #self.myframe2 = self.frame
        self.panel = None
        self._frame = None
        #self.vs = vs

        self.CreateAddRecPageGUI()

   
    def CreateAddRecPageGUI(self ):
        self.myroot.grid_columnconfigure((0,1), weight=1)

        # create a Form Heading label 
        xLblVal = 80
        yVal = 32
        ctrlHeight = 3
        ctrlWidth = 80

        # Heading...
        self.heading = Label(self.frame, text=strObj.strAddRecordPageH , fg=myTxtColor, bg=myAppBGColor, font=(myFont, myHeadingTxtFontSize), compound="left" , justify=LEFT, anchor=W )
        self.heading.configure(height=ctrlHeight, width=ctrlWidth)
        self.heading.place(x=xLblVal,y=32)  #.pack(expand=YES, fill=BOTH)     


        # self.btnAddNew = Button(self.frame, text= strObj.strBtnAddNewRecord, command=self.onBtnClickAddNewRecord  , justify = RIGHT, fg=myTxtColor, font=(myFont, myTxtFontSize) , bg=myBtnBGColor)
        # self.btnAddNew.configure(height=1, width=20)
        # self.btnAddNew.place(x=xLblVal, y=90)


        yVal += 85 + 30
        xEdtVal = 230
        ctrlHeight = 1 
        ctrlWidth = 20
        # 1. Row 1 - Emp. ID 
        self.empid = Label(self.frame, text=strObj.strEmpID , fg=myTxtColor, bg=myAppBGColor, font=(myFont, myTxtFontSize), justify=LEFT, anchor=W)
        self.empid.configure(height=ctrlHeight, width=ctrlWidth)
        self.empid.place(x=xLblVal,y=yVal) 

        self.entry_text_empid  = StringVar()
        self.empid_field = Entry(self.frame, width=ctrlWidth+20 , textvariable=self.entry_text_empid , highlightbackground=myBorderColor, highlightcolor=myBorderColor, highlightthickness=1 , bd= 0 )
        self.empid_field.place(x=xEdtVal, y=yVal) 
        self.empid_field.focus()
        #self.empid_field.bind("<Return>", self.empid_focus)
        yVal += 35

        # 2. Row 2 - Name
        self.name = Label(self.frame, text= strObj.strEmpName , fg=myTxtColor, bg=myAppBGColor, font=(myFont, myTxtFontSize), justify=LEFT, anchor=W)  
        self.name.configure(height=ctrlHeight, width=ctrlWidth)
        self.name.place(x=xLblVal,y=yVal) 

        self.name_field = Entry(self.frame, width=ctrlWidth+20 , highlightbackground=myBorderColor, highlightcolor=myBorderColor, highlightthickness=1 , bd= 0 )
        self.name_field.place(x=xEdtVal, y=yVal)
        #self.name_field.bind("<Return>", self.name_focus)        
        yVal += 35

        # 3. Row 3 - Dept
        self.dept = Label(self.frame, text=strObj.strDept , fg=myTxtColor, bg=myAppBGColor, font=(myFont, myTxtFontSize), justify=LEFT, anchor=W)
        self.dept.configure(height=ctrlHeight, width=ctrlWidth)
        self.dept.place(x=xLblVal,y=yVal) 

        self.dept_field = Entry(self.frame, width=ctrlWidth+20 , highlightbackground=myBorderColor, highlightcolor=myBorderColor, highlightthickness=1 , bd= 0 )        
        self.dept_field.place(x=xEdtVal, y=yVal)
        #self.dept_field.bind("<Return>", self.dept_field)
        yVal += 35

        # 4. Row 4 - Address
        self.myAdd = Label(self.frame, text=strObj.strAddress, fg=myTxtColor, bg=myAppBGColor, font=(myFont, myTxtFontSize), justify=LEFT, anchor=W)
        self.myAdd.configure(height=ctrlHeight, width=ctrlWidth)
        self.myAdd.place(x=xLblVal,y=yVal) 

        self.myAdd_field = Entry(self.frame, width=ctrlWidth+20 , highlightbackground=myBorderColor, highlightcolor=myBorderColor, highlightthickness=1 , bd= 0 )        
        self.myAdd_field.place(x=xEdtVal, y=yVal)
        yVal += 35

        # 5. Row 5 - Mobile No
        self.myMno = Label(self.frame, text=strObj.strMobileNo, fg=myTxtColor, bg=myAppBGColor, font=(myFont, myTxtFontSize), justify=LEFT, anchor=W)
        self.myMno.configure(height=ctrlHeight, width=ctrlWidth)
        self.myMno.place(x=xLblVal,y=yVal) 

        self.mobile_num_field = StringVar()
        self.myMno_field = Entry(self.frame, width=ctrlWidth+20, textvariable=self.mobile_num_field , highlightbackground=myBorderColor, highlightcolor=myBorderColor, highlightthickness=1 , bd= 0  )        
        self.myMno_field.place(x=xEdtVal, y=yVal)
        self.mobile_num_field.trace('w', self.validate_num_field)
        yVal += 35

        # 6. Row 6 - Email
        self.myEmail = Label(self.frame, text= strObj.strEmpEmail, fg=myTxtColor, bg=myAppBGColor, font=(myFont, myTxtFontSize), justify=LEFT, anchor=W)
        self.myEmail.configure(height=ctrlHeight, width=ctrlWidth)
        self.myEmail.place(x=xLblVal,y=yVal) 

        self.myEmail_field = Entry(self.frame, width=ctrlWidth+20 , highlightbackground=myBorderColor, highlightcolor=myBorderColor, highlightthickness=1 , bd= 0 )        
        self.myEmail_field.place(x=xEdtVal, y=yVal)
        yVal += 35

        # 7. Row 7 - Post
        self.myPost = Label(self.frame, text=strObj.strEmpPost, fg=myTxtColor, bg=myAppBGColor, font=(myFont, myTxtFontSize), justify=LEFT, anchor=W)
        self.myPost.configure(height=ctrlHeight, width=ctrlWidth)
        self.myPost.place(x=xLblVal,y=yVal) 

        self.myPost_field = Entry(self.frame, width=ctrlWidth+20 , highlightbackground=myBorderColor, highlightcolor=myBorderColor, highlightthickness=1 , bd= 0 )        
        self.myPost_field.place(x=xEdtVal, y=yVal)
        yVal += 35

        # 8. Row 8 - DOJ
        self.myDOJ = Label(self.frame, text=strObj.strEmpDOJ, fg=myTxtColor, bg=myAppBGColor, font=(myFont, myTxtFontSize), justify=LEFT, anchor=W)
        self.myDOJ.configure(height=ctrlHeight+1, width=ctrlWidth)
        self.myDOJ.place(x=xLblVal,y=yVal) 

        self.my_date_field = StringVar()
        self.myDOJ_field = Entry(self.frame, width=ctrlWidth+20, textvariable=self.my_date_field , highlightbackground=myBorderColor, highlightcolor=myBorderColor, highlightthickness=1 , bd= 0  )        
        self.myDOJ_field.place(x=xEdtVal, y=yVal)
        self.my_date_field.trace('w', self.validate_date_field)
        # self.myDOJ_field.insert(0, 'dd-mm-yy')
        # self.myDOJ_field.bind('<FocusIn>', self.on_entry_click)
        # self.myDOJ_field.bind('<FocusOut>', self.on_focusout)
        yVal += 35 +5

        
        # 9. Row 8 - DOB
        self.myDOB = Label(self.frame, text=strObj.strEmpDOB, fg=myTxtColor, bg=myAppBGColor, font=(myFont, myTxtFontSize), justify=LEFT, anchor=W)
        self.myDOB.configure(height=ctrlHeight+1, width=ctrlWidth)
        self.myDOB.place(x=xLblVal,y=yVal) 

        self.my_dateOfBirth_field = StringVar()
        self.myDOB_field = Entry(self.frame, width=ctrlWidth+20, textvariable=self.my_dateOfBirth_field , highlightbackground=myBorderColor, highlightcolor=myBorderColor, highlightthickness=1 , bd= 0 )        
        self.myDOB_field.place(x=xEdtVal, y=yVal)
        self.my_dateOfBirth_field.trace('w', self.validate_dateOfBirth_field)
        yVal += 35 +8



        # 10. Row 10 - Gender
        self.gender = Label(self.frame, text=strObj.strEmpGender, fg=myTxtColor, bg=myAppBGColor, font=(myFont, myTxtFontSize), justify=LEFT, anchor=W)
        self.gender.configure(height=ctrlHeight, width=ctrlWidth)
        self.gender.place(x=xLblVal,y=yVal) 
        
        global radioValue
        radioValue = IntVar()
        # Male
        self.male = Radiobutton(self.frame, text=strObj.strEmpMale, variable=radioValue, value=1, command=self.onClickRadioBtn , bg=myAppBGColor, font=(myFont, myTxtFontSize), compound="left", activeforeground= myTxtColor, activebackground = myAppBGColor )
        self.male.configure(height=ctrlHeight, width=ctrlWidth-10, selectcolor = "light pink"  )
        self.male.place(x=xEdtVal,y=yVal) 
        # FeMale
        # yVal += 35
        self.female = Radiobutton(self.frame, text=strObj.strEmpFemale, variable=radioValue, value=2, command=self.onClickRadioBtn , bg=myAppBGColor, font=(myFont, myTxtFontSize), compound="left", activeforeground= myTxtColor, activebackground = myAppBGColor)
        self.female.configure(height=ctrlHeight, width=ctrlWidth-10, selectcolor = "light pink"  )
        self.female.place(x=xEdtVal+100,y=yVal) 

        imgPath = cf.GetAppImageDirPath()
        #Display Image in Label
        imgHeight = 240
        imgWidth = 200
        xImgLblVal = 505 + 20
        yImgVal = 145
        myPhotofrm = PhotoImage(file = imgPath + 'img.png' )
        self.myImage = Label(self.frame , text="Image", bg="light green", image=myPhotofrm )
        self.myImage.image = myPhotofrm
        self.myImage.pack()
        self.myImage.configure(height=imgHeight, width=imgWidth)
        self.myImage.place(x=xImgLblVal,y=yImgVal) 

        # rounded_btn_dark.png        
        btnImg_N2 = imgPath + "rounded_btn.png"
        self.img_N2=PhotoImage(file=btnImg_N2 ) 
        ctrlHeight = 36
        ctrlWidth = 180

        xbtnVal = 545
        yBtnVal = 305
        self.btnPhoto = Button(self.frame, image=self.img_N2, text= strObj.strBtnCaptureImg, command=self.onBtnClickAddPhoto , justify = RIGHT, fg=myBtnTxtColor, font=(myFont, myTxtFontSize) , bg=myBtnBGColor , border=0,   highlightthickness = 0, borderwidth = 0)
        self.btnPhoto.configure(height=ctrlHeight, width=ctrlWidth, compound=CENTER)
        self.btnPhoto.place(x=xbtnVal, y=yBtnVal+100)
        
        
        btnImg_N1 = imgPath + "rounded_btn_dark.png"
        self.img_N1=PhotoImage(file=btnImg_N1 ) 
        yBtnVal  += 270
        self.Cancel_btn = Button(self.frame, image=self.img_N1, text=strObj.strBtnCancel, command=self.onBtnClickCancel , justify = RIGHT, fg=myBtnTxtColor, font=(myFont, myTxtFontSize) , bg=myBtnBGColor , border=0,   highlightthickness = 0, borderwidth = 0)
        self.Cancel_btn.configure(height=ctrlHeight, width=ctrlWidth, compound=CENTER)
        self.Cancel_btn.place(x=200+100, y=yBtnVal) 

        # create a Submit Button and place into the root window
        #yBtnVal  += 270
        self.submit_btn = Button(self.frame, image=self.img_N2, text=strObj.strBtnSave, command=self.onBtnClickSave , justify = RIGHT, fg=myBtnTxtColor, font=(myFont, myTxtFontSize) , bg=myBtnBGColor , border=0,   highlightthickness = 0, borderwidth = 0)
        self.submit_btn.configure(height=ctrlHeight, width=ctrlWidth, compound=CENTER)
        self.submit_btn.place(x=xbtnVal, y=yBtnVal) 

        self.SetNewEmpID()

    def SetNewEmpID(self):
        obj = MyMongoDB()
        newEmpId = obj.GetNextEmpID()
        self.entry_text_empid.set( newEmpId )
        self.empid_field['state'] = 'disable'


    def validate_num_field(self, *args):
        value = self.mobile_num_field.get()
        if not value.isdigit():
            self.mobile_num_field.set(''.join(x for x in value if x.isdigit()))

    def validate_date_field(self, *args):
        pattern = ['-', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        value = self.my_date_field.get()
        if value != '':
            last_chr = value[-1]
            match = last_chr in pattern
            if match == False:
                self.my_date_field.set(  value.replace( last_chr , ''  )  )

    def validate_dateOfBirth_field(self, *args):
        pattern = ['-', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        value = self.my_dateOfBirth_field.get()
        if value != '':
            last_chr = value[-1]
            match = last_chr in pattern
            if match == False:
                self.my_dateOfBirth_field.set(  value.replace( last_chr , ''  )  )        

    # use to show and hide the frames
    def Show_Child_frame(self, frame_class, classObj ):
        new_frame =  frame_class(classObj, self)
        if self._frame is not None:
            self._frame.destroy() 
            if self._frame.frame is not None:  
                self._frame.frame.destroy()

        self._frame = new_frame
        self._frame.pack()

    def OpenNewPhotoGUIPage(self ):
        import TakeEmpPhotoPage as tempImg
        self.Show_Child_frame( tempImg.MyPhotoAppPage  , self.myroot )


    def onClickRadioBtn(self):        
        print(f"You selected the option { str(radioValue.get()) } ")
    
    # def onBtnClickAddNewRecord(self):
    #     print("Add new records")
    #     self.clear_txt()


    # # Function to set focus (cursor) 
    # def empid_focus(self, event): 
    #     # set focus on the empid_field box 
    #     self.empid_field.focus_set() 
    # def name_focus(self, event): 
    #     # set focus on the sem_field box 
    #     self.name_field.focus_set()  
    # def dept_focus(self, event): 
    #     # set focus on the sem_field box 
    #     self.dept_field.focus_set()         

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
        self.SetImageInLabel(imgPath + 'img.png')


        #self.male.set(None)
        #self.female.set(None)
        #self.radioValue.set("")
         
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

    # Function to take data from GUI window and write to an excel file or etc.
    def onBtnClickSave(self): 
        # if user not fill any entry 
        # then print "empty input" 
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
        if isValidDate_DOB:
            enter_date_Info = date( int(dob_year), int(dob_month), int(dob_day) )
            if enter_date_Info > NowDate_Info:
                msg.showinfo(strObj.strMsgTitel, strObj.strDOBDateNotGreatThanNow  )
                return

        emp_gender_value = ""
        if( str(radioValue.get()) == "1" ):
            emp_gender_value = "male"
        elif( str(radioValue.get()) == "2" ):
            emp_gender_value = "female"

        if (  (empid_value.strip() == "" ) or ( name_value.strip() == "")  or ( dept_value.strip() == "" )   or
              ( myAdd_value.strip() == "") or ( myMno_value.strip() == "") or ( myEmail_value.strip() == "") or
              (myPost_value.strip() == "") or ( myDOJ_value.strip() == "") or ( myDOB_value.strip() == "")    
        ):
            print("empty input") 
            msg.showinfo(strObj.strMsgTitel, strObj.strFillAllFileds)
        elif(   emp_gender_value.strip() == ""  ):
            msg.showinfo(strObj.strMsgTitel, strObj.strMsgSelectGender )
        elif( False ==  myEmailIsValid ): 
            msg.showinfo(strObj.strMsgTitel, strObj.strEmailNotValid  )
        elif(False == isValidDate_DOJ ):
            msg.showinfo(strObj.strMsgTitel, strObj.strInValid_DOJ  )
        elif(False == isValidDate_DOB ):
            msg.showinfo(strObj.strMsgTitel, strObj.strInValid_DOB  )  
        else:
            sEmpFullDetails_Dictionary = dict()            
            # 1. emp full data
            sEmpFullDetails_Dictionary["empid"] = empid_value.strip()
            sEmpFullDetails_Dictionary["name"] =  name_value.strip()
            sEmpFullDetails_Dictionary["department"] =  dept_value.strip()
            sEmpFullDetails_Dictionary["address"] =  myAdd_value.strip()
            sEmpFullDetails_Dictionary["mobile"] =  myMno_value.strip()
            sEmpFullDetails_Dictionary["email"] = myEmail_value.strip()
            sEmpFullDetails_Dictionary["designation"] =  myPost_value.strip()
            sEmpFullDetails_Dictionary["doj"] = myDOJ_value.strip()
            sEmpFullDetails_Dictionary["gender"] =  emp_gender_value.strip()
            sEmpFullDetails_Dictionary["emp_status"] =   "working"
            sEmpFullDetails_Dictionary["dob"] =    myDOB_value.strip()    
            # 3. save in db
            obj = MyMongoDB()
            bIsEmpID_GivenToAnyOne = obj.Check_EmpID_AlreadyExistsInDB( empid_value.strip() )
            if( bIsEmpID_GivenToAnyOne):
                msg.showinfo(strObj.strMsgTitel, strObj.strMsgEmpIDAlreadyUsed )
                return
            else:         
                
                ## folder name => used in page_addrecord.py, mongo_db.py, takeempphotopage.py, page_facerecognition.py
                if( name_value.find(" ") > 0 ):
                    nameTmp = name_value.replace(" ", "_")
                else:
                    nameTmp = name_value.strip()
                if( dept_value.find(" ") > 0 ):
                    depTmp = dept_value.replace(" ", "_")
                else:
                    depTmp = dept_value.strip()
                empPhoto_value = cf.GetStaffImageDirPath() + "\\" + empid_value + "-" + nameTmp + "-" + depTmp + "\\" +  '1.png'  
                if( False == os.path.exists( empPhoto_value )):
                    msg.showinfo(strObj.strMsgTitel, strObj.strPlsAddEmPhoto)
                    ##empPhoto_value = imgPath + 'img.png'
                    return

                # 2. emp image
                #sImg = "D:\\MyAllProjects\\FaceRecognition\\staffImages\\Sofware-Ajay-99\\6.jpg"
                # read the image and convert it to RGB
                emp_image = cv2.imread(empPhoto_value, 1)
                emp_image = cv2.cvtColor(emp_image, cv2.COLOR_BGR2RGB  ) ### save Color image in db
                ###emp_image = cv2.cvtColor(emp_image, cv2.COLOR_BGR2GRAY ) ### save Gray color photo in DB

                bRes = obj.Add_Emp_NewRecordInDb_With_Photo(sEmpFullDetails_Dictionary, emp_image)
                if(bRes == False):
                    msg.showinfo(strObj.strMsgTitel, strObj.strExceedAllottedLimit )
                else:
                    msg.showinfo(strObj.strMsgTitel, strObj.strSaveEmpDataInDB)
                    msg.showinfo(strObj.strMsgTitel, strObj.strMsgPlsTrainTheSystem)
                    self.SetNewEmpID()
            # call the clear() function 
            self.clear_txt()

    
    def onBtnClickAddPhoto(self):
        dept_value = self.dept_field.get()
        name_value = self.name_field.get()
        empid_value = self.empid_field.get()

        dept_value = dept_value.strip() 
        name_value = name_value.strip()
        empid_value = empid_value.strip() 

        if ( (dept_value.strip() == "") or (name_value.strip() == "") or (empid_value.strip() == "" ) ) : 
            #msg.showinfo("AutoCaptureImage", "Details should not be empty")
            msg.showinfo(strObj.strMsgTitel, strObj.strMsgNotEmpty)

        else:       
            obj = MyMongoDB()
            bIsEmpID_GivenToAnyOne = obj.Check_EmpID_AlreadyExistsInDB( empid_value.strip() )
            if( bIsEmpID_GivenToAnyOne):
                msg.showinfo(strObj.strMsgTitel, strObj.strMsgEmpIDAlreadyUsed )
                return
            else:
                ###--To take Manual snap on button click
                self.OpenNewPhotoGUIPage( )
                
                ###--for Automatic snap - auto start to take all snaps
                ##start.StartMain(dept_value, name_value, empid_value)                
                # after taking image - display same image in label
                #empPhoto_value = cf.GetStaffImageDirPath() + "\\" + dept_value + "-" + name_value+ "-" + empid_value + "\\" +  '1.png' 
                #self.SetImageInLabel( empPhoto_value  ) 
                
             

    def SetImageInLabel(self, sImgPath):
        #sImgPath = "D:\\MyAllProjects\\FaceRecognition\\staffImages\\Class6-Tanishka-EmpID8\\3.jpg"        
        if(os.path.exists( sImgPath )):
            original = Image.open(sImgPath)
            resized = original.resize((200, 225) ,Image.ANTIALIAS)
            img = ImageTk.PhotoImage( resized )
            self.myImage.configure( image = img )
            self.myImage.image = img

    def onBtnClickCancel(self):
        dept_value = self.dept_field.get()
        name_value = self.name_field.get()
        empid_value = self.empid_field.get()
        
        dept_value = dept_value.strip() 
        name_value = name_value.strip()
        empid_value = empid_value.strip() 
        
        imgPathParent = cf.GetStaffImageDirPath()  
        folder =  empid_value  + "-" + name_value+ "-" +   dept_value
        
        path = os.path.join(imgPathParent, folder) 
        if(os.path.exists(path)):
            # Remove the specified dir
            shutil.rmtree(path) 
            #os.rmdir(path) 
        self.clear_txt()


def myAddRecordsMain(root):
    print("[INFO] warming up camera...")
    # vs = VideoStream( 0 ).start()
    # time.sleep(1.0)
    #MyAddRecordPage(vs, root)
    MyAddRecordPage( root)
    

if __name__ == "__main__" :
    root = Tk()
    root.geometry("960x640")
    root.title( "strApptitle" )     
    root.resizable(False, False)
    root.configure(background="black" )

    myAddRecordsMain(root)

    root.mainloop()

