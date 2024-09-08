
from tkinter import *
from AllStrings import myStrings
import common_fun as cf 
import tkinter.messagebox as msg
import time
import tkinter.font as font
 
import tkinter as tk
from Mongo_DB import MyMongoDB
import calendar 
from PIL import Image
from PIL import ImageTk
import os 


myAppBGColor =  "grey" 
myFont = "Helvetica"
myHeadingTxtFontSize = 15
myTxtFontSize = 10
myTxtColor = "white"
myBtnBGColor="Green"

Legend_color_present = "green"
Legend_color_absent = "red"
Legend_color_WorkOnHoliday = "yellow"
Legend_color_Holiday = "#8080FF"
myLegendTxtColor = "black"


strObj  = myStrings()


class MyYearTkinterCalendar(calendar.Calendar):
   
    def My_Complete_Year_Calendar(self, master, year, month, emp_attendance_days_list  ):
        #tk.Label(master, text = '{} / {}'.format(year, month)).pack()
        frame = tk.Frame(master)
        myRow = 1
        myCol = 1
        Lbl = tk.Label(frame, text = '{} / {}'.format(year, month)) 
        Lbl.grid(row=myRow, column=myCol, padx=1, pady = 1) 
        myRow += 1
        #create heading- Su Mo Tu We Th Fr Sa
        weekDay = [ 'Mon', 'Tue', 'Wed', 'Thr', 'Fri', 'Sat','Sun']
        i = 0
        for strName in weekDay:
            label1 = tk.Label(frame, text= f"{strName}" ,  borderwidth=0, relief="groove", underline=True )
            label1.grid(row=myRow, column=i, padx=0, pady = 0) 
            i += 1

        myRow += 1
        #employe data
        emp_att = emp_attendance_days_list # [1,2,3,5,6,7,9,11,15,18,21,25,26,27,30]
        #days = self.monthdayscalendar(year, month)
        days = self.monthdatescalendar(year, month)
        self.labels = []
        for r, week in enumerate(days):
            r += 1 + myRow
            labels_row = []
            for c, date in enumerate(week):
                strTxtToDisplay = "" 
                #if(date != 0 ):
                if date.month == month:
                     
                    strTxtToDisplay = date.day
                    label = tk.Button(frame, text= f"{strTxtToDisplay}")
                    label.grid(row=r, column=c, padx=0, pady = 0)
                    if( c == 6  ) :
                        if( date.day in emp_att):
                            # for Sunday but Working day
                            label['bg'] = Legend_color_WorkOnHoliday
                            label['fg'] = 'black'
                             
                        else:
                            # for Sunday - Holiday
                            label['bg'] = Legend_color_Holiday
                            label['fg'] = 'black'
                            
                    elif( date.day in emp_att):
                        label['bg'] = Legend_color_present
                        label['fg'] = 'black'
                        #label.configure(text="Hi")
                         
                    else :
                        # On leave
                        label['bg'] = Legend_color_absent
                        label['fg'] = 'black'
                         
                    labels_row.append(label)
            self.labels.append(labels_row)
        return frame 



