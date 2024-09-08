
from tkinter import *
from AllStrings import myStrings
import common_fun as cf 
import tkinter.messagebox as msg
import time
import tkinter.font as font
 
import tkinter as tk
from Mongo_DB import MyMongoDB
 
myAppBGColor =  "lavender blush" #  "grey" 
myFont = "Helvetica"
myHeadingTxtFontSize = 15
myTxtFontSize = 10
myTxtColor = "black" # "white"
myBtnBGColor="lavender blush" # "white smoke" #  "Green"
myBorderColor = "medium violet red"
myBtnTxtColor = "white"


strObj  = myStrings()


class MyRegisterNewUserPage(tk.Frame):

    def __del__(self):
        #msg.showinfo("Title 1 ", "Login close destroy....") 
        print("Bye MyRegisterNewUserPage-1-2")

    def __init__(self, master, Parent=None):
        print("Hi MyRegisterNewUserPage-1-2")

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
 
        self.CreateRegisterNewUserPageGUI()


    def CreateRegisterNewUserPageGUI(self):
        self.myroot.grid_columnconfigure((0,1), weight=1)

        global userName_verify
        global Password_verify
        global confirmPassword_verify
        global email_verify

        userName_verify = StringVar()
        Password_verify = StringVar()
        confirmPassword_verify = StringVar()
        email_verify =  StringVar()

        
        # create a Form Heading label 
        xLblVal = 80
        yVal = 32
        ctrlHeight = 3
        ctrlWidth = 80

        # Heading...
        self.heading = Label(self.frame, text= strObj.strPRegNewUserHeading, fg=myTxtColor, bg=myAppBGColor, font=(myFont, myHeadingTxtFontSize), compound="left", justify=LEFT, anchor=W )
        self.heading.configure(height=ctrlHeight, width=ctrlWidth)
        self.heading.place(x=xLblVal,y=32)  #.pack(expand=YES, fill=BOTH)     

        # Sub - Heading...
        self.Subheading = Label(self.frame, text= strObj.strPRegNewUserSubHeading, fg=myTxtColor, bg=myAppBGColor, font=(myFont, myTxtFontSize), justify=LEFT, anchor=W )
        self.Subheading.configure(height=ctrlHeight, width=ctrlWidth)
        self.Subheading.place(x=xLblVal,y=100) 

    
        yVal += 85 + 30 + 64
        xEdtVal = 230
        ctrlHeight = 1 
        ctrlWidth = 20       

        # 1. Row 1 - User Name
        self.userName = Label(self.frame, text=strObj.strUserName , fg=myTxtColor, bg=myAppBGColor, font=(myFont, myTxtFontSize), justify=LEFT, anchor=W)
        self.userName.configure(height=ctrlHeight, width=ctrlWidth)
        self.userName.place(x=xLblVal,y=yVal) 

        self.userName_field = Entry(self.frame, width=ctrlWidth+20, textvariable=userName_verify , highlightbackground=myBorderColor, highlightcolor=myBorderColor, highlightthickness=1 , bd= 0 )
        self.userName_field.place(x=xEdtVal, y=yVal) 
        #self.userName_field.bind("<Return>", self.empid_focus)
        yVal += 35
 
        # 2. Row 2 - Password
        self.Password = Label(self.frame, text=strObj.strPW, fg=myTxtColor, bg=myAppBGColor, font=(myFont, myTxtFontSize), justify=LEFT, anchor=W)  
        self.Password.configure(height=ctrlHeight, width=ctrlWidth)
        self.Password.place(x=xLblVal,y=yVal) 

        self.Password_field = Entry(self.frame, width=ctrlWidth+20, textvariable=Password_verify, show= '*' , highlightbackground=myBorderColor, highlightcolor=myBorderColor, highlightthickness=1 , bd= 0 )
        self.Password_field.place(x=xEdtVal, y=yVal)
        #self.Password_field.bind("<Return>", self.name_focus)        
        yVal += 35

        # 3. Row 3 - Confirm Password
        self.ConfirmPassword = Label(self.frame, text=strObj.strConfirmMyPW , fg=myTxtColor, bg=myAppBGColor, font=(myFont, myTxtFontSize), justify=LEFT, anchor=W)  
        self.ConfirmPassword.configure(height=ctrlHeight, width=ctrlWidth)
        self.ConfirmPassword.place(x=xLblVal,y=yVal) 

        self.ConfirmPassword_field = Entry(self.frame, width=ctrlWidth+20, textvariable=confirmPassword_verify, show= '*' , highlightbackground=myBorderColor, highlightcolor=myBorderColor, highlightthickness=1 , bd= 0 )
        self.ConfirmPassword_field.place(x=xEdtVal, y=yVal)
        #self.Password_field.bind("<Return>", self.name_focus) 
        yVal += 35       
        
        # 4. Row 4 - E-Mail
        self.EMail = Label(self.frame, text=strObj.strEmpEmail  , fg=myTxtColor, bg=myAppBGColor, font=(myFont, myTxtFontSize), justify=LEFT, anchor=W)  
        self.EMail.configure(height=ctrlHeight, width=ctrlWidth)
        self.EMail.place(x=xLblVal,y=yVal) 

        self.email_field = Entry(self.frame, width=ctrlWidth+20, textvariable=email_verify , highlightbackground=myBorderColor, highlightcolor=myBorderColor, highlightthickness=1 , bd= 0 )
        self.email_field.place(x=xEdtVal, y=yVal)
         

        

        # Button
        yBtnVal = 305 + 270

        # rounded_btn_dark.png
        imgPath = cf.GetAppImageDirPath()
        btnImg_N1 = imgPath + "rounded_btn_dark.png"
        self.img_N1=PhotoImage(file=btnImg_N1 )         
        ctrlHeight = 36
        ctrlWidth = 180
        xbtnVal = 345
        self.btnCancel_btn = Button(self.frame, image=self.img_N1 , text=strObj.strBtnCancel, command=self.onBtnClickCancel, justify = RIGHT, fg=myTxtColor, font=(myFont, myTxtFontSize) , bg=myBtnBGColor  , border=0,   highlightthickness = 0, borderwidth = 0 )
        self.btnCancel_btn.configure(height=ctrlHeight, width=ctrlWidth , compound=CENTER)
        self.btnCancel_btn.place(x=xbtnVal, y=yBtnVal)

        btnImg_N2 = imgPath + "rounded_btn.png"
        self.img_N2=PhotoImage(file=btnImg_N2 ) 

        xbtnVal = 545
        self.btnSave = Button(self.frame, image=self.img_N2 , text= strObj.strBtnSave  , command=self.onBtnClickSave, justify = RIGHT, fg=myTxtColor, font=(myFont, myTxtFontSize) , bg=myBtnBGColor  , border=0,   highlightthickness = 0, borderwidth = 0 )
        self.btnSave.configure(height=ctrlHeight, width=ctrlWidth , compound=CENTER)
        self.btnSave.place(x=xbtnVal, y=yBtnVal) 
   
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

    def onBtnClickSave(self):
        userName = userName_verify.get()
        sPW = Password_verify.get()
        sCPW = confirmPassword_verify.get()
        email = email_verify.get()

        userName = userName.strip()
        sPW = sPW.strip()
        sCPW = sCPW.strip() 
        email = email.strip()            

        if( ( userName == "") or (sPW == "") or ( sCPW == "") or (email == "") ):
            msg.showinfo( strObj.strPageLogin,  strObj.strBlank )
        elif( False == self.valideEmail(email) ):
            msg.showinfo(strObj.strPageTitleNewUser, strObj.strEmailNotValid )
            return
        elif( sPW == sCPW ):
                # save new pw in DB
                objDB = MyMongoDB()
                objDB.Register_User( userName, sPW, email )
                msg.showinfo(strObj.strPageTitleNewUser, strObj.strRegisterSuccessfully)

                self.myParent.lblRegNewUser['state']="disabled"
                self.myParent.bUserAlreadyRegistered = True

                # this will delete the entry after button is pressed
                self.userName_field.delete(0, END)
                self.Password_field.delete(0, END)
                self.ConfirmPassword_field.delete(0, END)

                self.onBtnClickCancel()
        else:
            # msg.showinfo("Password", "Password and Confirmed password both are different")
            msg.showinfo(strObj.strPageLogin, strObj.strNewUserDiffPW )


    def onBtnClickCancel(self):
        # open Login Page
        print("Bye MyRegisterNewUserPage-1-2")
        self.frame.destroy()

   


def myMyRegisterNewUserPageMain(root):    
    MyRegisterNewUserPage(root)
 

if __name__ == "__main__" :
    root = Tk()
    root.geometry("960x640")
    root.title( "strApptitle" )     
    root.resizable(False, False)
    root.configure(background="pink" )

    myMyRegisterNewUserPageMain(root)     

    root.mainloop()

