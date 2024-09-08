  
#from tkinter import Tk, Label, Button

from tkinter import *
from AllStrings import myStrings
import common_fun as cf 
import tkinter.messagebox as msg
import time
import tkinter.font as font
 
import tkinter as tk

myAppBGColor =  "lavender blush" #  "grey" 
myFont = "Helvetica"
myHeadingTxtFontSize = 15
myTxtFontSize = 10
myTxtColor = "black" # "white"
myBtnBGColor= "lavender blush" # "Green"
myBorderColor = "medium violet red"
myBtnTxtColor = "white"


strObj  = myStrings()


class MyAboutPage(tk.Frame):
    def __del__(self):
        print("Bye MyAboutPage-7")
    def __init__(self,  tkFrame, Parent=None):
        print("Hi MyAboutPage-7")

        #self._frame = None
        tk.Frame.__init__(self,  tkFrame, Parent)

        #self._frame = tkFrame
        self.myParent = Parent
        self.myroot = tkFrame

        # define font - weight − "bold" for boldface, "normal" for regular weight
        #self.myFont = font.Font(family='Helvetica', size=13, weight='normal')

        self.frame = tk.Frame(tkFrame, width=385, height=460, borderwidth=0, bg= myAppBGColor , relief=SUNKEN   )
        #self.frame.pack(side = LEFT, anchor = "nw", fill=Y, expand=YES)
        self.frame.place(x=200-4, y=1, anchor="nw", width=758+6, height=621-1)

        # if(False):
        #     self.strMyAppStatus = strObj.strRegisterVer
        # else:
        #     self.strMyAppStatus = strObj.strAppTrialVer

        self.strMyAppStatus = Parent.sAppStatus
 
        self.CreateAboutPageGUI()

    def CreateAboutPageGUI(self):
        self.myroot.grid_columnconfigure((0,1), weight=1)

        # create a Form Heading label 
        xLblVal = 80
        yVal = 32
        ctrlHeight = 3
        ctrlWidth = 80

        # Heading...
        self.heading = Label(self.frame, text=strObj.strHeadingAbout , fg=myTxtColor, bg=myAppBGColor, font=(myFont, myHeadingTxtFontSize), compound="left" , justify=LEFT, anchor=W )
        self.heading.configure(height=ctrlHeight, width=ctrlWidth)
        self.heading.place(x=xLblVal,y=32)  #.pack(expand=YES, fill=BOTH)     
    
        yVal += 85 + 30
        ctrlHeight = 1 
        ctrlWidth = 25
        # 1. Row 1 - Company Name
        self.CompanyLbl = Label(self.frame, text=strObj.strCompanyName , fg=myTxtColor, bg=myAppBGColor, font=(myFont, myTxtFontSize), justify=LEFT, anchor=W)
        self.CompanyLbl.configure(height=ctrlHeight, width=ctrlWidth)
        self.CompanyLbl.place(x=xLblVal,y=yVal) 
        xLblVal += 200
        ctrlWidth = 35
        self.CompanyName = Label(self.frame, text=strObj.strCompany, fg=myTxtColor, bg=myAppBGColor, font=(myFont, myTxtFontSize), justify=LEFT, anchor=W)
        self.CompanyName.configure(height=ctrlHeight, width=ctrlWidth)
        self.CompanyName.place(x=xLblVal,y=yVal)
        yVal += 35

        # 2. Row 2 - Version
        xLblVal = 80
        ctrlWidth = 25
        self.VersionLbl = Label(self.frame, text=strObj.strVNum, fg=myTxtColor, bg=myAppBGColor, font=(myFont, myTxtFontSize), justify=LEFT, anchor=W)
        self.VersionLbl.configure(height=ctrlHeight, width=ctrlWidth)
        self.VersionLbl.place(x=xLblVal,y=yVal) 
        xLblVal += 200
        ctrlWidth = 35
        self.VersionName = Label(self.frame, text=strObj.strVersionNo, fg=myTxtColor, bg=myAppBGColor, font=(myFont, myTxtFontSize), justify=LEFT, anchor=W)
        self.VersionName.configure(height=ctrlHeight, width=ctrlWidth)
        self.VersionName.place(x=xLblVal,y=yVal)
        yVal += 35

        # 3. Row 3 - License
        xLblVal = 80
        ctrlWidth = 25
        self.LicenseLbl = Label(self.frame, text=strObj.strLicenseStatus, fg=myTxtColor, bg=myAppBGColor, font=(myFont, myTxtFontSize), justify=LEFT, anchor=W)
        self.LicenseLbl.configure(height=ctrlHeight, width=ctrlWidth)
        self.LicenseLbl.place(x=xLblVal,y=yVal) 
        xLblVal += 200
        ctrlWidth = 35
        self.LicenseStatus = Label(self.frame, text=self.strMyAppStatus, fg=myTxtColor, bg=myAppBGColor, font=(myFont, myTxtFontSize), justify=LEFT, anchor=W)
        self.LicenseStatus.configure(height=ctrlHeight, width=ctrlWidth)
        self.LicenseStatus.place(x=xLblVal,y=yVal)
        yVal += 35


        # 4. Row 4 - Company URL - Company WebSite
        xLblVal = 80
        ctrlWidth = 25
        self.CompanyLbl = Label(self.frame, text=strObj.strCompany_WebSite, fg=myTxtColor, bg=myAppBGColor, font=(myFont, myTxtFontSize), justify=LEFT, anchor=W)
        self.CompanyLbl.configure(height=ctrlHeight, width=ctrlWidth)
        self.CompanyLbl.place(x=xLblVal,y=yVal) 
        xLblVal += 200
        ctrlWidth = 35
        self.CompanyURL = Label(self.frame, text=strObj.strCompanyurl, fg="blue", cursor="hand2", bg=myAppBGColor, font=(myFont, myTxtFontSize), justify=LEFT, anchor=W)
        self.CompanyURL.configure(height=ctrlHeight, width=ctrlWidth)
        self.CompanyURL.place(x=xLblVal,y=yVal)
        self.CompanyURL.bind("<Button-1>", self.callback_onBtnOpenCompanyURL)

        yVal += 35        

    def callback_onBtnOpenCompanyURL(self, event):
        import webbrowser
        webbrowser.open( strObj.strCompanyurl )



        # # 4. Row 4 - 
        # xLblVal = 80
        # ctrlWidth = 25
        # self.LicenseLbl = Label(self.frame, text="License Status", bg="light green")
        # self.LicenseLbl.configure(height=ctrlHeight, width=ctrlWidth)
        # self.LicenseLbl.place(x=xLblVal,y=yVal) 
        # xLblVal += 200
        # ctrlWidth = 35
        # self.LicenseStatus = Label(self.frame, text="Trial version", bg="light green")
        # self.LicenseStatus.configure(height=ctrlHeight, width=ctrlWidth)
        # self.LicenseStatus.place(x=xLblVal,y=yVal)
        # yVal += 35






 
def myAboutMain(root):
    
    MyAboutPage(root)
    

if __name__ == "__main__" :
    root = Tk()
    root.geometry("960x640")
    root.title( "strApptitle" )     
    root.resizable(False, False)
    root.configure(background="black" )

    myAboutMain(root)

    root.mainloop()


