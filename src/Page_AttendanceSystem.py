
#from tkinter import Tk, Label, Button

from tkinter import *
from AllStrings import myStrings
import common_fun as cf 
import tkinter.messagebox as msg
import time
import tkinter.font as font
import tkinter as tk
from tkinter import ttk
from Mongo_DB import MyMongoDB


from tkcalendar import Calendar, DateEntry
# import calendar module 
import calendar 
from PIL import Image
from PIL import ImageTk
import os 
# import openpyxl and tkinter modules 
#from openpyxl import *
# import xlsxwriter module 
import xlsxwriter
from tkinter.filedialog import asksaveasfile 


myAppBGColor =  "lavender blush" #  "grey" 
myFont = "Helvetica"
myHeadingTxtFontSize = 15
myTxtFontSize = 10
myTxtColor =  "black" #  "white"
myBtnBGColor= "lavender blush" # "Green"
myBorderColor = "medium violet red"
myBtnTxtColor = "white"

Legend_color_present = "green"
Legend_color_absent = "red"
Legend_color_WorkOnHoliday = "yellow"
Legend_color_Holiday = "#8080FF"
myLegendTxtColor = "black"

nCount_Total_Days_InMonth = 0
nCount_Total_Present_Days = 0
nCount_Total_Absent_Days = 0
nCount_Total_Holiday_Days = 0
nCount_Total_Work_On_Holiday_Days = 0

strObj  = myStrings()
imgPath = cf.GetAppImageDirPath() 

