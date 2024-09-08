from tkinter import *
from AllStrings import myStrings
import common_fun as cf 
import tkinter.messagebox as msg
import time
import tkinter.font as font
 
import tkinter as tk
from Mongo_DB import MyMongoDB

import smtplib, ssl
# Here are the email package modules we'll need
from email.message import EmailMessage
import urllib
from urllib.request import urlopen
import requests



myAppBGColor =  "lavender blush" #  "white smoke" # "grey" 
myFont = "Helvetica"
myHeadingTxtFontSize = 15
myTxtFontSize = 10
myTxtColor = "black" # "white"
myBtnBGColor= "lavender blush" # "white smoke" # "Green"
myBorderColor = "medium violet red"
myBtnTxtColor = "white"

strObj  = myStrings()

class MyForgotPWPage(tk.Frame):

    def __del__(self):
        #msg.showinfo("Title 1 ", "Login close destroy....") 
        print("Bye MyForgotPWPage-1-1")

    def __init__(self, master, Parent=None):
        print("Hi MyForgotPWPage-1-1")

        #self._frame = None
        tk.Frame.__init__(self, master)

        #self._frame = master
        self.myroot = master
        self.myParent = Parent

        # define font - weight − "bold" for boldface, "normal" for regular weight
        #self.myFont = font.Font(family='Helvetica', size=13, weight='normal')

        self.frame = tk.Frame(master, width=385, height=460, borderwidth=0, bg= myAppBGColor, relief=SUNKEN   )
        ####self.frame.pack(side = LEFT, anchor = "nw", fill=Y, expand=YES)
        self.frame.place(x=200-4, y=1, anchor="nw", width=758+6, height=621-1)
 
        self.CreateForgotPWPageGUI()

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

    def CreateForgotPWPageGUI(self):
        self.myroot.grid_columnconfigure((0,1), weight=1)

        global email_address
        email_address = StringVar()
        
        # create a Form Heading label 
        xLblVal = 80
        yVal = 32
        ctrlHeight = 3
        ctrlWidth = 80

        # Heading...
        self.heading = Label(self.frame, text=strObj.strReSetPW, fg=myTxtColor, bg=myAppBGColor, font=(myFont, myHeadingTxtFontSize), compound="left" , justify=LEFT, anchor=W )
        self.heading.configure(height=ctrlHeight, width=ctrlWidth)
        self.heading.place(x=xLblVal,y=32)  #.pack(expand=YES, fill=BOTH)     

        # Sub - Heading...
        self.Subheading = Label(self.frame, text=strObj.strSubHReSetPW, fg=myTxtColor, bg=myAppBGColor, font=(myFont, myTxtFontSize), justify=LEFT, anchor=W )
        self.Subheading.configure(height=ctrlHeight, width=ctrlWidth)
        self.Subheading.place(x=xLblVal,y=100) 

    
        # create a Form Heading label 
        xLblVal = 80
        yVal += 85 + 30 + 64
        ctrlHeight = 3
        ctrlWidth = 80

        # 1. Row 1 -Email
        self.userOldPW = Label(self.frame, text=strObj.strEmail , fg=myTxtColor, bg=myAppBGColor, font=(myFont, myTxtFontSize), justify=LEFT, anchor=W)
        self.userOldPW.configure(height=ctrlHeight, width=ctrlWidth)
        self.userOldPW.place(x=xLblVal,y=yVal-15) 

        
        xEdtVal = 230
        ctrlHeight = 1 
        ctrlWidth = 20   

        self.email_field = Entry(self.frame, width=ctrlWidth+20, textvariable=email_address , highlightbackground=myBorderColor, highlightcolor=myBorderColor, highlightthickness=1 , bd= 0 ) 
        self.email_field.place(x=xEdtVal, y=yVal) 
        yVal += 35
        

        # Button Reset
        yBtnVal = 305 + 270

        # rounded_btn_dark.png
        imgPath = cf.GetAppImageDirPath()
        btnImg_N1 = imgPath + "rounded_btn_dark.png"
        self.img_N1=PhotoImage(file=btnImg_N1 )         
        ctrlHeight = 36
        ctrlWidth = 180
        xbtnVal = 345
        self.btnCancel_btn = Button(self.frame , image=self.img_N1, text=strObj.strBtnCancel, command=self.onBtnClickCancel , justify = RIGHT, fg=myBtnTxtColor, font=(myFont, myTxtFontSize) , bg=myBtnBGColor  , border=0,   highlightthickness = 0, borderwidth = 0 )
        self.btnCancel_btn.configure(height=ctrlHeight, width=ctrlWidth , compound=CENTER)
        self.btnCancel_btn.place(x=xbtnVal, y=yBtnVal)

        btnImg_N2 = imgPath + "rounded_btn.png"
        self.img_N2=PhotoImage(file=btnImg_N2 ) 

        xbtnVal = 545
        self.btnSendMail_btn = Button(self.frame  , image=self.img_N2, text= strObj.strBtnSendmail, command=self.onBtnClickSendmail , justify = RIGHT, fg=myBtnTxtColor, font=(myFont, myTxtFontSize) , bg=myBtnBGColor , border=0,   highlightthickness = 0, borderwidth = 0 )
        self.btnSendMail_btn.configure(height=ctrlHeight, width=ctrlWidth, compound=CENTER)
        self.btnSendMail_btn.place(x=xbtnVal, y=yBtnVal) 
   
  

    def onBtnClickCancel(self):
        # open Login Page
        print("Bye MyForgotPWPage-1-1")
        self.frame.destroy()

    def onBtnClickSendmail(self):
        email = email_address.get()     
        email = email.strip()   

        # get saved user and PW from DB
        objDB = MyMongoDB()
        mydataList = objDB.GetUserName_PW()
        db_email = ""

        if(email == ""):
            #msg.showinfo("Email", "User email cannot be empty.")
            msg.showinfo(strObj.strEmail, strObj.strUsrEmailNotEpty) 
            return
        elif( ( self.valideEmail(email) )        ):

            if( len(mydataList) > 0 ):
                user_db =  mydataList[0]   
                pw_db = mydataList[1] 
                db_email = mydataList[2] 
            else:
                msg.showerror(strObj.strMsgCommonTitle, strObj.strMsgRegBeforeUpdate)
                return

            if( email == db_email ) :
                # 1. sending the email 
                if( self.Is_InternetWork() ):
                    bRes = self.SentMailForUserName_PW(db_email, user_db, pw_db) 
                    if(bRes):
                        #msg.showinfo("Email", f"Mail has been sent, please check your email account")
                        msg.showinfo(strObj.strEmail, strObj.strMailSend)
                    else:
                        msg.showinfo(strObj.strEmail, strObj.strErrorSendingMail )
                else:
                    msg.showinfo(strObj.strEmail, strObj.strCheckYourNetConnection)
                    return
            else:
                msg.showerror(strObj.strMsgCommonTitle, strObj.strEmailNotMatch)
                return

            # 2. open Login page
            # this will delete the entry after reset button is pressed
            self.email_field.delete(0, END)
            self.onBtnClickCancel()

        else:
            #msg.showinfo("Invalid Email", f"Invalid Email, cross-check once again")
            msg.showinfo(strObj.strEmail, strObj.strInvalidEmail)

            # this will delete the entry after reset button is pressed
            self.email_field.delete(0, END)

    # ---------------------------EMail--------------------------------------------
    def Is_InternetWork(self):
        try:
            url='http://google.com'
            timeout=1
            urlopen(url, timeout=timeout)
            return True
        except urllib.error.URLError as er:
            print(er)
            return False

    def SentMailForUserName_PW(self, email, username, uerpw):
        print(f"mail = {email} and username = {username}, password = {uerpw}")

        port = 465
        smtp_server = "mail.vervelogic.a2hosted.com"
        sender_email = "info@vervelogic.a2hosted.com"
        receiver_email = email
        password = "j}@R}R5)qc@-"  # paste your password generated by Mail trap
        cc = ['info@vervelogic.a2hosted.com']
        bcc = [sender_email, 'ajayjpr.2010@gmail.com']
        rcpt = [email] + cc + bcc
        # type your message: use two newlines (\n) to separate the subject from the message body, and use 'f' to
        # automatically insert variables in the text
        message = EmailMessage()
        message['From'] = f"{sender_email}"
        message['To'] = receiver_email
        message['Subject'] = f"Hello {username}"
        message.set_content(f"""\
            Hello {username},
        
            It seems you have forgotten your Face Recognition application password.

            Please find the following credentials to run the application smoothly.
                    
            user name : {username}
            password  : {uerpw}
            
            please don't reply this email directly as it was sent automatically
        
            Best regard,
            Team.
        """)

        # print(f"Your mag \n{message}")
        try:
            # send your message with credentials specified above
            '''
            with smtplib.SMTP(smtp_server, port) as server:
                server.login(login, password)
                server.sendmail(sender, receiver_email, message)
            '''
            # Create a secure SSL context
            context = ssl.create_default_context()
            # with smtplib.SMTP(smtp_server, port) as server:
            with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                print(f"Check Login for {sender_email}")
                server.login(sender_email, password)
                print(f"Try to sent mail...")
                server.sendmail(sender_email, rcpt, message.as_string())
                print('Successfully sent email')
                return True
        # except (gaierror, ConnectionRefusedError):
        #     print('Failed to connect to the server. Bad connection settings?')
        except smtplib.SMTPServerDisconnected:
            print('Failed to connect to the server. Wrong user/password?')
            return False
        except smtplib.SMTPException as e:
            print('SMTP error occurred: ' + str(e))
            return False
        # finally:
        #    server.quit()
    # ---------------------------EMail------------------------------------------

    


def myForgotPWMain(root):    
    MyForgotPWPage(root)
 

if __name__ == "__main__" :
    root = Tk()
    root.geometry("960x640")
    root.title( "strApptitle" )     
    root.resizable(False, False)
    root.configure(background="pink" )

    myForgotPWMain(root)     

    root.mainloop()

