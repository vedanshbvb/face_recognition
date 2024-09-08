'''
Ajay Sharma: Main UI class with seven left side button to open related frame in it.
'''

#from tkinter import Tk, Label, Button

from tkinter import *
from AllStrings import myStrings
import common_fun as cf 
import tkinter.messagebox as msg
import time
import tkinter.font as font

import PageTrialNag as trialNag

import Page_Login as loginPage
import Page_AddRecord as addRecoPage
import Page_EditRecord as editRecoPage
import Page_TrainedSystem as trainSys
import Page_AttendanceSystem as chkAttendance
import Page_FaceRecognition as faceRecog
import Page_About as abt
import Page_RemoveFaceFrom_Detection as rFD
import datetime
import json
import os 
from datetime import *
import objcrypt
#import threading
import subprocess
import Start_Stop_MongoDb as mg

import urllib
from urllib.request import urlopen
import requests

## https://www.rapidtables.com/web/color/RGB_Color.html#color-table
myBtnTxtCol_N = "dark magenta" # 'yellow'
myBtnTxtCol_H =  "slate blue" # 'white'
myBtnTxtCol_D = 'black'
myBtnTxtCol_Disable = "navy"
 
myAppBGColor = "Black" # "yellow"  #"white" # "medium violet red"  # 
myFont = "Helvetica"
myHeadingTxtFontSize = 15
myTxtFontSize = 10
myTxtColor = "red" # "white"
myBtnBGColor="Green"

strObj  = myStrings()
imgPath = cf.GetAppImageDirPath()

import tkinter as tk

# import sys
# sys.setrecursionlimit(20000)



class MyButton(tk.Button):
    def __init__(self, master, **kw):
        tk.Button.__init__(self,master=master,**kw)
        #self.defaultBackground = self["background"]
        ##self["background"] = myAppBGColor # "black" # to set button back ground

        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
       
    def on_enter(self, e):
        # self['background'] = self['activebackground']
        #self['font'] = 
        self['fg'] = myBtnTxtCol_H

    def on_leave(self, e):
        #self['background'] = self.defaultBackground
        self['fg'] = myBtnTxtCol_N

   


class MyHomePage(tk.Tk):
    #def __init__(self,master):

    # def __del__(self):
    #     self.CloseMainApp()
  
    def __init__(self):
        #tk.Tk.__init__(self)
        #self._frame = None

        master = tk.Tk()
        tk.Frame.__init__(self, master)

        ## to bring top most 
        master.call('wm', 'attributes', '.', '-topmost', True)


        # VERY IMP ==> START MONGO DB ---
        self.StartMongoDB()

        # Main frame W = 962, H = 672
        # Left frame W = 198, H = 621
        # Right frame W = 758, H = 621
        # Bottom status bar W = 960, H = 19
                
        master.geometry("960x640")
        master.title( strObj.strApptitle )     
        master.resizable(False, False)
        master.configure(background=myAppBGColor )
        master.wm_iconbitmap(  imgPath + "app.ico" )


        # define font - weight − "bold" for boldface, "normal" for regular weight
        self.myFont = font.Font(family='Helvetica', size=13, weight='normal')
        #self.myFontDisableBtn = font.Font(family='Helvetica', size=14, weight='bold')

        self.statusvar = StringVar()
        self.statusvar.set("Test status bar")
        self.mystatusbar = Label(master, borderwidth=1, textvariable=self.statusvar, relief=SUNKEN, anchor="w")
        self.mystatusbar.pack(side=BOTTOM, fill=X)

        self.frame = tk.Frame(master, borderwidth=0, bg= myAppBGColor, relief=SUNKEN    )
        self.frame.pack(side = LEFT, anchor = "nw", fill=Y, expand=YES) 

##-----------------------
        #### Set Left side Back Ground Image of App
        BG_IMAGE_PATH = imgPath +  'left_bg.png'
        BG_photo = tk.PhotoImage(file= BG_IMAGE_PATH )
        self.label = tk.Label(self.frame, image=BG_photo ,   highlightthickness = 0, borderwidth = 0)
        self.label.image = BG_photo
        self.label.place(x=0, y=0)