class Callback:
    def __init__(self, func, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs
    def __call__(self):
        self.func(*self.args, **self.kwargs)

def onBtnClickMonthDays(nMonthDays, sYear, nMonth , empid_value, name_value, obj_image):
    ## print("Button '{}' pressed.".format(nMonthDays))
    print(f"monthday = {nMonthDays}, Year = {sYear}, month = {nMonth}, EmpID = {empid_value}, EmpName = {name_value}")
    
    Month = {  'January' : 1, 'February' : 2, 'March' : 3, 'April' : 4, 'May' : 5,  'June' : 6, 'July' : 7, 'August' : 8, 'September' : 9, 'October' : 10, 'November' : 11, 'December' : 12 }
    strMyMonth = ""
    for key, value in Month.items(): 
        if nMonth == value: 
            strMyMonth = key
            break
    strMonthDays  = "{0:0=2d}".format(nMonthDays)

    obj = MyMongoDB()
    #to get employee image
    obj.GetEmp_Photo_DateWise_During_Attendance_Mark( empid_value.strip(), name_value.strip(), strMyMonth , strMonthDays  )
    imgPath = cf.Get_Emp_Tmp_Image_Dir() + "//attendance.png"  ## Ajay
    if os.path.isfile(imgPath):
        ###--new---
        my_img = Image.open( imgPath )
        img_resized = my_img.resize((210,250), Image.ANTIALIAS)
        myPhotofrm = ImageTk.PhotoImage( img_resized  )
        obj_image.image = myPhotofrm  
        obj_image.configure( image = myPhotofrm  )
        
        ###--old---
        # myPhotofrm = PhotoImage(file = imgPath  )
        # obj_image.image = myPhotofrm  
        # obj_image.configure( image = myPhotofrm  )

class TkinterCalendar(calendar.Calendar):
    def formatmonth(self, master, year, month):
        # show next month days also
        dates = self.monthdatescalendar(year, month) 
        frame = tk.Frame(master)
        self.labels = []
        for r, week in enumerate(dates):
            labels_row = []
            for c, date in enumerate(week):
                label = tk.Button(frame, text=date.strftime('%Y\n%m\n%d'))
                label.grid(row=r, column=c)
                if date.month != month:
                    # not below to this month
                    label['bg'] = '#aaa'
                if c == 6:
                    # for Sunday
                    label['fg'] = 'red'
                labels_row.append(label)
            self.labels.append(labels_row)
        return frame
    
    def My_New_Year_Wise_Attendance(self, master, year, month, emp_attendance_days_list):
        tk.Label(master, text = '{} / {}'.format(year, month)).pack()
        print("Year wise display")
        frame = tk.Frame(  master )
        #create heading- Su Mo Tu We Th Fr Sa
        weekDay = [ 'Mon', 'Tue', 'Wed', 'Thr', 'Fri', 'Sat','Sun']
        i = 0
        for strName in weekDay:
            label1 = tk.Label(frame, text= f"{strName}" ,  borderwidth=0, relief="groove", underline=True )
            label1.grid(row=0, column=i, padx=5, pady = 5) 
            i += 1
        #employe data
        emp_att = emp_attendance_days_list # [1,2,3,5,6,7,9,11,15,18,21,25,26,27,30]
        #days = self.monthdayscalendar(year, month)
        days = self.monthdatescalendar(year, month)
        self.labels = []
        for r, week in enumerate(days):
            r += 1
            labels_row = []
            for c, date in enumerate(week):
                strTxtToDisplay = "" 
                #if(date != 0 ):
                if date.month == month:
                    strTxtToDisplay = date.day
                    label = tk.Button(frame, text= f"{strTxtToDisplay}")
                    label.grid(row=r, column=c, padx=5, pady = 5)
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
       

    # def onBtnClickMonthDays(self, sMonthday):
    #     print( f"Btn click no = {sMonthday}")

    def My_New_Month(self, master, year, month, emp_attendance_days_list, empid_value, name_value, obj_image):
        ##lbl_header = tk.Label(master, text = '{} / {}'.format(year, month)).pack()
        global nCount_Total_Days_InMonth
        nCount_Total_Days_InMonth = 0
        global nCount_Total_Present_Days
        nCount_Total_Present_Days = 0
        global nCount_Total_Absent_Days
        nCount_Total_Absent_Days = 0
        global nCount_Total_Holiday_Days
        nCount_Total_Holiday_Days = 0
        global nCount_Total_Work_On_Holiday_Days
        nCount_Total_Work_On_Holiday_Days = 0

        frame = tk.Frame(master)
        
        #create heading- Su Mo Tu We Th Fr Sa
        weekDay = [ 'Mon', 'Tue', 'Wed', 'Thr', 'Fri', 'Sat','Sun']
        i = 0
        for strName in weekDay:
            label1 = tk.Label(frame, text= f"{strName}" ,  borderwidth=0, relief="groove", underline=True )
            label1.grid(row=0, column=i, padx=5, pady = 5) 
            i += 1

        #employe data
        emp_att = emp_attendance_days_list # [1,2,3,5,6,7,9,11,15,18,21,25,26,27,30]
        #days = self.monthdayscalendar(year, month)
        days = self.monthdatescalendar(year, month)
        self.labels = []
        for r, week in enumerate(days):
            r += 1
            labels_row = []
            for c, date in enumerate(week):
                strTxtToDisplay = "" 
                #if(date != 0 ):
                if date.month == month:
                    nCount_Total_Days_InMonth += 1
                    strTxtToDisplay = date.day
                    label = tk.Button(frame, text= f"{strTxtToDisplay}", command=Callback(onBtnClickMonthDays, strTxtToDisplay, year, month, empid_value, name_value, obj_image )  )
                    label.grid(row=r, column=c, padx=5, pady = 5)
                    if( c == 6  ) :
                        if( date.day in emp_att):
                            # for Sunday but Working day
                            label['bg'] = Legend_color_WorkOnHoliday
                            label['fg'] = 'black'
                            nCount_Total_Work_On_Holiday_Days += 1
                        else:
                            # for Sunday - Holiday
                            label['bg'] = Legend_color_Holiday
                            label['fg'] = 'black'
                            nCount_Total_Holiday_Days += 1
                    elif( date.day in emp_att):
                        label['bg'] = Legend_color_present
                        label['fg'] = 'black'
                        #label.configure(text="Hi")
                        nCount_Total_Present_Days += 1
                    else :
                        # On leave
                        label['bg'] = Legend_color_absent
                        label['fg'] = 'black'
                        nCount_Total_Absent_Days += 1
                    labels_row.append(label)
            self.labels.append(labels_row)
        return frame 


class MyAttendanceSystemPage(tk.Frame):
    def __del__(self):
        print("Bye MyAttendanceSystemPage-5")

    def __init__(self, tkFrame, Parent=None):
        print("Hi MyAttendanceSystemPage-5")
        #self._frame = None
        tk.Frame.__init__(self, tkFrame, Parent)

        #self._frame = tkFrame
        self.myParent = Parent
        self.myroot = tkFrame

        self._frame = None

        global bIsMonthCaldendarShow
        self.bIsMonthCaldendarShow = False

        # define font - weight − "bold" for boldface, "normal" for regular weight
        #self.myFont = font.Font(family='Helvetica', size=13, weight='normal')

        self.frame = tk.Frame(tkFrame, width=385, height=460, borderwidth=0, bg= myAppBGColor, relief=SUNKEN   )
        #self.frame.pack(side = LEFT, anchor = "nw", fill=Y, expand=YES)
        self.frame.place(x=200-4, y=1, anchor="nw", width=758+6, height=621-1)

        self.CreateAttendancePageGUI()

    def CreateAttendancePageGUI(self):
        self.myroot.grid_columnconfigure((0,1), weight=1)

        # create a Form Heading label 
        xLblVal = 80
        yVal = 32
        ctrlHeight = 3
        ctrlWidth = 20
         
        # Heading...
        self.heading = Label(self.frame, text= strObj.strAttendancePageHeading ,fg=myTxtColor, bg=myAppBGColor, font=(myFont, myHeadingTxtFontSize), compound="left" )
        self.heading.configure(height=ctrlHeight, width=ctrlWidth + 15 )
        self.heading.place(x=xLblVal,y=32)  #.pack(expand=YES, fill=BOTH)     
    
        yVal += 85 
        xEdtVal = 230
        ctrlHeight = 1 
        ctrlWidth = 15
  
        global radioValueEdit_ATT
        radioValueEdit_ATT = IntVar()
        # 1. Radio - emp_id
        self.emp_id = Radiobutton(self.frame, text=strObj.strEmpID,  bg=myAppBGColor, font=(myFont, myTxtFontSize), compound="left", variable=radioValueEdit_ATT, value=1, command=self.onClickRadioBtnEdit_RFD, activeforeground= myTxtColor, activebackground = myAppBGColor)
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
        self.emp_name = Radiobutton(self.frame, text=strObj.strEmpName,  bg=myAppBGColor, font=(myFont, myTxtFontSize), compound="left", variable=radioValueEdit_ATT, value=2, command=self.onClickRadioBtnEdit_RFD, activeforeground= myTxtColor, activebackground = myAppBGColor)
        self.emp_name.configure(height=ctrlHeight, width=ctrlWidth , selectcolor = "light pink" )
        self.emp_name.place(x=xLblVal-8,y=yVal) 

        self.entry_text_name  = StringVar()
        self.name_field = Entry(self.frame, width=ctrlWidth+20, textvariable=self.entry_text_name , highlightbackground=myBorderColor, highlightcolor=myBorderColor, highlightthickness=1 , bd= 0  )
        self.name_field.place(x=xEdtVal, y=yVal)
        #self.name_field.bind("<Return>", self.name_focus) 
        self.name_field['state'] = 'disable'       
        yVal += 10        
       
        # rounded_btn_dark.png        
        btnImg_N1 = imgPath + "small_btn.png"
        self.img_N1=PhotoImage(file=btnImg_N1 ) 
        ctrlHeight_New = 36
        ctrlWidth_New = 130

        self.btnSearch = Button(self.frame, image=self.img_N1, text= strObj.strBtnShowInfo , justify = RIGHT, command=self.onBtnClickShowAttendance   , fg=myBtnTxtColor, font=(myFont, myTxtFontSize) , bg=myBtnBGColor  , border=0,   highlightthickness = 0, borderwidth = 0)
        #self.btnSearch.configure(height=2, width=15)
        self.btnSearch.configure(height=ctrlHeight_New, width=ctrlWidth_New, compound=CENTER)
        self.btnSearch.place(x=xLblVal + 280 , y=yVal+20)

        btnImg_N0 = imgPath + "small_btn_dark.png"
        self.img_N0=PhotoImage(file=btnImg_N0 ) 

        yVal += 48
        self.btnClear = Button(self.frame, image=self.img_N0, text= strObj.strBtnClear , justify = RIGHT, command=self.onBtnClickClearAttendance   , fg=myBtnTxtColor, font=(myFont, myTxtFontSize) , bg=myBtnBGColor  , border=0,   highlightthickness = 0, borderwidth = 0)
        #self.btnClear.configure(height=2, width=15)
        self.btnClear.configure(height=ctrlHeight_New, width=ctrlWidth_New, compound=CENTER)
        self.btnClear.place(x=xLblVal + 280 , y=yVal+20)

        yVal += 35 + 70

        # global radioValue
        # radioValue = IntVar()
        ctrlHeight = 1 
        ctrlWidth = 10
        xVal = 80
        yVal = 190
        # Radio - Month
        self.month = Label(self.frame, text=strObj.strSelMonth ,  bg=myAppBGColor, font=(myFont, myTxtFontSize), compound="left",   activeforeground= myTxtColor, activebackground = myAppBGColor , justify=LEFT, anchor=W)
        self.month.configure(height=ctrlHeight, width=ctrlWidth)
        self.month.place(x=xVal,y=yVal)
        #self.month.select() 
        # Radio - year
        xVal += 150
        self.year = Label(self.frame, text=strObj.strSelYear,  bg=myAppBGColor, font=(myFont, myTxtFontSize), compound="left",   activeforeground= myTxtColor, activebackground = myAppBGColor, justify=LEFT, anchor=W)
        self.year.configure(height=ctrlHeight, width=ctrlWidth)
        self.year.place(x=xVal,y=yVal) 

        # combobox for month----------------------------------
        self.myMonth = dict()
        self.myMonth = {  'January' : 1, 'February' : 2, 'March' : 3, 'April' : 4, 'May' : 5,  'June' : 6, 'July' : 7, 'August' : 8, 'September' : 9, 'October' : 10, 'November' : 11, 'December' : 12 }
        ctrlHeight = 5 
        ctrlWidth = 13
        xVal = 80
        yVal = 220
        #n = tk.StringVar() 
        self.monthCmbBox = ttk.Combobox(self.frame, width = 32, textvariable = "Text" )
        self.monthCmbBox.configure(height=ctrlHeight, width=ctrlWidth)  
        self.monthCmbBox.place(x=xVal,y=yVal)      
        # Adding combobox drop down list 
        month_list = []
        for mon in self.myMonth:
            month_list.append(mon)
        self.monthCmbBox['values'] = month_list
        #self.monthCmbBox['values'] = (' January', ' February', ' March', ' April', ' May',  ' June', ' July', ' August', ' September', ' October', ' November', ' December')

        # combobox for Year----------------------------------
        xVal += 150
        yVal = 220
        #n = tk.StringVar() 
        self.yearCmbBox = ttk.Combobox(self.frame, width = 32  )
        self.yearCmbBox.configure(height=ctrlHeight, width=ctrlWidth)  
        self.yearCmbBox.place(x=xVal,y=yVal)      
        # Adding combobox drop down list 
        self.yearCmbBox['values'] = ( 2020, 2021, 2022, 2023, 2024, 2025, 2026, 2027, 2028, 2029 )
        ####--------------------------------------------------

        #Display Image in Label
        imgHeight = 230
        imgWidth = 200
        xImgLblVal = 505
        yImgVal = 35
        myPhotofrm = PhotoImage(file = imgPath + 'img.png' )
        self.myImage = Label(self.frame , text="Image", bg="light green", image=myPhotofrm )
        self.myImage.image = myPhotofrm
        self.myImage.pack()
        self.myImage.configure(height=imgHeight, width=imgWidth)
        self.myImage.place(x=xImgLblVal,y=yImgVal) 

        #----Month---Calender ---Work-----
        self.myLblMonthCalendar = Label(self.frame, borderwidth=0, relief="groove",  fg=myTxtColor, bg=myAppBGColor, font=(myFont, myHeadingTxtFontSize), compound="left" )
        self.myLblMonthCalendar.configure(height=10, width=25 )
        #self.myLblMonthCalendar.place(x=80,y=300) 
        self.myLblMonthCalendar.grid(row = 5  , column = 1, padx = 50, pady = 300)

        #----Year---Calender ---Work-----
        # self.myLblYearCalendar = Label(self.frame, borderwidth=1, relief="groove",  fg=myTxtColor, bg=myAppBGColor, font=(myFont, myHeadingTxtFontSize), compound="left" )
        # self.myLblYearCalendar.configure(height=10, width=25 )
        # self.myLblYearCalendar.grid(row = 5  , column = 2, padx = 50, pady = 300)
        #----end------------------------
        #self.myLblMonthCalendar.grid_remove()
        #self.myLblYearCalendar.grid_remove()

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
       
        #show calculation---- 
        # nCount_Total_Days_InMonth = 0
        # nCount_Total_Present_Days = 0
        # nCount_Total_Absent_Days = 0
        # nCount_Total_Holiday_Days = 0
        # nCount_Total_Work_On_Holiday_Days = 0

        ctrlCalHeight = 1
        ctrlCalWidth =  25
        xCalVal = 500
        yCalVal = 350
        sTxt = strObj.strTotal_Days_InMonth + f" = {nCount_Total_Days_InMonth}"
        self.Total_Days_InMonth = Label(self.frame, text= sTxt  ,fg=myLegendTxtColor, bg=myAppBGColor, font=(myFont, myTxtFontSize), compound="left" , justify=LEFT, anchor=W )
        self.Total_Days_InMonth.configure(height=ctrlCalHeight, width=ctrlCalWidth)
        self.Total_Days_InMonth.place(x = xCalVal, y = yCalVal) 
        yCalVal += 35
        sTxt = strObj.strTotal_Present_Days + f" = {nCount_Total_Present_Days}"
        self.Total_Present_Days = Label(self.frame, text= sTxt  ,fg=myLegendTxtColor, bg=myAppBGColor, font=(myFont, myTxtFontSize), compound="left" , justify=LEFT, anchor=W )
        self.Total_Present_Days.configure(height=ctrlCalHeight, width=ctrlCalWidth)
        self.Total_Present_Days.place(x = xCalVal, y = yCalVal) 
        yCalVal += 35
        sTxt = strObj.strTotal_Absent_Days + f" = {nCount_Total_Absent_Days}"
        self.Total_Absent_Days = Label(self.frame, text= sTxt  ,fg=myLegendTxtColor, bg=myAppBGColor, font=(myFont, myTxtFontSize), compound="left" , justify=LEFT, anchor=W )
        self.Total_Absent_Days.configure(height=ctrlCalHeight, width=ctrlCalWidth)
        self.Total_Absent_Days.place(x = xCalVal, y = yCalVal) 
        yCalVal += 35
        sTxt = strObj.strTotal_Holiday_Days + f" = {nCount_Total_Holiday_Days}"
        self.Total_Holiday_Days = Label(self.frame, text= sTxt  ,fg=myLegendTxtColor, bg=myAppBGColor, font=(myFont, myTxtFontSize), compound="left" , justify=LEFT, anchor=W )
        self.Total_Holiday_Days.configure(height=ctrlCalHeight, width=ctrlCalWidth)
        self.Total_Holiday_Days.place(x = xCalVal, y = yCalVal) 
        yCalVal += 35
        sTxt = strObj.strTotal_Work_On_Holiday_Days + f" = {nCount_Total_Work_On_Holiday_Days}"
        self.Total_Work_On_Holiday_Days = Label(self.frame, text= sTxt  ,fg=myLegendTxtColor, bg=myAppBGColor, font=(myFont, myTxtFontSize), compound="left" , justify=LEFT, anchor=W )
        self.Total_Work_On_Holiday_Days.configure(height=ctrlCalHeight, width=ctrlCalWidth)
        self.Total_Work_On_Holiday_Days.place(x = xCalVal, y = yCalVal) 

        newtop = 40
        self.btnExportData = Button(self.frame, image=self.img_N1, text= strObj.strBtnExportData_Excel , justify = RIGHT, command=self.onBtnClickExportData_Excel   , fg=myBtnTxtColor, font=(myFont, myTxtFontSize) , bg=myBtnBGColor , border=0,   highlightthickness = 0, borderwidth = 0)
        #self.btnExportData.configure(height=2, width=15)
        self.btnExportData.configure( height=ctrlHeight_New, width=ctrlWidth_New, compound=CENTER )
        self.btnExportData.place(x= 565 , y=550-newtop)
       
        newY = 560
        self.btnExportAllEmpData = Button(self.frame, image=self.img_N0, text= strObj.strBtnExportAllData_Excel , justify = RIGHT, command=self.onBtnClickExportAllData_Excel   , fg=myBtnTxtColor, font=(myFont, myTxtFontSize) , bg=myBtnBGColor , border=0,   highlightthickness = 0, borderwidth = 0)
        #self.btnExportAllEmpData.configure(height=1, width=15)
        self.btnExportAllEmpData.configure( height=ctrlHeight_New, width=ctrlWidth_New, compound=CENTER  )
        self.btnExportAllEmpData.place(x= 565 , y= newY)


        self.DefaultState()

    # def Show_Hide_Frame1(self, bValue):
    #     if(bValue):
    #         self.myroot.grid_columnconfigure((0,1), weight=1)
    #         self.frm1 = Frame(self.frame)
    #         self.frm1.configure(height=295, width=625 )
    #         self.frm1.place(x=80, y= 290)
    #         self.frm1.grid()
    #     else:
    #         self.frm1.destroy()


    def DefaultState(self):
        self.monthCmbBox.current(0)
        self.yearCmbBox.current(0) 
        # self.monthCmbBox['state'] = 'normal'
        # self.yearCmbBox['state'] = 'disable'
        self.Total_Days_InMonth.config(text='')
        self.Total_Present_Days.config(text='')
        self.Total_Absent_Days.config(text='')
        self.Total_Holiday_Days.config(text='')
        self.Total_Work_On_Holiday_Days.config(text='')
        self.btnClear['state'] = 'disable'
        self.btnExportData['state'] = 'disable'

    def onClickRadioBtnEdit_RFD(self):        
        # print(f"You selected the option { str(radioValueEdit_ATT.get()) } ")
        if( radioValueEdit_ATT.get() == 1 ):
            #print("Radio emp_id")
            self.name_field.delete(0, END) 
            self.empid_field['state'] = 'normal'
            self.name_field['state'] = 'disable'
            self.empid_field.focus()
        elif(radioValueEdit_ATT.get() == 2 ):
            #print("Radio emp_name")
            self.empid_field.delete(0, END)
            self.empid_field['state'] = 'disable'
            self.name_field['state'] = 'normal'
            self.name_field.focus()

    # def onClickRadioBtn(self):        
    #     # print(f"You selected the option { str(radioValue.get()) } ")
    #     if( radioValue.get() == 1 ):
    #         # for Radio month
    #         self.monthCmbBox['state'] = 'normal'
    #         self.yearCmbBox['state'] = 'disable'
    #         #self.myLblMonthCalendar.grid()
    #         ##self.myLblYearCalendar.grid_remove()            
    #         ##self.Show_Hide_Frame1(False)  

    #     elif(radioValue.get() == 2 ):
    #         # for Radio year
    #         self.monthCmbBox['state'] = 'disable'
    #         self.yearCmbBox['state'] = 'normal'
    #         #self.myLblMonthCalendar.grid_remove()
    #         ##self.myLblYearCalendar.grid() 
    #         ##self.Show_Hide_Frame1(True)  

    def ShowMonthWise_Attendance(self, year, month, emp_data_lst, empid_value, name_value, obj_image ):
        emp_attendance_lst = emp_data_lst  
        emp_attendance_year = int(year)
        emp_attendance_month = self.myMonth.get(month)
        objCal = TkinterCalendar()
        self.myCalframe  = objCal.My_New_Month(self.myLblMonthCalendar, emp_attendance_year, emp_attendance_month, emp_attendance_lst, empid_value, name_value, obj_image )
        global bIsMonthCaldendarShow
        self.bIsMonthCaldendarShow = True
        self.myCalframe.pack()
        ####if( radioValue.get() == 1 ):
        #### for Radio month
        # Show only in case of Month
        sTxt = strObj.strTotal_Days_InMonth + f" = {nCount_Total_Days_InMonth}"
        self.Total_Days_InMonth.config(text=sTxt)
        sTxt = strObj.strTotal_Present_Days + f" = {nCount_Total_Present_Days}"
        self.Total_Present_Days.config(text=sTxt)
        sTxt = strObj.strTotal_Absent_Days + f" = {nCount_Total_Absent_Days}"
        self.Total_Absent_Days.config(text=sTxt)
        sTxt = strObj.strTotal_Holiday_Days + f" = {nCount_Total_Holiday_Days}"
        self.Total_Holiday_Days.config(text=sTxt)
        sTxt = strObj.strTotal_Work_On_Holiday_Days + f" = {nCount_Total_Work_On_Holiday_Days}"
        self.Total_Work_On_Holiday_Days.config(text=sTxt)

    # # use to show and hide the frames
    # def Show_Child_frame(self, frame_class, classObj ):
    #     new_frame =  frame_class(classObj, self)
    #     if self._frame is not None:
    #         self._frame.destroy() 
    #         if self._frame.frame is not None:  
    #             self._frame.frame.destroy()

    #     self._frame = new_frame
    #     self._frame.pack()

    # def CreateYearWiseAttendancePageGUI(self):
    #     # msg.showinfo("Btn", "CreateForgotPWPageGUI")
    #     import Page_YearWiseAttendance  as ywAtt
    #     self.Show_Child_frame( ywAtt.MyYearWiseAttendance  , self.myroot )

    # def ShowYearWise_Attendance(self, emp_id, emp_name, year_value):
    #     print("Open Year wise new class....")
    #     self.CreateYearWiseAttendancePageGUI()

    def onBtnClickClearAttendance(self):
        self.btnSearch['state'] = "normal"
        self.btnClear['state'] = "disable"
        self.btnExportData['state'] = 'disable'
        self.empid_field.focus()
        imgPath = cf.GetAppImageDirPath()    
        self.SetImageInLabel(imgPath + 'img.png')
        self.empid_field['state'] = 'normal'
        self.empid_field.delete(0, END)
        self.name_field['state'] = 'normal'
        self.name_field.delete(0, END)
        self.onClickRadioBtnEdit_RFD() 
        if( self.bIsMonthCaldendarShow ):
            self.myCalframe.destroy()
            self.bIsMonthCaldendarShow = False
        self.Total_Days_InMonth.config(text='')
        self.Total_Present_Days.config(text='')
        self.Total_Absent_Days.config(text='')
        self.Total_Holiday_Days.config(text='')
        self.Total_Work_On_Holiday_Days.config(text='')
        ##imgTmp = './/Emp_Tmp_Image//attendance.png'
        imgTmp = cf.Get_Emp_Tmp_Image_Dir() + "//attendance.png"  ## Ajay
        if os.path.isfile(imgTmp):
            os.remove(imgTmp)
         


    def SetImageInLabel(self, sImgPath):
        if(os.path.exists( sImgPath )):
            original = Image.open(sImgPath)
            resized = original.resize((200, 225) ,Image.ANTIALIAS)
            img = ImageTk.PhotoImage( resized )
            self.myImage.configure( image = img )
            self.myImage.image = img

    # def GetEmpInfo_ID_Name_Year(self):
    #     empid_value = self.empid_field.get()
    #     name_value = self.name_field.get()
    #     rdoYear_Value = ""
    #     if( str(radioValue.get()) == "1" ):
    #         rdoYear_Value =  self.monthCmbBox.get()
    #     elif( str(radioValue.get()) == "2" ):
    #         rdoYear_Value = self.yearCmbBox.get() 
    #     Detail_List = [empid_value, name_value, rdoYear_Value]
    #     return Detail_List


    def onBtnClickShowAttendance(self):
        print("onBtnClickShowAttendance...")
        empid_value = self.empid_field.get()
        name_value = self.name_field.get()
        year_Value = "" 
        month_Value = ""
        # if( str(radioValue.get()) == "1" ):
        #     radio_type = "month"
        month_Value =  self.monthCmbBox.get()
        # elif( str(radioValue.get()) == "2" ):
        #     radio_type = "year"
        year_Value = self.yearCmbBox.get()

        if ( (empid_value.strip() == "" ) and ( name_value.strip() == "")  ):
            print("empty input") 
            msg.showinfo(strObj.strMsgTitel, strObj.strFillAtleastOneOption)
        else:
            # to Get emp info from db
            obj = MyMongoDB()

            # first of all check - emp. Attendance is available or not
            bIsEmpExist = obj.Search_EmpID_OR_EmpName_ExistsIn_Attendance_Table(empid_value.strip(), name_value.strip() )
            if(False == bIsEmpExist):
                msg.showinfo(strObj.strMsgTitel, strObj.strMsgSearchUserAttendanceNotAvailable ) 
                return 

            # Second we have to check - emp. Attendance in given Month or Year is available or not
            ###obj.Search_User_Month_Year_ExistsIn_Attendance_Table("", "Ajay", "month", "may")
            #if( str(radioValue.get()) == "1" ):
                # ONLY for Month Wise details
            emp_Attendance_data = obj.Search_User_Month_Year_ExistsIn_Attendance_Table(empid_value.strip(), name_value.strip(), month_Value.strip(), year_Value.strip() )
            nRecordCount = emp_Attendance_data.count()
            if( nRecordCount > 0 ):
                '''
                    '_id': ObjectId('5eef58aab265399555f19bd4'), 
                    'empid': '001', 
                    'name': 'Ajay Sharma', 
                    'department': 'Computer', 
                    'month': 'May', 
                    'year': '2020', 
                    'month_date': '4',   #### current_date
                    'weekday_name': 'Monday', 
                    'complete_date': 'Sunday 21 June 2020', 
                    'time': '06:25:06PM', 
                    'emp_status': 'IN', 
                    'camera_id': '1'
                '''
                emp_att_year = ""
                emp_att_month = ""
                emp_att_name = ""
                emp_att_id = ""
                emp_Attendance_days_list = list()
                for emp_info in emp_Attendance_data:
                    #print(emp_info)
                    emp_att_year = emp_info['year']
                    emp_att_month = emp_info['month']
                    emp_att_name = emp_info['name']
                    emp_att_id =  emp_info["empid"]
                    emp_Attendance_days_list.append( int( emp_info['month_date'] ) )
                
                self.entry_text_empid.set( emp_att_id )
                self.entry_text_name.set( emp_att_name )
                self.myLblMonthCalendar.grid()
                self.myLblMonthCalendar.grid(row = 5  , column = 1, padx = 50, pady = 300)
                
                #to get employee image
                ###---obj.GetEmp_Photo_During_Attendance_Mark( empid_value.strip(), name_value.strip(), emp_att_month.strip())
                ## imgPath = ".\\Emp_Tmp_Image\\attendance.png"
                ###---imgPath = cf.Get_Emp_Tmp_Image_Dir() + "//attendance.png"  ## Ajay

                ## take Emp. photo from table - "Tale_Staff_Info" - COLLECTION_TABLE_STAFF_INFO
                obj.GetEmpDataFromDB(name_value.strip(), empid_value.strip()) 
                imgPath = cf.Get_Emp_Tmp_Image_Dir() + "//0.png"  ## Ajay - by default image

                if os.path.isfile(imgPath):
                    myPhotofrm = PhotoImage(file = imgPath  ) 
                    self.myImage.image = myPhotofrm  
                    self.myImage.configure( image = myPhotofrm  )
                
                self.ShowMonthWise_Attendance(emp_att_year, emp_att_month, emp_Attendance_days_list, empid_value.strip(), name_value.strip(), self.myImage )
                self.btnSearch['state'] = "disable"
                self.btnClear['state'] = "normal"
                self.btnExportData['state'] = 'normal'
            else:
                msg.showerror(strObj.strMsgTitel, strObj.strMsgSearchUserAttendanceNotAvailable)
            # elif( str(radioValue.get()) == "2" ):
            #     #msg.showerror(strObj.strMsgTitel, "Year search... pending" )
            #     #self.myLblYearCalendar.grid()
            #     #self.myLblYearCalendar.grid(row = 5  , column = 1, padx = 50, pady = 300)
            #     self.ShowYearWise_Attendance(empid_value.strip(), name_value.strip(), radio_Value.strip())
            #     self.btnSearch['state'] = "disable"
            #     self.btnClear['state'] = "normal"

            # if(False == bIsEmpExist):
            #     msg.showinfo(strObj.strMsgTitel, strObj.strMsgSearchUserAttendanceNotAvailable ) 
            #     return 
             

    def onBtnClickExportData_Excel(self):
        empid_value = self.empid_field.get()
        name_value = self.name_field.get()
        month_Value =  self.monthCmbBox.get()
        year_Value = self.yearCmbBox.get()

        # export to excel sheet
        obj = MyMongoDB()
        emp_Attendance_data = obj.Get_User_Month_Year_Attendance_Table(empid_value.strip(), name_value.strip(), month_Value.strip(), year_Value.strip() )
        nRecordCount = emp_Attendance_data.count()
        if( nRecordCount > 0 ):
            strExcelFileName = f"{name_value.strip()}_{empid_value.strip()}_{month_Value.strip()}_{year_Value.strip()} "
            strExcelFileName = strExcelFileName.replace(" ", "")
            self.Create_And_Export_Data_In_excel_sheet(strExcelFileName, emp_Attendance_data)
            
    
  
    def Create_And_Export_Data_In_excel_sheet(self, excel_file_name, empAttendanceData):
        # opening the existing excel file 
        ##exportDir = cf.GetExportDirName()
        ##strFilePath = f"{exportDir}\\{excel_file_name}.xlsx"

        ## here we open dialog box to save export file
        ##from tkinter.filedialog import asksaveasfile 
        ##from tkinter.filedialog import askopenfilename
        
        files = [('Excel File', '*.xlsx') ] 
        file = asksaveasfile(   filetypes = files, defaultextension = files, title="Save the file" ) 
        
        ##file = asksaveasfilename( initialdir = f"{excel_file_name}" , filetypes = files, defaultextension = files, title="Save the file" ) 
        
        if file is None: # asksaveasfile return `None` if dialog closed with "cancel".
            self.btnExportData['state'] = 'normal'
            return         
        else:
            self.btnExportData['state'] = 'disable'
            strFilePath = file.name         
        ##--------------------------------------------

        workbook = xlsxwriter.Workbook( strFilePath ) 
        # create the sheet object 
        worksheet = workbook.add_worksheet("Attendance")
       

        # write given data to an excel spreadsheet at particular location 
        row = 0
        column=1
        worksheet.write(row, column, 'Emp_ID' ) 
        column += 1 
        worksheet.write(row, column , "Emp_Name" ) 
        column += 1 
        worksheet.write(row, column , "Department" ) 
        column += 1 
        worksheet.write(row, column , "Month") 
        column += 1 
        worksheet.write(row, column , "Year") 
        column += 1 
        worksheet.write(row, column , "Week Day") 
        column += 1 
        worksheet.write(row, column , "Date") 
        column += 1 
        worksheet.write(row, column , "Time") 
        column += 1 
        worksheet.write(row, column , "Employe Status" ) 
        column += 1 
        worksheet.write(row, column  , "Camera ID" ) 
        column += 1 
        worksheet.write(row, column  , "Month Day" )

        # assigning the max row and max column value upto which data is written in an excel sheet to the variable 
        row = 1
        column=1
        for emp_info in empAttendanceData:
            # get method returns current text as string which we write into excel spreadsheet at particular location 
            worksheet.write(row, column,  emp_info['empid']  )  
            column += 1 
            worksheet.write(row, column,  emp_info['name']  )  
            column += 1 
            worksheet.write(row, column,  emp_info['department']  ) 
            column += 1  
            worksheet.write(row, column,  emp_info['month']  )  
            column += 1 
            worksheet.write(row, column,  emp_info['year']  )  
            column += 1 
            worksheet.write(row, column,  emp_info['weekday_name']  )  
            column += 1 
            worksheet.write(row, column,  emp_info['complete_date'] )  
            column += 1 
            worksheet.write(row, column,  emp_info['time']  )  
            column += 1 
            worksheet.write(row, column,  emp_info['emp_status'] )  
            column += 1 
            worksheet.write(row, column ,  emp_info['camera_id'] )  
            column += 1 
            worksheet.write(row, column ,  emp_info['month_date']  ) 
            row += 1
            column = 1
        
        # save the file 
        workbook.close()

    def onBtnClickExportAllData_Excel(self):
        print("onBtnClickExportAllData_Excel")
        # export to excel sheet
        month_Value =  self.monthCmbBox.get()
        year_Value = self.yearCmbBox.get()
        
        strFilePath = ""
        files = [('Excel File', '*.xlsx') ] 
        file = asksaveasfile(   filetypes = files, defaultextension = files, title="Save the file" ) 
        if file is None: # asksaveasfile return `None` if dialog closed with "cancel".
            #self.btnExportData['state'] = 'normal'
            return         
        else:
            #self.btnExportData['state'] = 'disable'
            strFilePath = file.name  

            workbook = xlsxwriter.Workbook( strFilePath ) 
        # create the sheet object 
        worksheet = workbook.add_worksheet("Attendance")
       

        # write given data to an excel spreadsheet at particular location 
        row = 0
        column=1
        worksheet.write(row, column, 'Emp_ID' ) 
        column += 1 
        worksheet.write(row, column , "Emp_Name" ) 
        column += 1 
        worksheet.write(row, column , "Department" ) 
        column += 1 
        worksheet.write(row, column , "Month") 
        column += 1 
        worksheet.write(row, column , "Year") 
        column += 1 
        worksheet.write(row, column , "Week Day") 
        column += 1 
        worksheet.write(row, column , "Date") 
        column += 1 
        worksheet.write(row, column , "Time") 
        column += 1 
        worksheet.write(row, column , "Employe Status" ) 
        column += 1 
        worksheet.write(row, column  , "Camera ID" ) 
        column += 1 
        worksheet.write(row, column  , "Month Day" )

      
        row = 1
        column=1

        obj = MyMongoDB()
        all_emp_data = obj.Get_AllEmpData_Month_Year_Attendance( month_Value.strip(), year_Value.strip() )
        for eid in all_emp_data:
            row += 1
            for emp_info in all_emp_data[eid]:
                # get method returns current text as string which we write into excel spreadsheet at particular location 
                worksheet.write(row, column,  emp_info['empid']  )  
                column += 1 
                worksheet.write(row, column,  emp_info['name']  )  
                column += 1 
                worksheet.write(row, column,  emp_info['department']  ) 
                column += 1  
                worksheet.write(row, column,  emp_info['month']  )  
                column += 1 
                worksheet.write(row, column,  emp_info['year']  )  
                column += 1 
                worksheet.write(row, column,  emp_info['weekday_name']  )  
                column += 1 
                worksheet.write(row, column,  emp_info['complete_date'] )  
                column += 1 
                worksheet.write(row, column,  emp_info['time']  )  
                column += 1 
                worksheet.write(row, column,  emp_info['emp_status'] )  
                column += 1 
                worksheet.write(row, column ,  emp_info['camera_id'] )  
                column += 1 
                worksheet.write(row, column ,  emp_info['month_date']  ) 
                row += 1
                column = 1
        
        # save the file 
        workbook.close()







 
def myAttendanceSystemMain(root):
    
    MyAttendanceSystemPage(root)
    

if __name__ == "__main__" :
    root = Tk()
    root.geometry("960x640")
    root.title( "strApptitle" )     
    root.resizable(False, False)
    root.configure(background="black" )

    myAttendanceSystemMain(root)

    root.mainloop()


