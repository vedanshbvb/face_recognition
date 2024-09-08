from tkinter import *
from AllStrings import myStrings
import common_fun as cf 
import tkinter.messagebox as msg
import time
import tkinter.font as font
 
import tkinter as tk
from Mongo_DB import MyMongoDB

 
myAppBGColor =  "lavender blush" # "white smoke" # "grey" 
myFont = "Helvetica"
myHeadingTxtFontSize = 15
myTxtFontSize = 10
myTxtColor = "black" # "white"
myBtnBGColor= "lavender blush" # "white smoke" # "Green"
myBorderColor = "medium violet red"
myBtnTxtColor = "white"


strObj  = myStrings()


class MyChangePWPage(tk.Frame):

    def __del__(self):
        #msg.showinfo("Title 1 ", "Login close destroy....") 
        print("Bye MyChangePWPage-1-2")

    def __init__(self, master, Parent=None):
        print("Hi MyChangePWPage-1-2")

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
 
        self.CreateChangePWPageGUI()


    def CreateChangePWPageGUI(self):
        self.myroot.grid_columnconfigure((0,1), weight=1)

        global oldPassword_verify
        global newPassword_verify
        global confirmNewPassword_verify

        oldPassword_verify = StringVar()
        newPassword_verify = StringVar()
        confirmNewPassword_verify = StringVar()

        
        # create a Form Heading label 
        xLblVal = 80
        yVal = 32
        ctrlHeight = 3
        ctrlWidth = 80

        # Heading...
        self.heading = Label(self.frame, text= strObj.strPHeading, fg=myTxtColor, bg=myAppBGColor, font=(myFont, myHeadingTxtFontSize), compound="left", justify=LEFT, anchor=W )
        self.heading.configure(height=ctrlHeight, width=ctrlWidth)
        self.heading.place(x=xLblVal,y=32)  #.pack(expand=YES, fill=BOTH)     

        # Sub - Heading...
        self.Subheading = Label(self.frame, text= strObj.strPSubHeading, fg=myTxtColor, bg=myAppBGColor, font=(myFont, myTxtFontSize), justify=LEFT, anchor=W )
        self.Subheading.configure(height=ctrlHeight, width=ctrlWidth)
        self.Subheading.place(x=xLblVal,y=100) 

    
        yVal += 85 + 30 + 64
        xEdtVal = 230
        ctrlHeight = 1 
        ctrlWidth = 20       

        # 1. Row 1 - Old Password
        self.userOldPW = Label(self.frame, text=strObj.strOldPW , fg=myTxtColor, bg=myAppBGColor, font=(myFont, myTxtFontSize), justify=LEFT, anchor=W)
        self.userOldPW.configure(height=ctrlHeight, width=ctrlWidth)
        self.userOldPW.place(x=xLblVal,y=yVal) 

        self.userOldPW_field = Entry(self.frame, width=ctrlWidth+20, textvariable=oldPassword_verify , highlightbackground=myBorderColor, highlightcolor=myBorderColor, highlightthickness=1 , bd= 0 )
        self.userOldPW_field.place(x=xEdtVal, y=yVal) 
        #self.userName_field.bind("<Return>", self.empid_focus)
        yVal += 35
 
        # 2. Row 2 - New Password
        self.NewPassword = Label(self.frame, text=strObj.strNewPW, fg=myTxtColor, bg=myAppBGColor, font=(myFont, myTxtFontSize), justify=LEFT, anchor=W)  
        self.NewPassword.configure(height=ctrlHeight, width=ctrlWidth)
        self.NewPassword.place(x=xLblVal,y=yVal) 

        self.NewPassword_field = Entry(self.frame, width=ctrlWidth+20, textvariable=newPassword_verify, show= '*' , highlightbackground=myBorderColor, highlightcolor=myBorderColor, highlightthickness=1 , bd= 0 )
        self.NewPassword_field.place(x=xEdtVal, y=yVal)
        #self.Password_field.bind("<Return>", self.name_focus)        
        yVal += 35

        # 3. Row 3 - Confirm New Password
        self.ConfirmNewPassword = Label(self.frame, text=strObj.strConfirmPW , fg=myTxtColor, bg=myAppBGColor, font=(myFont, myTxtFontSize), justify=LEFT, anchor=W)  
        self.ConfirmNewPassword.configure(height=ctrlHeight, width=ctrlWidth)
        self.ConfirmNewPassword.place(x=xLblVal,y=yVal) 

        self.ConfirmNewPassword_field = Entry(self.frame, width=ctrlWidth+20, textvariable=confirmNewPassword_verify, show= '*' , highlightbackground=myBorderColor, highlightcolor=myBorderColor, highlightthickness=1 , bd= 0 )
        self.ConfirmNewPassword_field.place(x=xEdtVal, y=yVal)
        #self.Password_field.bind("<Return>", self.name_focus)        
        
        

        # Button
        yBtnVal = 305 + 270

        # rounded_btn_dark.png
        imgPath = cf.GetAppImageDirPath()
        btnImg_N1 = imgPath + "rounded_btn_dark.png"
        self.img_N1=PhotoImage(file=btnImg_N1 )         
        ctrlHeight = 36
        ctrlWidth = 180
        xbtnVal = 345
        self.btnCancel_btn = Button(self.frame , image=self.img_N1 , text=strObj.strBtnCancel, command=self.onBtnClickCancel, justify = RIGHT, fg=myBtnTxtColor, font=(myFont, myTxtFontSize) , bg=myBtnBGColor , border=0,   highlightthickness = 0, borderwidth = 0 )
        self.btnCancel_btn.configure(height=ctrlHeight, width=ctrlWidth , compound=CENTER)
        self.btnCancel_btn.place(x=xbtnVal, y=yBtnVal)

        btnImg_N2 = imgPath + "rounded_btn.png"
        self.img_N2=PhotoImage(file=btnImg_N2 ) 

        xbtnVal = 545
        self.btnChangePW_btn = Button(self.frame , image=self.img_N2 , text= strObj.strBtn1ChangePW , command=self.onBtnClickChangePW, justify = RIGHT, fg=myBtnTxtColor, font=(myFont, myTxtFontSize) , bg=myBtnBGColor , border=0,   highlightthickness = 0, borderwidth = 0)
        self.btnChangePW_btn.configure(height=ctrlHeight, width=ctrlWidth , compound=CENTER)
        self.btnChangePW_btn.place(x=xbtnVal, y=yBtnVal) 
   
    def onBtnClickChangePW(self):
        oldPW = oldPassword_verify.get()
        newPW = newPassword_verify.get()
        CnewPW = confirmNewPassword_verify.get()

        oldPW = oldPW.strip()
        newPW = newPW.strip()
        CnewPW = CnewPW.strip()

        # get saved user and PW from DB
        objDB = MyMongoDB()
        mydataList = objDB.GetUserName_PW()
        pw_db = ""
        if( len(mydataList) > 0 ):
            user_db =  mydataList[0]   
            pw_db = mydataList[1] 
            db_email = mydataList[2] 
        else:
            msg.showerror(strObj.strMsgCommonTitle,  strObj.strMsgRegBeforeUpdate)
            return

        # get old PW from DB
        oldPW_DB = pw_db ####"admin"

        if( ( oldPW == "") or (newPW == "") or ( CnewPW == "") ):
            msg.showinfo( strObj.strPageLogin,  strObj.strBlank )
        elif( oldPW ==  oldPW_DB ):
            # save new pw
            if( newPW == CnewPW ):
                # save new pw in DB
                objDB.UpdateUserPasswordInDB(oldPW, CnewPW )
                #msg.showinfo("Password", "Password has been modifying successfully!!!")
                msg.showinfo(strObj.strPageLogin, strObj.strPWUpdate)

                # this will delete the entry after button is pressed
                self.userOldPW_field.delete(0, END)
                self.NewPassword_field.delete(0, END)
                self.ConfirmNewPassword_field.delete(0, END)

                self.onBtnClickCancel()
            else:
                # msg.showinfo("Password", "Confirmed password and new password both are different")
                msg.showinfo(strObj.strPageLogin, strObj.strDiffPW )
        else:
            #msg.showinfo("Password", "Your Old password not match")
            msg.showinfo(strObj.strPageLogin, strObj.strOldPWNotMatch)

            # this will delete the entry after button is pressed
            self.userOldPW_field.delete(0, END)
            self.NewPassword_field.delete(0, END)
            self.ConfirmNewPassword_field.delete(0, END)


    def onBtnClickCancel(self):
        # open Login Page
        print("Bye MyChangePWPage-1-2")
        self.frame.destroy()

   


def myChangePWPageMain(root):    
    MyChangePWPage(root)
 

if __name__ == "__main__" :
    root = Tk()
    root.geometry("960x640")
    root.title( "strApptitle" )     
    root.resizable(False, False)
    root.configure(background="pink" )

    myChangePWPageMain(root)     

    root.mainloop()