# ##-----------------------
 

        global bIsLogInPass
        self.bIsLogInPass = False

        global bIsRegVersion
        self.bIsRegVersion = False



        self.btnWidth  = "194" # "194"
        self.btnHeight =  "53"  
        
        self.objTkRoot = master

        # 0. Create Login Buton
        # self.btnLogin = MyButton(self.frame, text= strObj.strLogin, justify = LEFT, border=0, command=self.onBtnLogin, compound="center", fg= myBtnTxtCol_N   )        
        # self.btnLogin.config(image=self.img_N, width= self.btnWidth, height=self.btnHeight)
        # self.btnLogin['font'] = self.myFont
        # self.btnLogin.pack()
        yPadNo = 14
        myRowStart = 1
        # 1. 
        btnImg_N1 = imgPath + "btn_1_enable.png"
        self.img_N1=PhotoImage(file=btnImg_N1 )

        self.btnAddRecords = MyButton(self.frame, text= strObj.strAddRecords, justify = LEFT, border=0, command=self.onBtnAddRecords, compound="center", fg=myBtnTxtCol_N ,   highlightthickness = 0, borderwidth = 0   )
        self.btnAddRecords.config(image=self.img_N1, width= self.btnWidth, height=self.btnHeight , pady=yPadNo )
        self.btnAddRecords['font'] = self.myFont
        self.btnAddRecords.grid(row=myRowStart,column=0)
        self.btnAddRecords_state = True

        # 2.
        btnImg_N2 = imgPath + "btn_2_enable.png"
        self.img_N2=PhotoImage(file=btnImg_N2 )
        myRowStart += 1
        self.btnTainSys = MyButton(self.frame, text= strObj.strTrainSystem, justify = LEFT, border=0, command=self.onBtnTainSystem , compound="center" , fg=myBtnTxtCol_N ,   highlightthickness = 0, borderwidth = 0 )
        self.btnTainSys.config(image=self.img_N2, width= self.btnWidth, height=self.btnHeight , pady=yPadNo)
        self.btnTainSys['font'] = self.myFont
        self.btnTainSys.grid(row=myRowStart,column=0)
        self.btnTainSys_state = True

        # 3.
        btnImg_N3 = imgPath + "btn_3_enable.png"
        self.img_N3=PhotoImage(file=btnImg_N3 )        
        myRowStart += 1
        self.btnFaceRecognition = MyButton(self.frame, text= strObj.strStartFaceRecognition, justify = LEFT, border=0, command=self.onBtnFaceRecognition , compound="center" , fg=myBtnTxtCol_N ,   highlightthickness = 0, borderwidth = 0 )
        self.btnFaceRecognition.config(image=self.img_N3, width= self.btnWidth, height=self.btnHeight , pady=yPadNo)
        self.btnFaceRecognition['font'] = self.myFont
        self.btnFaceRecognition.grid(row=myRowStart,column=0)
        self.btnFaceRecognition_state = True   

        # 4.
        btnImg_N4 = imgPath + "btn_4_enable.png"
        self.img_N4=PhotoImage(file=btnImg_N4 )        
        myRowStart += 1
        self.btnCheckAttendance = MyButton(self.frame, text= strObj.strAttendanceInfo, justify = LEFT, border=0, command=self.onBtnCheckAttendance , compound="center" , fg=myBtnTxtCol_N ,   highlightthickness = 0, borderwidth = 0 )
        self.btnCheckAttendance.config(image=self.img_N4, width= self.btnWidth, height=self.btnHeight , pady=yPadNo)
        self.btnCheckAttendance['font'] = self.myFont
        self.btnCheckAttendance.grid(row=myRowStart,column=0) 
        self.btnCheckAttendance_state = True      
        
        # 5.
        btnImg_N5 = imgPath + "btn_5_enable.png"
        self.img_N5=PhotoImage(file=btnImg_N5 )        
        myRowStart += 1
        self.btnEditRecords = MyButton(self.frame, text= strObj.strEditRecords, justify = LEFT, border=0, command=self.onBtnEditRecords, compound="center" , fg=myBtnTxtCol_N ,   highlightthickness = 0, borderwidth = 0 )
        self.btnEditRecords.config(image=self.img_N5, width= self.btnWidth, height=self.btnHeight , pady=yPadNo)
        self.btnEditRecords['font'] = self.myFont
        self.btnEditRecords.grid(row=myRowStart,column=0)
        self.btnEditRecords_state = True
        
        # 6.
        btnImg_N6 = imgPath + "btn_6_enable.png"
        self.img_N6=PhotoImage(file=btnImg_N6 )        
        myRowStart += 1
        self.btnRemoveFace_Detection = MyButton(self.frame, text= strObj.strRemoveFace_Detection, justify = LEFT, border=0, command=self.onBtnRemoveFace_Detection , compound="center" , fg=myBtnTxtCol_N ,   highlightthickness = 0, borderwidth = 0 )
        self.btnRemoveFace_Detection.config(image=self.img_N6, width= self.btnWidth, height=self.btnHeight , pady=yPadNo)
        self.btnRemoveFace_Detection['font'] = self.myFont
        self.btnRemoveFace_Detection.grid(row=myRowStart,column=0)
        self.btnRemoveFace_Detection_state = True 

        # 7.
        btnImg_N7 = imgPath + "btn_7_enable.png"
        self.img_N7=PhotoImage(file=btnImg_N7 )        
        myRowStart += 1
        self.btnAbout = MyButton(self.frame, text= strObj.strAbout, justify = LEFT, border=0, command=self.onBtnAbout , compound="center" , fg=myBtnTxtCol_N ,   highlightthickness = 0, borderwidth = 0 )
        self.btnAbout.config(image=self.img_N7, width= self.btnWidth, height=self.btnHeight , pady=yPadNo)
        self.btnAbout['font'] = self.myFont
        self.btnAbout.grid(row=myRowStart,column=0)
        self.btnAbout_state = True  


        global bPlsStopCameraBeforeMoveNextPage 
        self.bPlsStopCameraBeforeMoveNextPage = False
        #open Login Page by Default
        self._frame = None

        # Online key checking system has been developed by "Ajay Sharma" in Django RestAPI
        self.OnAppLaunch_VerifyAppKeyOnLine()

        ##---Here we Check For Trial version------
        ## 1. check key file is available or Not
        strKeyDirPath = cf.GetKeyDirPath()
        keyfilePath =  strKeyDirPath + "key.key"
        if os.path.exists(keyfilePath):
            ## check expire date - Read key file and decrypt it
            bIsRunApp, machine_id_frm_key_file = self.GetTrialStatus(keyfilePath)
            if(bIsRunApp == False):
                ## Open Trial Key Page...
                print("open Trial nag page")
                self.bIsRegVersion = False
                self.OpenTrialKeyNagPage()
            else:
                ## Run application...
                print("Ok No problem")

                self.bIsRegVersion = True
                ## here we check machine id if it match than OK else Open Trial Nag
                my_mac_id = cf.GetMachineUniqueID()

                ##- Very IMP--
                if( machine_id_frm_key_file.lower() == my_mac_id.lower() ):
                    ## Compare Machine ID
                    self.onBtnLogin()  
                else:   
                    ## Open Trial Key Page...
                    print("open Trial nag page")
                    self.bIsRegVersion = False
                    self.OpenTrialKeyNagPage()
        else:
            ## open Trial nag page
            print("open Trial nag page")
            self.bIsRegVersion = False
            self.OpenTrialKeyNagPage()
            self.statusvar.set( strObj.strRegYourPrd)  ##("Please Register your Product")
        ##----------------------------------------
        global sAppStatus
        self.sAppStatus = self.statusvar.get()
        print(self.sAppStatus)

        ##---self.onBtnLogin()     
    # def CloseMainApp(self):
    #     ##self.master.q
    #     print("Close Mian Appliction")
    #     ##self.master.quit()
    #     self.StopMongoDB()


    # def Decrypt_Data(self, keyfilePath ):
    #     crypter = objcrypt.Crypter('key', 'cbc')
    #     ##Read file to decrypt
    #     read_file_data = dict()
    #     with open( keyfilePath ) as f_data:
    #         read_file_data = json.load( f_data )
    #     # decrypt now
    #     dec_dict = crypter.decrypt_object(read_file_data)
    #     print("Decrypt_Data done")
    #     return dec_dict 


    def Is_InternetWork(self):
        try:
            url='http://google.com'
            timeout=1
            urlopen(url, timeout=timeout)
            return True
        except urllib.error.URLError as er:
            print(er)
            return False

    def OnAppLaunch_VerifyAppKeyOnLine(self):
        # check online key on server
        '''
        Case 1: Internet not working: Do nothing start work as previously done
        Case 2: Internet Available:
                1 - Read key.key file - Not found 
                    -- open Trial Nag Page or it is manage previously
                2 - Read key.key file - Found
                    - send following json info. to server
                        {
                            "key":"aaaa",
                            "mac_id":"ggg",
                            "ver_no" : "1.0.0.1"
                        }
                    - Get server Response 
                        - Update all info. in file Key.key
        '''
        # case 1.
        if( self.Is_InternetWork() ):
            # case 2.
            strKeyDirPath = cf.GetKeyDirPath()
            keyfilePath =  strKeyDirPath + "key.key"
            if os.path.exists(keyfilePath):
                # read "key" and "mac_id" from file
                file_data = cf.Decrypt_Data(keyfilePath) 
                strKey = file_data['key'] 
                
                bIsKeyOk,  server_response_data = cf.VerifyKeyOnOur_WebServer(strKey, "keycheckonrun")  
                if( bIsKeyOk):
                    cf.Encrypt_Data(keyfilePath, server_response_data)
                else:
                    # According to Server key not valid So, delete key file
                    os.remove(keyfilePath)
                ##--------------------------------------------------------------------

    def GetTrialStatus(self, keyfilePath):
        ## Read 'key.key' file to get all information which was saved after on-line activation
        bIsRunApp = False
        file_data = cf.Decrypt_Data(keyfilePath) 
        my_dbkey = file_data['key']
        exp_date = file_data['key2']
        total_emp_no = file_data['key3']
        mac_id = file_data['key4']
          

        if( my_dbkey  == ''  or exp_date == '' or total_emp_no  == ''  or  mac_id  == '' ):
            print("Date formate not Valid...")  
            bIsRunApp = False 
            return bIsRunApp, mac_id

        exp_yy, exp_mm, exp_dd = exp_date.split('-')
        ExpireDate_Info = date( int(exp_yy), int(exp_mm), int(exp_dd) )
        expire_date_to_show =   f"{exp_dd}-{exp_mm}-{exp_yy}"

        now_dd, now_mm, now_yy = datetime.now().strftime("%d-%m-%Y").split('-')
        NowDate_Info = date( int(now_yy), int(now_mm), int(now_dd) )
        # Check the dates 
        ##key = "DummyKey"
        if ExpireDate_Info == NowDate_Info: 
            print("Both are equal...so run application")             
            self.statusvar.set(f"{strObj.strKeyExpireOn} {expire_date_to_show}")
            bIsRunApp = True
            # if( my_dbkey.lower() ==  key.lower() ):
            #     print("Both are equal...so run application")  
            #     bIsRunApp = True
            # else:
            #     print("Pls enter correct key...") 
            #     bIsRunApp = False
        elif ExpireDate_Info < NowDate_Info: 
            print("Trial expired...never run the application...")  
            bIsRunApp = False   
            self.statusvar.set(f"{strObj.strKeyExpired} {expire_date_to_show}")           
        else: 
            print("run application...") 
            bIsRunApp = True
            self.statusvar.set(f"{strObj.strKeyExpireOn} {expire_date_to_show}")
        return bIsRunApp, mac_id  
        


    # use to show and hide the frames
    def switch_frame(self, frame_class, classObj ):
        new_frame =  frame_class(classObj, self)
        if self._frame is not None:
            self._frame.destroy() 
            if self._frame.frame is not None:  
                self._frame.frame.destroy()

        self._frame = new_frame
        self._frame.pack()
        
         
    def upload(self):
        self.statusvar.set("Busy..")
        self.mystatusbar.update()
        import time
        time.sleep(2)
        self.statusvar.set("Ready....")

    def SetNormalButtonState(self):
        bState = "normal" 
        ####self.btnLogin["state"]           = bState
        self.btnAddRecords["state"]      = bState
        self.btnEditRecords["state"]     = bState
        self.btnTainSys["state"]         = bState
        self.btnCheckAttendance["state"] = bState
        self.btnFaceRecognition["state"] = bState
        self.btnAbout["state"]           = bState
        self.btnRemoveFace_Detection["state"]  = bState

        self.btnAddRecords_state = True
        self.btnTainSys_state = True
        self.btnFaceRecognition_state = True
        self.btnCheckAttendance_state = True
        self.btnEditRecords_state = True
        self.btnRemoveFace_Detection_state = True
        self.btnAbout_state = True


    def SetNormalImageOnBtns(self):
        
        #1.
        self.imgBtn_N1 = PhotoImage(file= imgPath + "btn_1_enable.png" )
        self.btnAddRecords.config(image=self.imgBtn_N1  )
        self.btnAddRecords['font'] = self.myFont
        self.btnAddRecords['fg'] = myBtnTxtCol_N
        #2.
        self.imgBtn_N2 = PhotoImage(file= imgPath + "btn_2_enable.png" )
        self.btnTainSys.config(image=self.imgBtn_N2 )      
        self.btnTainSys['font'] = self.myFont
        self.btnTainSys['fg'] = myBtnTxtCol_N
        #3.
        self.imgBtn_N3 = PhotoImage(file= imgPath + "btn_3_enable.png" )
        self.btnFaceRecognition.config(image=self.imgBtn_N3 )      
        self.btnFaceRecognition['font'] = self.myFont
        self.btnFaceRecognition['fg'] = myBtnTxtCol_N
        #4.
        self.imgBtn_N4 = PhotoImage(file= imgPath + "btn_4_enable.png" )
        self.btnCheckAttendance.config(image=self.imgBtn_N4 )      
        self.btnCheckAttendance['font'] = self.myFont
        self.btnCheckAttendance['fg'] = myBtnTxtCol_N
        #5.
        self.imgBtn_N5 = PhotoImage(file= imgPath + "btn_5_enable.png" )
        self.btnEditRecords.config(image=self.imgBtn_N5 )      
        self.btnEditRecords['font'] = self.myFont
        self.btnEditRecords['fg'] = myBtnTxtCol_N
        #6.
        self.imgBtn_N6 = PhotoImage(file= imgPath + "btn_6_enable.png" )
        self.btnRemoveFace_Detection.config(image=self.imgBtn_N6 )      
        self.btnRemoveFace_Detection['font'] = self.myFont
        self.btnRemoveFace_Detection['fg'] = myBtnTxtCol_N
        #7.
        self.imgBtn_N7 = PhotoImage(file= imgPath + "btn_7_enable.png" )
        self.btnAbout.config(image=self.imgBtn_N7 )      
        self.btnAbout['font'] = self.myFont
        self.btnAbout['fg'] = myBtnTxtCol_N

    def StartMongoDB(self):
        # The MongoDB server should be running on your localhost on the same machine that will execute 
        # the Python script for the Kivy application. Use the mongod or mongodb command, in a terminal or 
        # command prompt window, to ensure that the server is running
        # Going into the mongo Shell with mongo will also output the port that the server is running on
        print("Try to start mongod...")
        
        # ## first instance it can enter "mongod" commmand that establishes the mongoserver connection 
        # strBatFilePath = cf.GetStart_MongoDB_BatchFilePath()
        # if( strBatFilePath != '' ):
        #     ##---os.startfile(strBatFilePath)            
        #     subprocess.Popen([ strBatFilePath ], shell=True, creationflags=subprocess.SW_HIDE)
        # else:
        #     msg.showinfo(strObj.strMsgTxt_Title, strObj.strMsgTxt_PlsStartMongoDB_server )
        
        result = mg.StartMyMongoDB()
        if( result == None):
            msg.showinfo(strObj.strMsgTxt_Title, strObj.strMsgTxt_PlsStartMongoDB_server )
        #print(result)
         

    def OpenTrialKeyNagPage(self):
        self.switch_frame( trialNag.My_TrialNag_Page , self.objTkRoot )
    
    # 0. Login Btn
    def onBtnLogin(self):   
        # self.SetNormalButtonState()
        # self.btnLogin['state']="disabled"

        # self.SetNormalImageOnBtns() 
        # self.imgBtn_D = PhotoImage(file= imgPath + "btn_d.png" )
        # self.btnLogin.config(image=self.imgBtn_D , disabledforeground=myBtnTxtCol_Disable ) 
        # self.btnLogin['fg'] = myBtnTxtCol_D
        # self.btnLogin['font'] = self.myFontDisableBtn
        #msg.showinfo("Title 1 ", "Login click")

        self.switch_frame( loginPage.MyLoginPage , self.objTkRoot )
 
    # 1. Add Records Btn
    def onBtnAddRecords(self):
        if(self.btnAddRecords_state == False):
            return

        if(self.bIsRegVersion == False):
            msg.showinfo( strObj.strMsgTxt_TrialVer, strObj.strMsgTxt_TrialVerInfo )
            return 
        if(self.bIsLogInPass):
            if(self.bPlsStopCameraBeforeMoveNextPage):
                # msg.showinfo("Camera", f"Please Stop Camera Before moving to next Tab.")
                msg.showinfo(strObj.strMsgTxt_Title, strObj.strMsgTxt_StopCamera)
            else:
                self.SetNormalButtonState()
                # self.btnAddRecords['state']="disabled"
                self.btnAddRecords_state = False

                self.SetNormalImageOnBtns()
                self.imgBtn_D = PhotoImage(file= imgPath + "btn_1_disable.png" )
                self.btnAddRecords.config(image=self.imgBtn_D , disabledforeground=myBtnTxtCol_Disable, font = self.myFont  ) 
                self.btnAddRecords['fg'] = myBtnTxtCol_D
                self.btnAddRecords['font'] = self.myFont 
                #msg.showinfo("Title 2 ", "Add Records click") myAddRecordsMain
                self.switch_frame( addRecoPage.MyAddRecordPage, self.objTkRoot   )
                ##self.switch_frame( addRecoPage.myAddRecordsMain , self.objTkRoot   )
        else:
            #msg.showinfo("Login", f"Please Login first")
            msg.showinfo( strObj.strMsgTxt_Login, strObj.strMsgTxt_PLFirst)
     
    # 5. Edit Records Btn
    def onBtnEditRecords(self):
        if(self.btnEditRecords_state == False):
            return

        if(self.bIsRegVersion == False):
            msg.showinfo( strObj.strMsgTxt_TrialVer, strObj.strMsgTxt_TrialVerInfo )
            return         
        if(self.bIsLogInPass):
            if(self.bPlsStopCameraBeforeMoveNextPage):
                # msg.showinfo("Camera", f"Please Stop Camera Before moving to next Tab.")
                msg.showinfo(strObj.strMsgTxt_Title, strObj.strMsgTxt_StopCamera)
            else:
                self.SetNormalButtonState()
                # self.btnEditRecords['state']="disabled"
                self.btnEditRecords_state = False

                self.SetNormalImageOnBtns()
                self.imgBtn_D = PhotoImage(file= imgPath + "btn_5_disable.png" )
                self.btnEditRecords.config(image=self.imgBtn_D, disabledforeground=myBtnTxtCol_Disable, font = self.myFont )
                self.btnEditRecords['fg'] = myBtnTxtCol_D
                self.btnEditRecords['font'] = self.myFont
                # msg.showinfo("Title 3 ", "Edit Records click")
                self.switch_frame( editRecoPage.MyEditRecordPage, self.objTkRoot   )
                
                #stop camera
                ##addRecoPage.MyAddRecordPage.onClose()
        else:
            # msg.showinfo("Login", f"Please Login first")
            msg.showinfo( strObj.strMsgTxt_Login, strObj.strMsgTxt_PLFirst)
        
    # 2. Train System Btn
    def onBtnTainSystem(self):
        if(self.btnTainSys_state == False):
            return

        if(self.bIsRegVersion == False):
            msg.showinfo( strObj.strMsgTxt_TrialVer, strObj.strMsgTxt_TrialVerInfo )
            return         
        if(self.bIsLogInPass):
            if(self.bPlsStopCameraBeforeMoveNextPage):
                #msg.showinfo("Camera", f"Please Stop Camera Before moving to next Tab.")
                msg.showinfo(strObj.strMsgTxt_Title, strObj.strMsgTxt_StopCamera)
            else:
                #msg.showinfo("Title 4 ", "Train System click")
                self.SetNormalButtonState()
                #self.btnTainSys['state']="disabled"
                self.btnTainSys_state = False


                self.SetNormalImageOnBtns() 
                self.imgBtn_D = PhotoImage(file= imgPath + "btn_2_disable.png" )
                self.btnTainSys.config(image=self.imgBtn_D , disabledforeground=myBtnTxtCol_Disable, font = self.myFont ) 
                self.btnTainSys['fg'] = myBtnTxtCol_D
                self.btnTainSys['font'] = self.myFont        
                self.switch_frame( trainSys.MyTrainedSystemPage, self.objTkRoot   )
        else:
            #msg.showinfo("Login", f"Please Login first")
            msg.showinfo( strObj.strMsgTxt_Login, strObj.strMsgTxt_PLFirst)

    # 4. Check Attendance Btn
    def onBtnCheckAttendance(self):
        if(self.btnCheckAttendance_state == False):
            return

        if(self.bIsRegVersion == False):
            msg.showinfo( strObj.strMsgTxt_TrialVer, strObj.strMsgTxt_TrialVerInfo )
            return         
        if(self.bIsLogInPass):
            if(self.bPlsStopCameraBeforeMoveNextPage):
                #msg.showinfo("Camera", f"Please Stop Camera Before moving to next Tab.")
                msg.showinfo(strObj.strMsgTxt_Title, strObj.strMsgTxt_StopCamera)
            else:            
                #msg.showinfo("Title 4 ", "onBnCheckAttendance click")
                self.SetNormalButtonState()
                #self.btnCheckAttendance['state']="disabled"
                self.btnCheckAttendance_state = False


                self.SetNormalImageOnBtns() 
                self.imgBtn_D = PhotoImage(file= imgPath + "btn_4_disable.png" )
                self.btnCheckAttendance.config(image=self.imgBtn_D, disabledforeground=myBtnTxtCol_Disable, font = self.myFont  ) 
                self.btnCheckAttendance['fg'] = myBtnTxtCol_D
                self.btnCheckAttendance['font'] = self.myFont
                self.switch_frame( chkAttendance.MyAttendanceSystemPage, self.objTkRoot   )
        else:
            #msg.showinfo("Login", f"Please Login first")
            msg.showinfo( strObj.strMsgTxt_Login, strObj.strMsgTxt_PLFirst)

    # 3. Face Recognition Btn
    def onBtnFaceRecognition(self):
        if(self.btnFaceRecognition_state == False):
            return

        if(self.bIsRegVersion == False):
            msg.showinfo( strObj.strMsgTxt_TrialVer, strObj.strMsgTxt_TrialVerInfo )
            return         
        if(self.bIsLogInPass):
            if(self.bPlsStopCameraBeforeMoveNextPage):
                #msg.showinfo("Camera", f"Please Stop Camera Before moving to next Tab.")
                msg.showinfo(strObj.strMsgTxt_Title, strObj.strMsgTxt_StopCamera)
            else:            
                #msg.showinfo("Title 5 ", "start FaceRecognition click")
                self.SetNormalButtonState()
                #self.btnFaceRecognition['state']="disabled"
                self.btnFaceRecognition_state = False


                self.SetNormalImageOnBtns() 
                self.imgBtn_D = PhotoImage(file= imgPath + "btn_3_disable.png" )
                self.btnFaceRecognition.config(image=self.imgBtn_D, disabledforeground=myBtnTxtCol_Disable, font = self.myFont  ) 
                self.btnFaceRecognition['fg'] = myBtnTxtCol_D
                self.btnFaceRecognition['font'] = self.myFont
                self.switch_frame( faceRecog.MyFaceRecognitionPage, self.objTkRoot   )
        else:
            #msg.showinfo("Login", f"Please Login first")
            msg.showinfo( strObj.strMsgTxt_Login, strObj.strMsgTxt_PLFirst)

    # 6.   
    def onBtnRemoveFace_Detection(self):
        if(self.btnRemoveFace_Detection_state == False):
            return

        if(self.bIsRegVersion == False):
            msg.showinfo( strObj.strMsgTxt_TrialVer, strObj.strMsgTxt_TrialVerInfo )
            return         
        if(self.bIsLogInPass):
            if(self.bPlsStopCameraBeforeMoveNextPage):
                #msg.showinfo("Camera", f"Please Stop Camera Before moving to next Tab.")
                msg.showinfo(strObj.strMsgTxt_Title, strObj.strMsgTxt_StopCamera)
            else:            
                #msg.showinfo("Title 5 ", "start FaceRecognition click")
                self.SetNormalButtonState()
                #self.btnRemoveFace_Detection['state']="disabled"
                self.btnRemoveFace_Detection_state = False


                self.SetNormalImageOnBtns() 
                self.imgBtn_D = PhotoImage(file= imgPath + "btn_6_disable.png" )
                self.btnRemoveFace_Detection.config(image=self.imgBtn_D, disabledforeground=myBtnTxtCol_Disable, font = self.myFont  ) 
                self.btnRemoveFace_Detection['fg'] = myBtnTxtCol_D
                self.btnRemoveFace_Detection['font'] = self.myFont
                self.switch_frame( rFD.RemoveFaceFrom_Detection, self.objTkRoot   )
        else:
            #msg.showinfo("Login", f"Please Login first")
            msg.showinfo( strObj.strMsgTxt_Login, strObj.strMsgTxt_PLFirst)

    # 7. About Btn
    def onBtnAbout(self):
        if(self.btnAbout_state == False):
            return

        if(self.bIsRegVersion == False):
            msg.showinfo( strObj.strMsgTxt_TrialVer, strObj.strMsgTxt_TrialVerInfo )
            return         
        if(self.bIsLogInPass):
            if(self.bPlsStopCameraBeforeMoveNextPage):
                #msg.showinfo("Camera", f"Please Stop Camera Before moving to next Tab.")
                msg.showinfo(strObj.strMsgTxt_Title, strObj.strMsgTxt_StopCamera)
            else:            
                #msg.showinfo("Title 4 ", "About click")
                self.SetNormalButtonState()
                #self.btnAbout['state']="disabled"
                self.btnAbout_state = False
                
                self.SetNormalImageOnBtns() 
                self.imgBtn_D = PhotoImage(file= imgPath + "btn_7_disable.png" )
                self.btnAbout.config(image=self.imgBtn_D, disabledforeground=myBtnTxtCol_Disable, font = self.myFont  ) 
                self.btnAbout['fg'] =  myBtnTxtCol_D
                self.btnAbout['font'] = self.myFont
                
                
                self.switch_frame( abt.MyAboutPage, self.objTkRoot   ) 

                # to update status bar at bottom of application
                #self.upload()
        else:
            #msg.showinfo("Login", f"Please Login first")
            msg.showinfo( strObj.strMsgTxt_Login, strObj.strMsgTxt_PLFirst)

 
