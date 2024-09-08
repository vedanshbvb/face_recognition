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

 
myAppBGColor =  "lavender blush" #  "grey" 
myFont = "Helvetica"
myHeadingTxtFontSize = 15
myTxtFontSize = 10
myTxtColor = "black" #  "white"
myBtnBGColor=  "lavender blush" # "Green"
myBorderColor = "medium violet red"
myBtnTxtColor = "white"


strObj  = myStrings()
imgPath = cf.GetAppImageDirPath() 

class RemoveFaceFrom_Detection(tk.Frame): 
    def __del__(self):
        print("Bye RemoveFaceFrom_Detection-3")

    def __init__(self, tkFrame, Parent=None):
        print("Hi RemoveFaceFrom_Detection-3")

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
        self.heading = Label(self.frame, text=strObj.strRemoveFacePageHeading , fg=myTxtColor, bg=myAppBGColor, font=(myFont, myHeadingTxtFontSize), compound="left" , justify=LEFT, anchor=W )
        self.heading.configure(height=ctrlHeight, width=ctrlWidth)
        self.heading.place(x=xLblVal,y=32)  #.pack(expand=YES, fill=BOTH)     


        yVal += 85 
        xEdtVal = 230
        ctrlHeight = 1 
        ctrlWidth = 20

        global radioValue_RFD
        radioValue_RFD = IntVar()
        # 1. Radio - emp_id
        self.emp_id = Radiobutton(self.frame, text=strObj.strEmpID,  bg=myAppBGColor, font=(myFont, myTxtFontSize), compound="left", variable=radioValue_RFD, value=1, command=self.onClickRadioBtn_RFD, activeforeground= myTxtColor, activebackground = myAppBGColor)
        self.emp_id.configure(height=ctrlHeight, width=ctrlWidth, selectcolor = "light pink")
        self.emp_id.place(x=xLblVal,y=yVal) 
        self.emp_id.select()

        self.entry_text_empid  = StringVar()
        self.empid_field = Entry(self.frame, width=ctrlWidth+20, textvariable=self.entry_text_empid , highlightbackground=myBorderColor, highlightcolor=myBorderColor, highlightthickness=1 , bd= 0  )
        self.empid_field.place(x=xEdtVal, y=yVal)
        self.empid_field.focus() 
        #self.empid_field.bind("<Return>", self.empid_focus)
        yVal += 35

        # 2. Radio - emp_name
        self.emp_name = Radiobutton(self.frame, text=strObj.strEmpName,  bg=myAppBGColor, font=(myFont, myTxtFontSize), compound="left", variable=radioValue_RFD, value=2, command=self.onClickRadioBtn_RFD, activeforeground= myTxtColor, activebackground = myAppBGColor)
        self.emp_name.configure(height=ctrlHeight, width=ctrlWidth, selectcolor = "light pink")
        self.emp_name.place(x=xLblVal-8,y=yVal) 


        self.entry_text_name  = StringVar()
        self.name_field = Entry(self.frame, width=ctrlWidth+20, textvariable=self.entry_text_name  , highlightbackground=myBorderColor, highlightcolor=myBorderColor, highlightthickness=1 , bd= 0  )
        self.name_field.place(x=xEdtVal, y=yVal)
        #self.name_field.bind("<Return>", self.name_focus) 
        self.name_field['state'] = 'disable'        
        yVal += 35

        # rounded_btn_dark.png        
        btnImg_N0 = imgPath + "rounded_btn.png"
        self.img_N0=PhotoImage(file=btnImg_N0 ) 
        ctrlHeight_New = 36
        ctrlWidth_New = 180

        self.btnSearch = Button(self.frame, image=self.img_N0, text= strObj.strBtnSearchToRemoveFace, command=self.onBtnClickSearchRecord   , justify = RIGHT, fg=myBtnTxtColor, font=(myFont, myTxtFontSize) , bg=myBtnBGColor , border=0,   highlightthickness = 0, borderwidth = 0)
        self.btnSearch.configure(height=ctrlHeight_New, width=ctrlWidth_New, compound=CENTER)
        self.btnSearch.place(x=xLblVal , y=yVal)
        
        btnImg_N01 = imgPath + "rounded_btn_dark.png"
        self.img_N01=PhotoImage(file=btnImg_N01 ) 

        self.btnClearInfo = Button(self.frame, image=self.img_N01, text= strObj.strBtnClearInfo, command=self.onBtnClickClearInfo   , justify = RIGHT, fg=myBtnTxtColor, font=(myFont, myTxtFontSize) , bg=myBtnBGColor  , border=0,   highlightthickness = 0, borderwidth = 0)
        self.btnClearInfo.configure(height=ctrlHeight_New, width=ctrlWidth_New, compound=CENTER)
        self.btnClearInfo.place(x=xLblVal + 190 , y=yVal)
        yVal += 35 + 40
        
        
        # 3. Row 3 - Dept
        self.dept = Label(self.frame, text=strObj.strDept, fg=myTxtColor, bg=myAppBGColor, font=(myFont, myTxtFontSize), justify=LEFT, anchor=W)
        self.dept.configure(height=ctrlHeight, width=ctrlWidth)
        self.dept.place(x=xLblVal,y=yVal) 

        self.entry_text_dept  = StringVar()
        self.dept_field = Entry(self.frame, width=ctrlWidth+20, textvariable=self.entry_text_dept, highlightbackground=myBorderColor, highlightcolor=myBorderColor, highlightthickness=1 , bd= 0  )        
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
        self.myMno_field = Entry(self.frame, width=ctrlWidth+20 , textvariable=self.entry_text_myMno, highlightbackground=myBorderColor, highlightcolor=myBorderColor, highlightthickness=1 , bd= 0  )        
        self.myMno_field.place(x=xEdtVal, y=yVal)
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
        yVal += 35

        # 9. Row 8 - DOB
        self.myDOB = Label(self.frame, text=strObj.strEmpDOB, fg=myTxtColor, bg=myAppBGColor, font=(myFont, myTxtFontSize), justify=LEFT, anchor=W)
        self.myDOB.configure(height=ctrlHeight+1, width=ctrlWidth)
        self.myDOB.place(x=xLblVal,y=yVal) 

        self.entry_text_myDOB = StringVar()
        self.myDOB_field = Entry(self.frame, width=ctrlWidth+20 , textvariable=self.entry_text_myDOB  , highlightbackground=myBorderColor, highlightcolor=myBorderColor, highlightthickness=1 , bd= 0  )        
        self.myDOB_field.place(x=xEdtVal, y=yVal)
        yVal += 35

        # 9. Row 9 - Gender
        self.gender = Label(self.frame, text=strObj.strEmpGender, fg=myTxtColor, bg=myAppBGColor, font=(myFont, myTxtFontSize), justify=LEFT, anchor=W)
        self.gender.configure(height=ctrlHeight, width=ctrlWidth)
        self.gender.place(x=xLblVal,y=yVal) 
        
        global radioValue
        radioValue = IntVar()
        # Male
        self.male = Radiobutton(self.frame, text=strObj.strEmpMale, variable=radioValue, value=1, command=self.onClickRadioBtn , bg=myAppBGColor, font=(myFont, myTxtFontSize), compound="left", activeforeground= myTxtColor, activebackground = myAppBGColor)
        self.male.configure(height=ctrlHeight, width=ctrlWidth-10, selectcolor = "light pink")
        self.male.place(x=xEdtVal,y=yVal) 
        # FeMale
        # yVal += 35
        self.female = Radiobutton(self.frame, text=strObj.strEmpFemale, variable=radioValue, value=2, command=self.onClickRadioBtn , bg=myAppBGColor, font=(myFont, myTxtFontSize), compound="left", activeforeground= myTxtColor, activebackground = myAppBGColor)
        self.female.configure(height=ctrlHeight, width=ctrlWidth-10, selectcolor = "light pink")
        self.female.place(x=xEdtVal+100,y=yVal) 

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

        
        ctrlHeight = 36
        ctrlWidth = 180

        xbtnVal = 500
        yBtnVal = 565        
        self.btnRemovefrmFR = Button(self.frame , image=self.img_N0, text=strObj.strBtnRemoveFace , command=self.onBtnClickRemoveUserFromFaceDetectionOnly , justify = RIGHT, fg=myBtnTxtColor, font=(myFont, myTxtFontSize) , bg=myBtnBGColor  , border=0,   highlightthickness = 0, borderwidth = 0)
        self.btnRemovefrmFR.configure(height=ctrlHeight, width=ctrlWidth+6 , compound=CENTER)
        self.btnRemovefrmFR.place(x=xbtnVal, y=yBtnVal)

        self.btnRemovefrmFR['state'] = "disable"
 
    def onBtnClickClearInfo(self):
        self.empid_field['state'] = 'normal'
        self.empid_field.delete(0, END)
        self.name_field['state'] = 'normal'
        self.name_field.delete(0, END)
        self.clear_txt()
        self.onClickRadioBtn_RFD()         


    def onClickRadioBtn_RFD(self):        
        # print(f"You selected the option { str(radioValue_RFD.get()) } ")
        if( radioValue_RFD.get() == 1 ):
            #print("Radio emp_id")
            self.name_field.delete(0, END) 
            self.empid_field['state'] = 'normal'
            self.name_field['state'] = 'disable'
            self.empid_field.focus()
        elif(radioValue_RFD.get() == 2 ):
            #print("Radio emp_name")
            self.empid_field.delete(0, END)
            self.empid_field['state'] = 'disable'
            self.name_field['state'] = 'normal'
            self.name_field.focus()
        
    def onClickRadioBtn(self):        
        print(f"You selected the option { str(radioValue.get()) } ")             

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

            ## imgPath = ".\\Emp_Tmp_Image\\0.png"
            imgPath = cf.Get_Emp_Tmp_Image_Dir() + "//0.png"  ## Ajay
            myPhotofrm = PhotoImage(file = imgPath  )
            self.myImage.image = myPhotofrm  
            self.myImage.configure( image = myPhotofrm  )
            self.btnRemovefrmFR['state'] = "normal"
            self.SetBtnState_RemoveUserFromFaceDetectionOnly( )

    def SetBtnState_RemoveUserFromFaceDetectionOnly(self ):
            dept_value = self.dept_field.get()
            name_value = self.name_field.get()
            empid_value = self.empid_field.get()
            
            dept_value = dept_value.strip() 
            name_value = name_value.strip()
            empid_value = empid_value.strip() 
            
            imgPathParent = cf.GetStaffImageDirPath()  
            folder = empid_value  + "-" + name_value+ "-" +   dept_value
            path = os.path.join(imgPathParent, folder) 
            if(os.path.exists(path)):
                # show btn to remove user photo folder
                self.btnRemovefrmFR['state'] = "normal"
            else:
                #disable btn - i.e user image folder is not available 
                #already remove user from face detection
                # so disable btn
                self.btnRemovefrmFR['state'] = "disable"


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
        
        self.btnRemovefrmFR['state'] = "disable"
        

        
    

    

    def onBtnClickRemoveUserFromFaceDetectionOnly(self):
        print("onBtnClickRemoveUserFromFaceDetectionOnly")
        
        # 1. Show Msg Box to confirm to remove User from face Detection process only
        MsgBox_Res = msg.askyesno(strObj.strMsgTitel, strObj.strMsgConfirm_RemoveUser_FR, icon = 'warning')
        if( MsgBox_Res ):
            print("delete image folder")
            # 2. delete User Image folder from Staffimage folder = "staffImages"
            dept_value = self.dept_field.get()
            name_value = self.name_field.get()
            empid_value = self.empid_field.get()
            
            dept_value = dept_value.strip() 
            name_value = name_value.strip()
            empid_value = empid_value.strip() 
            
            imgPathParent = cf.GetStaffImageDirPath() 
            folder = empid_value  + "-" + name_value+ "-" +   dept_value 
            
            path = os.path.join(imgPathParent, folder) 
            if(os.path.exists(path)):
                # Remove the specified dir
                shutil.rmtree(path) 
                #os.rmdir(path) 
            self.clear_txt()

            # 3. Show Msg Box to Tain System again After any modification is DB
            msg.showinfo(strObj.strMsgTitel, strObj.strMsgPlsTrainTheSystem)



def myRemoveFaceFrom_Detection_Main(root):
    
    RemoveFaceFrom_Detection(root)
    

if __name__ == "__main__" :
    root = Tk()
    root.geometry("960x640")
    root.title( "strApptitle" )     
    root.resizable(False, False)
    root.configure(background="black" )

    myRemoveFaceFrom_Detection_Main(root)

    root.mainloop()

