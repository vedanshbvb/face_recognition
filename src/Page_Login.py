#from tkinter import Tk, Label, Button

from tkinter import *
from AllStrings import myStrings
import common_fun as cf 
import tkinter.messagebox as msg
import time
import tkinter.font as font
 
import tkinter as tk
#from HomePage import MyHomePage
from Mongo_DB import MyMongoDB
import Page_RegisterNewUser as newReg
import json
import os.path
from os import path
import subprocess as sp	


#import urllib.request
from urllib.parse import urlparse


myAppBGColor = "lavender blush" # "white smoke" # "grey" 
myFont = "Helvetica"
myHeadingTxtFontSize = 15
myTxtFontSize = 10
myTxtColor = "black" # "white"
myBtnBGColor= "lavender blush" # "white smoke" #  #"Green"
myBorderColor = "medium violet red"
myBtnTxtColor = "white"

strObj  = myStrings()


class MyLoginPage(tk.Frame):

    def __del__(self):
        #msg.showinfo("Title 1 ", "Login close destroy....") 
        print("Bye MyLoginPage-1")

    def __init__(self, tkFrame, Parent=None):
        print("Hi MyLoginPage-1")
        tk.Frame.__init__(self, tkFrame, Parent)

        #self.app = master
        self.myParent = Parent

        #self._frame = None
        self.bUserAlreadyRegistered = False
        

        #self._frame = master
        self.myroot = tkFrame

        #open Login Page by Default
        self._frame = None

        # define font - weight − "bold" for boldface, "normal" for regular weight
        #self.myFont = font.Font(family='Helvetica', size=13, weight='normal')

        self.frame = tk.Frame(tkFrame, width=385, height=460, borderwidth=0, bg= myAppBGColor, relief=SUNKEN   )
        ####self.frame.pack(side = LEFT, anchor = "nw", fill=Y, expand=YES)
        self.frame.place(x=200-4, y=1, anchor="nw", width=758+6, height=621-1)
 
       
        self.CreateLoginPageGUI()

        # Ajay: Check Update on server - if available than only do next step
        if( cf.CheckIsUpdateAvailable() ):
            self.ReadUpdateFileToDwnSetup()


    def ReadUpdateFileToDwnSetup(self):
        # 1. Open and Read check for update file - Json data
        # Opening JSON file 
        checkUpdateData = dict()
        updateFilePath = cf.GetUpdateFilePath()
        if path.exists( updateFilePath ): 
            with open(updateFilePath, 'r') as openfile: 
                # Reading from json file 
                checkUpdateData = json.load(openfile) 
        print(checkUpdateData) 

        # 2. Get value of 'new_ver_no' 
        server_ver_no = checkUpdateData['new_ver_no']
        print(f"server_ver_no = {server_ver_no}")

        # 3. compare 'new_ver_no' == current running app. version
        myAppVersionNo = cf.GetAppVersionNo()

        # 4. Show Msg box if 'new_ver_no' is Greater than our version
        if( cf.versiontuple(server_ver_no) > myAppVersionNo  ):
            '''
                Ex:
                >>> (2,3,1) < (10,1,1)
                True
                >>> (2,3,1) < (10,1,1,1)
                True
                >>> (2,3,1,10) < (10,1,1,1)
                True
                >>> (10,3,1,10) < (10,1,1,1)
                False
                >>> (10,3,1,10) < (10,4,1,1)
                True
            '''
            # "Please download the latest version of Face Recognition"
            bRes = msg.askyesno(strObj.strMsgCommonTitle, strObj.strDownloadNewSetup,  )
            if(bRes): # True

                # mini. main application if possible---------------------------------------  
                #self.myroot.protocol("WM_DELETE_WINDOW", root.iconify)      

                dwn_url = checkUpdateData['new_setup_url']
                print(f"Start download process...{dwn_url}")

                # setup_file_name =  ""
                # tmp = urlparse( dwn_url ) 
                # setup_file_name = os.path.basename( tmp.path )

                '''
                The first argument is the URL of the resource that you want to retrieve, and 
                the second argument is the local file path where you want to store the downloaded file.
                '''
                
                # location_ToSave_setup  = cf.GetAppDataFolderPath()  
                # cf.download_setup( dwn_url, location_ToSave_setup, setup_file_name )
                # cf.install_setup( location_ToSave_setup )

                # from Test_PageDownloadSetup import ProgressWindow                
                # self.dwn_lst = [
                #                  "" ,  
                #                  f'{dwn_url}',
                #                 # 'Bushes01.png',  'Bushes02.png', 'Bushes03.png', 'Bushes04.png', 'Bushes05.png',
                #                 # 'Forest01.png',  'Forest02.png', 'Forest03.png', 'Forest04.png', 'Road01.png',
                #                 # 'Road02.png',    'Road03.png',   'Lake01.png',   'Lake02.png',   'Field01.png' 
                #             ]
                # s = ProgressWindow(self, 'Downloading...', self.dwn_lst )  # create progress window

                from Page_Download_Seup_Ok import Download_MySetup
                
                setup_name = urlparse( dwn_url )         
                appdata_path  = cf.GetAppDataFolderPath() 
                setup_file_name = os.path.basename( setup_name.path )  
                location_ToSave_setup = appdata_path + setup_file_name
                
                # Ok Done
                s = Download_MySetup(   dwn_url, location_ToSave_setup)   

                # self.myroot.wait_window(s)  # display the window and wait for it to close
                # print('file has been downloaded')

                # Max or Restore main application if possible---------------------------------------

                # Start Setup installation
                process = sp.Popen( location_ToSave_setup, shell=True)
                process.wait() 

                # Close Itself
                


    # def rounded_rect(self, canvas, x, y, w, h, c):
    #     canvas.create_arc(x,   y,   x+2*c,   y+2*c,   start= 90, extent=90, style="arc")
    #     canvas.create_arc(x+w-2*c, y+h-2*c, x+w, y+h, start=270, extent=90, style="arc")
    #     canvas.create_arc(x+w-2*c, y,   x+w, y+2*c,   start=  0, extent=90, style="arc")
    #     canvas.create_arc(x,   y+h-2*c, x+2*c,   y+h, start=180, extent=90, style="arc")
    #     canvas.create_line(x+c, y,   x+w-c, y    )
    #     canvas.create_line(x+c, y+h, x+w-c, y+h  )
    #     canvas.create_line(x,   y+c, x,     y+h-c)
    #     canvas.create_line(x+w, y+c, x+w,   y+h-c)


    def CreateLoginPageGUI(self):
        self.myroot.grid_columnconfigure((0,1), weight=1)

        global username_verify
        global password_verify

        username_verify = StringVar()
        password_verify = StringVar()

        # create a Form Heading label 
        xLblVal = 80
        yVal = 32
        ctrlHeight = 3
        ctrlWidth = 40

        # Heading...
        self.heading = Label(self.frame, text= strObj.strLoginPageHeading, fg=myTxtColor, bg=myAppBGColor, font=(myFont, myHeadingTxtFontSize), compound="left", justify=LEFT, anchor=W )
        self.heading.configure(height=ctrlHeight, width=ctrlWidth)
        self.heading.place(x=xLblVal,y=32)  #.pack(expand=YES, fill=BOTH)     
    
        yVal += 85 + 30
        xEdtVal = 230
        ctrlHeight = 1 
        ctrlWidth = 20
        # 1. Row 1 - User Name
        self.userName = Label(self.frame, text= strObj.strUserName, fg=myTxtColor, bg=myAppBGColor, font=(myFont, myTxtFontSize), justify=LEFT, anchor=W    )
        self.userName.configure(height=ctrlHeight, width=ctrlWidth)
        self.userName.place(x=xLblVal,y=yVal) 

        self.userName_field = Entry(self.frame, width=ctrlWidth+20, textvariable=username_verify, highlightbackground=myBorderColor, highlightcolor=myBorderColor, highlightthickness=1 , bd= 0 )
        self.userName_field.place(x=xEdtVal, y=yVal) 
        #self.userName_field.bind("<Return>", self.empid_focus)
        yVal += 35
 
        # 2. Row 2 - Password
        self.Password = Label(self.frame, text=strObj.strPW, fg=myTxtColor, bg=myAppBGColor, font=(myFont, myTxtFontSize), justify=LEFT, anchor=W)  
        self.Password.configure(height=ctrlHeight, width=ctrlWidth)
        self.Password.place(x=xLblVal,y=yVal) 

        self.Password_field = Entry(self.frame, width=ctrlWidth+20, textvariable=password_verify, show= '*' , highlightbackground=myBorderColor, highlightcolor=myBorderColor, highlightthickness=1 , bd= 0 )
        self.Password_field.place(x=xEdtVal, y=yVal)
        #self.Password_field.bind("<Return>", self.name_focus)        
        #yVal += 35

        bValue = self.CheckDB_IsAnyUserExist()
        if(False == bValue):
            # Register New User
            self.lblRegNewUser = Label(self.frame, text=strObj.strRegNewUser , justify=LEFT, anchor=W, fg="blue", cursor="hand2", bg=myAppBGColor ) # , font=(myFont, myHeadingTxtFontSize)
            self.lblRegNewUser.configure(height=ctrlHeight, width=ctrlWidth  )
            self.lblRegNewUser.place(x=xLblVal,y=yVal+45) 
            self.lblRegNewUser.bind("<Button-1>", self.callback_onBtnRegNewUser)

        yVal += 395

        # Change password
        self.lblChangePW = Label(self.frame, text=strObj.strChangePW, fg="blue", cursor="hand2", bg=myAppBGColor ) # , font=(myFont, myHeadingTxtFontSize)
        self.lblChangePW.configure(height=ctrlHeight, width=ctrlWidth)
        self.lblChangePW.place(x=xLblVal,y=yVal) 
        self.lblChangePW.bind("<Button-1>", self.callback_onBtnChangePw)
        #yVal += 35
        xLblVal += 200

        # Forgot password?
        self.lblForgotPW = Label(self.frame, text= strObj.strBtnForgotPW, fg="blue", cursor="hand2", bg=myAppBGColor) # , font=(myFont, myHeadingTxtFontSize)
        self.lblForgotPW.configure(height=ctrlHeight, width=ctrlWidth)
        self.lblForgotPW.place(x=xLblVal,y=yVal) 
        self.lblForgotPW.bind("<Button-1>", self.callback_onBtnForgotPw)




        # 4. Row 4 - Button Login
        # xbtnVal = 545
        # yBtnVal = 305 + 270
        # self.btnLogin_btn = Button(self.frame, text= strObj.strBtnLogin, command=self.onBtnClickLoginVerification, justify = RIGHT, fg=myTxtColor, font=(myFont, myTxtFontSize) , bg=myBtnBGColor  )
        # self.btnLogin_btn.configure(height=ctrlHeight, width=ctrlWidth)
        # self.btnLogin_btn.place(x=xbtnVal, y=yBtnVal) 

        imgPath = cf.GetAppImageDirPath()
        btnImg_N = imgPath + "rounded_btn.png"
        self.img_N=PhotoImage(file=btnImg_N ) 

        self.BtnTxt = strObj.strBtnLogin
        xbtnVal = 545
        yBtnVal = 305 + 270
        self.btnLogin_btn = Button(self.frame, text=self.BtnTxt, image=self.img_N,  command=self.onBtnClickLoginVerification, justify = RIGHT, fg=myBtnTxtColor, font=(myFont, myTxtFontSize) , bg=myBtnBGColor, border=0,   highlightthickness = 0, borderwidth = 0  )
        self.btnLogin_btn.configure( height=36, width=180 , compound=CENTER )
        self.btnLogin_btn.place(x=xbtnVal, y=yBtnVal) 
        
         



    def CheckDB_IsAnyUserExist(self):
        # cehck DB for any user exist or not
        bUserExist = False
        objDB = MyMongoDB()
        if( objDB.bIsErrorInDB ):
            ###self.myParent.CloseMainApp()
            msg.showerror( strObj.strMsgCommonTitle,  strObj.strMsg_Mongodb_not_run)
            return

        bUserExist = objDB.IsAnyUserAlreadyRegister()
        return bUserExist




    # use to show and hide the frames
    def Show_Child_frame(self, frame_class, classObj ):
        new_frame =  frame_class(classObj, self)
        if self._frame is not None:
            self._frame.destroy() 
            if self._frame.frame is not None:  
                self._frame.frame.destroy()

        self._frame = new_frame
        self._frame.pack()

    def CreateForgotPWPageGUI(self):
        # msg.showinfo("Btn", "CreateForgotPWPageGUI")
        import PageForgotPW as fpw
        self.Show_Child_frame( fpw.MyForgotPWPage , self.myroot )
    
    def callback_onBtnForgotPw(self, event):
        #msg.showinfo("Btn", "Forgot Password")
        self.CreateForgotPWPageGUI() 

    def CreateChangePWPageGUI(self): 
        #msg.showinfo("Btn", "CreateChangePWPageGUI")
        import PageChangePW as cpwp
        self.Show_Child_frame( cpwp.MyChangePWPage , self.myroot )

    def callback_onBtnChangePw(self, event):
        #msg.showinfo("Btn", "callback_onBtnChangePw")
        self.CreateChangePWPageGUI()

    def callback_onBtnRegNewUser(self, event):
        #print("Hi")
        if(False == self.bUserAlreadyRegistered):
            self.Show_Child_frame( newReg.MyRegisterNewUserPage  , self.myroot )

        
                

    def onBtnClickLoginVerification(self):
        username1 = username_verify.get()
        password1 = password_verify.get()

        username1 = username1.strip()
        password1 = password1.strip()

        # get saved user and PW from DB
        objDB = MyMongoDB()
        mydataList = objDB.GetUserName_PW()
        user_db = ""
        pw_db = ""
        if( len(mydataList) > 0 ):
            user_db =  mydataList[0]   
            pw_db = mydataList[1] 
        else:
            msg.showerror( strObj.strMsgCommonTitle,  strObj.strMsgRegBeforeLogin)
            return

        if(username1 == ""):
            msg.showinfo( strObj.strMsgCommonTitle,  strObj.strUserNameNotEmpty)
        elif(password1 == ""):
            msg.showinfo(strObj.strMsgCommonTitle, strObj.strPWNotEmpty)
        elif( ( username1 == user_db) and (password1 == pw_db) ):
            msg.showinfo(strObj.strMsgCommonTitle, strObj.strLoginOK)           
            #--self.userName_field.delete(0, END)
            #--self.Password_field.delete(0, END) 
            self.myParent.bIsLogInPass = True
            self.myParent.onBtnAddRecords()
            return
        else:
            msg.showinfo(strObj.strMsgCommonTitle,  strObj.strUser_PW_Incorrect)

        # this will delete the entry after login button is pressed
        self.userName_field.delete(0, END)
        self.Password_field.delete(0, END)

    

def myLoginMain(root):    
    MyLoginPage(root)
 

if __name__ == "__main__" :
    root = Tk()
    root.geometry("960x640")
    root.title( "strApptitle" )     
    root.resizable(False, False)
    root.configure(background="pink" )

    myLoginMain(root)     

    root.mainloop()

