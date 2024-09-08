from tkinter import *
from AllStrings import myStrings
import common_fun as cf 
import tkinter.messagebox as msg
import time
import tkinter.font as font 
import tkinter as tk
#from Mongo_DB import MyMongoDB
import datetime
import json
import os 
from datetime import *
import objcrypt
import requests
##from BeautifulSoup import BeautifulSoup
# from bs4 import BeautifulSoup
from requests.exceptions import HTTPError


myAppBGColor =  "lavender blush" # "white smoke" # "grey" 
myFont = "Helvetica"
myHeadingTxtFontSize = 15
myTxtFontSize = 10
myTxtColor = "black" # "white"
myBtnBGColor= "lavender blush" #  "white smoke" # "Green"
myBorderColor = "medium violet red"
myBtnTxtColor = "white"

strObj  = myStrings()


class My_TrialNag_Page(tk.Frame):

    def __del__(self):
        #msg.showinfo("Title 1 ", "Login close destroy....") 
        print("Bye My_TrialNag_Page-1-1")

    def __init__(self, master, Parent=None):
        print("Hi My_TrialNag_Page-1-1")

        #self._frame = None
        tk.Frame.__init__(self, master)

        #self._frame = master
        self.myroot = master
        self.myParent = Parent

        self.myParent.bIsRegVersion = False

        # strkey_salt = "AjaySharma"
        # # using join() + bytearray() + format()  Converting String to binary 
        # self.my_key_salt = ''.join(format(i, 'b') for i in bytearray( strkey_salt, encoding ='utf-8')) 
        ##self.my_key_salt = "AjaySharma"

        # define font - weight − "bold" for boldface, "normal" for regular weight
        #self.myFont = font.Font(family='Helvetica', size=13, weight='normal')

        self.frame = tk.Frame(master, width=385, height=460, borderwidth=0, bg= myAppBGColor, relief=SUNKEN   )
        ####self.frame.pack(side = LEFT, anchor = "nw", fill=Y, expand=YES)
        self.frame.place(x=200-4, y=1, anchor="nw", width=758+6, height=621-1)
 
        self.CreatePageTrialNagGUI()

    

    def CreatePageTrialNagGUI(self):
        self.myroot.grid_columnconfigure((0,1), weight=1)

        global my_key
        my_key = StringVar()
        
        # Update this URL to ORIGINAL Url
        self.strMyWebServeUrl = cf.URL_TO_VERIFY_KEY  
        
        # create a Form Heading label 
        xLblVal = 80
        yVal = 32
        ctrlHeight = 3
        ctrlWidth = 80

        # Heading...
        self.heading = Label(self.frame, text=strObj.strHeadingPageTrialNag, fg=myTxtColor, bg=myAppBGColor, font=(myFont, myHeadingTxtFontSize), compound="left" , justify=LEFT, anchor=W )
        self.heading.configure(height=ctrlHeight, width=ctrlWidth)
        self.heading.place(x=xLblVal,y=32)  #.pack(expand=YES, fill=BOTH)     

        # Sub - Heading...
        self.Subheading = Label(self.frame, text=strObj.strSubHeadingPageTrialNag, fg=myTxtColor, bg=myAppBGColor, font=(myFont, myTxtFontSize), justify=LEFT, anchor=W )
        self.Subheading.configure(height=ctrlHeight, width=ctrlWidth)
        self.Subheading.place(x=xLblVal,y=100) 
    
        yVal += 85 + 30 + 64
        xEdtVal = 230
        ctrlHeight = 1 
        ctrlWidth = 20       

        self.myKey = Label(self.frame, text=strObj.strEnterValidKey, fg=myTxtColor, bg=myAppBGColor, font=(myFont, myTxtFontSize), justify=LEFT, anchor=W)
        self.myKey.configure(height=ctrlHeight, width=ctrlWidth-3)
        self.myKey.place(x=xLblVal,y=yVal) 

        self.Key_field = Entry(self.frame, width=ctrlWidth+20, textvariable=my_key  , highlightbackground=myBorderColor, highlightcolor=myBorderColor, highlightthickness=1 , bd= 0 )
        self.Key_field.place(x=xEdtVal, y=yVal) 
        yVal += 35
        
        # Button Reset
        yBtnVal = 305 + 270 

        # rounded_btn_dark.png
        imgPath = cf.GetAppImageDirPath()
        btnImg_N2 = imgPath + "rounded_btn.png"
        self.img_N2=PhotoImage(file=btnImg_N2 ) 
        ctrlHeight = 36
        ctrlWidth = 180
        xbtnVal = 545   
        self.btnVerifyKey = Button(self.frame, image=self.img_N2, text= strObj.strBtnVerifyKey, command=self.onBtnClickVerifyKey , justify = RIGHT, fg=myBtnTxtColor, font=(myFont, myTxtFontSize) , bg=myBtnBGColor  , border=0,   highlightthickness = 0, borderwidth = 0)
        self.btnVerifyKey.configure(height=ctrlHeight, width=ctrlWidth, compound=CENTER)
        self.btnVerifyKey.place(x=xbtnVal, y=yBtnVal) 

    def CloseTrialNagPage(self):
        # open Login Page
        print("Bye My_TrialNag_Page-1-1")
        self.frame.destroy()
        self.myParent.onBtnLogin()
    
    '''
    def VerifyKeyOnOur_WebServer(self, strKey):
        # now_dd, now_mm, now_yy = datetime.now().strftime("%d-%m-%Y").split('-')
        # now_date_Info = date( int(now_yy), int(now_mm), int(now_dd) )
        
        # 0. SEND following information to our web server
        send_info_to_server = dict()
        myMacID = cf.GetMachineUniqueID()
        send_info_to_server = {  
                    'key' : strKey, 
                    ##'current_date': now_date_Info, 
                    'mac_id' : myMacID
                }
        ###send_info_to_server = {'username':'Ajay','password':'ajay123'}
        ##--ajay----my_response = requests.post( self.strMyWebServeUrl, data = send_info_to_server)
        
        ## just to check------------------------------------------------------
        my_response = None
        try:
            sUrl =  self.strMyWebServeUrl   +  strKey  + "/"
            ##---headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
            ##---my_response = requests.get(url=sUrl, params=send_info_to_server, headers=headers)
            my_response = requests.get( sUrl, data = send_info_to_server)
            
            print( my_response.status_code )
            my_response.raise_for_status()
            # access JSOn content
            jsonResponse = my_response.json()
            print(jsonResponse)
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
            msg.showinfo( strObj.strMsgTxt_TrialVer, strObj.strEnterValidKey )
            return
        except Exception as err:
            print(f'Other error occurred: {err}')
            msg.showinfo( strObj.strMsgTxt_TrialVer, strObj.strFailedCon  )
            return
        ##--------------------------------------------------------------------

        ###soup = BeautifulSoup(my_response.content)
        ## The result obtained from the above code is Python dictionary and is also in 'key-value'
        my_response_dictionary = my_response.json()
        print( my_response_dictionary )
        print(f" Final Status ==>{ my_response_dictionary['app_final_status'] } " )

        ##-----Get Response from WEB Server with following info--------------------------------server_response_
        # 1. verify key on our web server and Return True/ False according to key_DB
        # 2. and also return Expire Date in formate as "09-07-2020" 
        if( 1 == my_response_dictionary['app_final_status'] ):
            server_response_bIsKeyVerify = True   
        else:
            server_response_bIsKeyVerify = False
        server_response_Key = str(strKey)
        server_response_ExpireDate = my_response_dictionary['expire_date'] ## str("30-09-2020") ## "10-08-2020"
        server_response_allow_total_emp_count = my_response_dictionary['allow_emp_count'] ## str('10')
        server_response_machine_id = my_response_dictionary['mac_id'] ##  str("A63E11FF-7D9D-11E3-9DE6-618FE803C0FF")
        server_response_msg = my_response_dictionary['show_msg'] ## 'msg'


        server_response_data = dict()
        server_response_data['key']  = str(server_response_Key)
        server_response_data['key2'] = str(server_response_ExpireDate)
        server_response_data['key3'] = str(server_response_allow_total_emp_count)
        server_response_data['key4'] = str(server_response_machine_id)
        server_response_data['key5'] = str(server_response_msg)
        ##-------------------------------------------------------------------------------------

        #3. Retuen both variables to set Aplication State
        return server_response_bIsKeyVerify, server_response_data  
    '''

    def onBtnClickVerifyKey(self):
        strKeyDirPath = cf.GetKeyDirPath()
        keyfilePath =  strKeyDirPath + "key.key"

        key = my_key.get()     
        key = key.strip()  
        if(key == ''):
            msg.showinfo( strObj.strMsgTxt_TrialVer, strObj.strMsgTxt_KeyNotEmpty )
            return

        bIsKeyOk,  server_response_data = cf.VerifyKeyOnOur_WebServer(key)  
        ExpireDate = server_response_data['key2']
        if(bIsKeyOk):
            # format on server is "%Y-%m-%d"
            exp_yy, exp_mm, exp_dd  = ExpireDate.split('-')
            ExpireDate_Info = date( int(exp_yy), int(exp_mm), int(exp_dd) )
            expire_date_to_show =   f"{exp_dd}-{exp_mm}-{exp_yy}"

            now_dd, now_mm, now_yy = datetime.now().strftime("%d-%m-%Y").split('-')
            NowDate_Info = date( int(now_yy), int(now_mm), int(now_dd) )
            # Check the dates 
            if ExpireDate_Info == NowDate_Info: 
                print("Both are equal...so run application") 
                self.myParent.bIsRegVersion = True                
            elif ExpireDate_Info < NowDate_Info: 
                print("Trial expired...never run the application...")  
                self.myParent.bIsRegVersion = False
                msg.showinfo( strObj.strMsgTxt_TrialVer, strObj.strMsgTxt_KeyExpire )
                self.myParent.statusvar.set(f"Product Key is expired on: {expire_date_to_show}")
                return               
            else: 
                print("run application...") 
                self.myParent.bIsRegVersion = True
            # 1. write key and date in Original file "key.key" 
            # save data { 'key' : key, 'ExpireDate' : ExpireDate}
            ###file_data = { 'key' : key, 'key2' : ExpireDate, 'key3': machine_id }
            ###-------------------------------
            ## Create 'key.key' and store all info. in which was get from server
            cf.Encrypt_Data(keyfilePath, server_response_data)
            ###------------------------------
            self.myParent.statusvar.set(f"Product Key is expire on: {expire_date_to_show}")
            self.CloseTrialNagPage()
        else:
            ## invalid key
            # 'key':'User Crossed the maximum limit of key uses'
            # 'key2':'0'
            msgFrmServer = server_response_data['key']
            print("Pls enter correct key...")
            self.myParent.bIsRegVersion = False
            msg.showinfo( strObj.strMsgTxt_TrialVer, msgFrmServer ) # strObj.strMsgTxt_EnterKey
                    
        # else:
        #     ## key is not verify 
        #     ## check available key file
        #     if os.path.exists(keyfilePath): ## Ajay
        #         ##Read file to decrypt
        #         file_data = self.Decrypt_Data(keyfilePath) 
        #         my_dbkey = file_data['key']
        #         exp_date = file_data['key2']

        #         exp_dd, exp_mm, exp_yy = exp_date.split('-')
        #         ExpireDate_Info = date( int(exp_yy), int(exp_mm), int(exp_dd) )

        #         now_dd, now_mm, now_yy = datetime.now().strftime("%d-%m-%Y").split('-')
        #         NowDate_Info = date( int(now_yy), int(now_mm), int(now_dd) )
        #         # Check the dates 
        #         if ExpireDate_Info == NowDate_Info: 
        #             if( my_dbkey.lower() ==  key.lower() ):
        #                 print("Both are equal...so run application") 
        #                 self.myParent.bIsRegVersion = True 
        #             else:
        #                 print("Pls enter correct key...") 
        #                 self.myParent.bIsRegVersion = False
        #                 msg.showinfo( strObj.strMsgTxt_TrialVer, strObj.strMsgTxt_EnterKey )
        #                 return              
        #         elif ExpireDate_Info < NowDate_Info: 
        #             print("Trial expired...never run the application...") 
        #             self.myParent.bIsRegVersion = False 
        #             msg.showinfo( strObj.strMsgTxt_TrialVer, strObj.strMsgTxt_KeyExpire )
        #             return               
        #         else: 
        #             print("run application...") 
        #             self.myParent.bIsRegVersion = True

        #     else:
        #         print("Pls enter correct key...")
        #         self.myParent.bIsRegVersion = False
        #         msg.showinfo( strObj.strMsgTxt_TrialVer, strObj.strMsgTxt_EnterKey )

    # def Encrypt_Data(self, keyfilePath, file_data):
    #     crypter = objcrypt.Crypter('key', 'cbc')
    #     # encrypte now
    #     encrypted_dict = crypter.encrypt_object(file_data)
    #     with open(keyfilePath, 'w') as outfile:
    #         json.dump(encrypted_dict, outfile)
    #     print("Encrypt_Data done") 

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


def myVerifyKeyMain(root):    
    My_TrialNag_Page(root)
 

if __name__ == "__main__" :
    root = Tk()
    root.geometry("960x640")
    root.title( "strApptitle" )     
    root.resizable(False, False)
    root.configure(background="pink" )

    myVerifyKeyMain(root)     

    root.mainloop()