###-------------------------------------------
FILE_NAME = 'PageHome.py'
# import win32event
# import win32api
# from winerror import ERROR_ALREADY_EXISTS

# def CheckMutex():
#     mutex = win32event.CreateMutex(None, False, 'name')
#     last_error = win32api.GetLastError()

#     if last_error == ERROR_ALREADY_EXISTS:
#        print("App instance already running")

###-------------------------------------------
from MyMutexClass import singleinstance
from sys import exit

def main():

    # beginnig of our application
    myapp = singleinstance()
    # check is another instance of same program running
    if myapp.aleradyrunning():
        # print("Another instance of this program is already running")
        ## msg.showinfo(strObj.strMsgTxt_Title, strObj.strMsgTxt_AlreadyRun )
        exit(0)

    # not running, safe to continue...
    print("No another instance is running, can continue here")


    #root = Tk()
    #MyHomePage(root)

    ##CheckMutex()
    
    root = MyHomePage()
 
    root.mainloop()
    print("Bye....")
    print("Try to Stop mongod server...")

    ####mg.StopMyMongoDB()

    strBatFilePath = cf.GetStop_MongoDB_BatchFilePath()
    if( strBatFilePath != '' ):
        ##---os.startfile(strBatFilePath)            
        subprocess.Popen([ strBatFilePath ], shell=True, creationflags=subprocess.SW_HIDE)
        print("mongod server is stopped")




if __name__ == "__main__" :
    main()