class MyYearWiseAttendance(tk.Frame):  

    def __del__(self):
        #msg.showinfo("Title 1 ", "Login close destroy....") 
        print("Bye MyYearWiseAttendance-1-1")

    def __init__(self, master, Parent=None):
        print("Hi MyYearWiseAttendance-1-1")

        #self._frame = None
        tk.Frame.__init__(self, master)

        #self._frame = master
        self.myroot = master
        self.myParent = Parent

        # define font - weight − "bold" for boldface, "normal" for regular weight
        #self.myFont = font.Font(family='Helvetica', size=13, weight='normal')

        self.frame = tk.Frame(master, width=385, height=460, borderwidth=0, bg= myAppBGColor, relief=SUNKEN   )
        ####self.frame.pack(side = LEFT, anchor = "nw", fill=Y, expand=YES)
        self.frame.place(x=200, y=0, anchor="nw", width=758, height=621)
 
        self.CreatePageGUI()

   
    def CreatePageGUI(self):
        self.myroot.grid_columnconfigure((0,1), weight=1)
        
        # create a Form Heading label 
        xLblVal = 80
        yVal = 32
        ctrlHeight = 2
        ctrlWidth = 20+5

        # Heading...
        self.heading = Label(self.frame, text=strObj.strReSetPW, fg=myTxtColor, bg=myAppBGColor, font=(myFont, myHeadingTxtFontSize), compound="left" , justify=LEFT, anchor=W )
        self.heading.configure(height=ctrlHeight, width=ctrlWidth)
        self.heading.place(x=xLblVal,y=yVal)  #.pack(expand=YES, fill=BOTH)     

           
        ####------Y--side-scrollbar------------
        xLblVal = 5  
        yVal = 90        
        ####------Y--side-scrollbar------------
        self.frm1 = Frame(self.frame)
        self.frm1.configure(height=300, width=620 )
        self.frm1.place(x=xLblVal, y=yVal)          
        self.y_scrollbar = Scrollbar(self.frm1, orient="vertical")
        self.y_scrollbar.pack(side=RIGHT, fill=Y) 
        self.listNodes = Listbox(self.frm1,width=80, height=23, yscrollcommand=self.y_scrollbar.set, font=("Helvetica", 12))
        self.listNodes.pack(side="left", fill="y")
        self.y_scrollbar.config( command=self.listNodes.yview )

        ####------X-side-scrollbar------------
        # self.x_scrollbar = Scrollbar(self.frm1, orient=HORIZONTAL)
        # self.x_scrollbar.pack(side=TOP, fill=X) 
        # #self.listNodes = Listbox(self.frm1,width=65, height=14, xscrollcommand=self.x_scrollbar.set, font=("Helvetica", 12))
        # self.listNodes.config(xscrollcommand=self.x_scrollbar.set)
        # self.listNodes.pack(side=TOP, fill=X)
        # self.x_scrollbar.config( command=self.listNodes.xview )
        ####-------------------


        xLblVal = 15
        yVal = 5
        self.myLblYearCalendar_1 = Label(self.listNodes, borderwidth=1, relief="groove",  fg=myTxtColor, bg=myAppBGColor, font=(myFont, myHeadingTxtFontSize), compound="left" )
        self.myLblYearCalendar_1.configure(height=10, width=25 )
        self.myLblYearCalendar_1.place(x=xLblVal,y=yVal)
        xLblVal += 240
        
        self.myLblYearCalendar_2 = Label(self.listNodes, borderwidth=1, relief="groove",  fg=myTxtColor, bg=myAppBGColor, font=(myFont, myHeadingTxtFontSize), compound="left" )
        self.myLblYearCalendar_2.configure(height=10, width=25 )
        self.myLblYearCalendar_2.place(x=xLblVal,y=yVal)
        xLblVal += 230
         
        self.myLblYearCalendar_3 = Label(self.listNodes, borderwidth=1, relief="groove",  fg=myTxtColor, bg=myAppBGColor, font=(myFont, myHeadingTxtFontSize), compound="left" )
        self.myLblYearCalendar_3.configure(height=10, width=25 )
        self.myLblYearCalendar_3.place(x=xLblVal,y=yVal)
        
        xLblVal = 15
        yVal += 230
        self.myLblYearCalendar_4 = Label(self.listNodes, borderwidth=1, relief="groove",  fg=myTxtColor, bg=myAppBGColor, font=(myFont, myHeadingTxtFontSize), compound="left" )
        self.myLblYearCalendar_4.configure(height=10, width=25 )
        self.myLblYearCalendar_4.place(x=xLblVal,y=yVal)
        xLblVal += 240
        
        self.myLblYearCalendar_5 = Label(self.listNodes, borderwidth=1, relief="groove",  fg=myTxtColor, bg=myAppBGColor, font=(myFont, myHeadingTxtFontSize), compound="left" )
        self.myLblYearCalendar_5.configure(height=10, width=25 )
        self.myLblYearCalendar_5.place(x=xLblVal,y=yVal)
        xLblVal += 230
         
        self.myLblYearCalendar_6 = Label(self.listNodes, borderwidth=1, relief="groove",  fg=myTxtColor, bg=myAppBGColor, font=(myFont, myHeadingTxtFontSize), compound="left" )
        self.myLblYearCalendar_6.configure(height=10, width=25 )
        self.myLblYearCalendar_6.place(x=xLblVal,y=yVal)


        xbtnVal = 565+45
        self.btnClose = Button(self.frame, text= strObj.strBtnClose  , command=self.onBtnClickClose , justify = RIGHT, fg=myTxtColor, font=(myFont, myTxtFontSize) , bg=myBtnBGColor)
        self.btnClose.configure(height=1, width=10)
        self.btnClose.place(x=xbtnVal, y=565) 
   
        # Legend = [Green, Red, Yellow, Grey ]
        ctrlLegendHeight = 1
        ctrlLegendWidth = 10
        xLegendVal = 70
        yLegendVal = 570
        # 1. Present - Working day - Green
        self.LegendPresent = Label(self.frame, text= "" ,fg=myLegendTxtColor, bg= Legend_color_present, font=(myFont, myTxtFontSize), compound="left" )
        self.LegendPresent.configure(height=1, width=1)
        self.LegendPresent.place(x = xLegendVal, y = yLegendVal)
        xLegendVal += 16
        self.LegendPresentTxt = Label(self.frame, text= strObj.strLegendPresent ,fg=myLegendTxtColor, bg=myAppBGColor, font=(myFont, myTxtFontSize), compound="left" , justify=LEFT, anchor=W )
        self.LegendPresentTxt.configure(height=ctrlLegendHeight, width=ctrlLegendWidth)
        self.LegendPresentTxt.place(x = xLegendVal, y = yLegendVal)
        xLegendVal += 100  
        # 2. On leave - Red
        self.LegendAbsent = Label(self.frame, text= "" ,fg=myLegendTxtColor, bg= Legend_color_absent, font=(myFont, myTxtFontSize), compound="left" )
        self.LegendAbsent.configure(height=1, width=1)
        self.LegendAbsent.place(x = xLegendVal, y = yLegendVal)  
        xLegendVal += 16
        self.LegendAbsentTxt = Label(self.frame, text= strObj.strLegendAbsent ,fg=myLegendTxtColor, bg=myAppBGColor, font=(myFont, myTxtFontSize), compound="left" , justify=LEFT, anchor=W )
        self.LegendAbsentTxt.configure(height=ctrlLegendHeight, width=ctrlLegendWidth)
        self.LegendAbsentTxt.place(x = xLegendVal, y = yLegendVal)
        xLegendVal += 100    
        # 4. Holiday - Grey
        self.LegendHoliday = Label(self.frame, text= "" ,fg=myLegendTxtColor, bg=Legend_color_Holiday, font=(myFont, myTxtFontSize), compound="left" )
        self.LegendHoliday.configure(height=1, width=1)
        self.LegendHoliday.place(x = xLegendVal, y = yLegendVal) 
        xLegendVal += 20
        self.LegendHolidayTxt = Label(self.frame, text= strObj.strLegendHoliday ,fg=myLegendTxtColor, bg=myAppBGColor, font=(myFont, myTxtFontSize), compound="left" , justify=LEFT, anchor=W )
        self.LegendHolidayTxt.configure(height=ctrlLegendHeight, width=ctrlLegendWidth)
        self.LegendHolidayTxt.place(x = xLegendVal, y = yLegendVal)        
        xLegendVal += 100      
        # 3. Work on Holiday - Yellow
        self.LegendWorkOnHoliday = Label(self.frame, text= "" ,fg=myLegendTxtColor, bg=Legend_color_WorkOnHoliday, font=(myFont, myTxtFontSize), compound="left" )
        self.LegendWorkOnHoliday.configure(height=1, width=1)
        self.LegendWorkOnHoliday.place(x = xLegendVal, y = yLegendVal)  
        xLegendVal += 20
        self.LegendWorkOnHolidayTxt = Label(self.frame, text= strObj.strLegendWorkONHoliday ,fg=myLegendTxtColor, bg=myAppBGColor, font=(myFont, myTxtFontSize), compound="left" , justify=LEFT, anchor=W )
        self.LegendWorkOnHolidayTxt.configure(height=ctrlLegendHeight, width=ctrlLegendWidth+10)
        self.LegendWorkOnHolidayTxt.place(x = xLegendVal, y = yLegendVal)       


        self.ShowYear_Wise_Attendance()

  
    def ShowYear_Wise_Attendance(self):
        ###emp_info = self.myParent.GetEmpInfo_ID_Name_Year()
        empid_value = "001"  ## emp_info[0]
        name_value =  ""     ## emp_info[1]
        year_value = "2020"  ## emp_info[2]

        if ( (empid_value.strip() == "" ) and ( name_value.strip() == "")  ):
            print("empty input") 
            msg.showinfo(strObj.strMsgTitel, strObj.strFillAtleastOneOption)
        else:
            ## to Get emp info from db
            #obj = MyMongoDB()
            # 1. first of all check - emp. Attendance is available or not in given year
            # bIsEmpExist = obj.Search_Year_for_EmpID_OR_EmpName_ExistsIn_Attendance_Table(empid_value.strip(), name_value.strip(), year_value.strip() )
            # if(False == bIsEmpExist):
            #     msg.showinfo(strObj.strMsgTitel, strObj.strMsgSearchUserAttendanceNotAvailable ) 
            #     return 
            emp_all_month_attendance_days_List = [1,2,4,6,8,9,10,13,20,21,22,23,24,25,26,27]
            objYearCal = MyYearTkinterCalendar()
 
            month = 1 
            self.myYearCalframe  = objYearCal.My_Complete_Year_Calendar(  self.myLblYearCalendar_1 , int(year_value), month, emp_all_month_attendance_days_List   )
            self.myYearCalframe.pack(side = LEFT, anchor = "nw",   expand=YES)
            month = 2 
            self.myYearCalframe2  = objYearCal.My_Complete_Year_Calendar(  self.myLblYearCalendar_2 , int(year_value), month, emp_all_month_attendance_days_List   )
            self.myYearCalframe2.pack(side = LEFT, anchor = "nw",   expand=YES)
            month = 3 
            self.myYearCalframe3  = objYearCal.My_Complete_Year_Calendar(  self.myLblYearCalendar_3 , int(year_value), month, emp_all_month_attendance_days_List   )
            self.myYearCalframe3.pack(side = LEFT, anchor = "nw",   expand=YES)
            month = 4 
            self.myYearCalframe4  = objYearCal.My_Complete_Year_Calendar(  self.myLblYearCalendar_4 , int(year_value), month, emp_all_month_attendance_days_List   )
            self.myYearCalframe4.pack(side = LEFT, anchor = "nw",   expand=YES)
            month = 5 
            self.myYearCalframe5  = objYearCal.My_Complete_Year_Calendar(  self.myLblYearCalendar_5 , int(year_value), month, emp_all_month_attendance_days_List   )
            self.myYearCalframe5.pack(side = LEFT, anchor = "nw",   expand=YES)
            month = 6 
            self.myYearCalframe6  = objYearCal.My_Complete_Year_Calendar(  self.myLblYearCalendar_6 , int(year_value), month, emp_all_month_attendance_days_List   )
            self.myYearCalframe6.pack(side = LEFT, anchor = "nw",   expand=YES)            





    def onBtnClickClose(self):
        # open Login Page
        print("Bye MyYearWiseAttendance-1-1")
        self.frame.destroy()
        self.myParent.onBtnClickClearAttendance()
        



def myForgotPWMain(root):    
    MyYearWiseAttendance(root)
 

if __name__ == "__main__" :
    root = Tk()
    root.geometry("960x640")
    root.title( "strApptitle" )     
    root.resizable(False, False)
    root.configure(background="pink" )

    myForgotPWMain(root)     

    root.mainloop()


