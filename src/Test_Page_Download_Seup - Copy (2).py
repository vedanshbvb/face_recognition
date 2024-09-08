from tkinter import *
import sys
from threading import Event, Thread
from tkinter import Tk, ttk
from urllib.request import urlretrieve

import tkinter as tk
from tkinter import simpledialog
import subprocess as sp	



myPrgBarPer = 0
 
def Download_MySetup( url, filename):
    

    root = progressbar = quit_id = lblDwnInfo  = None
    ready = Event()

    # def onBtnClickStop():
    #     print("Stop")
    #     root.destroy()
    #     #root.quit()
    #     print("close GUI")


    def reporthook(blocknum, blocksize, totalsize):
        nonlocal quit_id
        if blocknum == 0: # started downloading
            def guiloop():
                nonlocal root, progressbar, lblDwnInfo
                root = Tk()
                root.withdraw() # hide

                ## to bring top most 
                root.call('wm', 'attributes', '.', '-topmost', True)

                root.geometry("500x200")
                root.title( "Download Setup File" )     
                root.resizable(False, False)
                root.configure(background="pink" )

                # 1. Row 1 - 
                 
                lblDwnInfo = Label(root, text= "Download Info"  ) # , fg=myTxtColor, bg=myAppBGColor, font=(myFont, myTxtFontSize), justify=LEFT, anchor=W    )
                lblDwnInfo.configure(height=1, width=50)
                lblDwnInfo.place(x=10,y=20) 


                global myPrgBarPer 
                progressbar = ttk.Progressbar(root, length=400, variable= myPrgBarPer )
                progressbar.place(x=10,y=50)
                # progressbar.grid()

                # btnStop_btn = Button( root, text="Stop",  command=onBtnClickStop , justify = LEFT ) # , fg=myBtnTxtColor, font=(myFont, myTxtFontSize) , bg=myBtnBGColor, border=0,   highlightthickness = 0, borderwidth = 0  )
                # btnStop_btn.configure( height=1, width=20  ) # , compound=CENTER
                # btnStop_btn.place(x=200, y=100) 



                # show progress bar if the download takes more than .5 seconds
                root.after(500, root.deiconify)
                ready.set() # gui is ready
                root.mainloop()
            Thread(target=guiloop).start()
        ready.wait(1) # wait until gui is ready
        percent = blocknum * blocksize * 1e2 / totalsize # assume totalsize > 0
        if quit_id is None:
            #---root.title('%%%.0f %s' % (percent, filename,))
            progressbar['value'] = percent # report progress
            myPrgBarPer = percent

            ## ------------------------------------------------------------------
            readsofar = blocknum * blocksize
            my_percent = readsofar * 1e2 / totalsize
            #--download_in_percentage  = "%5.1f%% (%*d / %d)" % ( my_percent, len(str(totalsize)), readsofar, totalsize)
            download_in_percentage  = "%5.1f" % ( my_percent  )
            strTmp = f"Total Download percentage: {download_in_percentage}"
            lblDwnInfo.config(text= strTmp)
            ## ------------------------------------------------------------------

            if percent >= 100:  # finishing download
                
                process = sp.Popen( filename, shell=True)
                process.wait() 

                quit_id = root.after(0, root.destroy) # close GUI

    return urlretrieve(url, filename, reporthook)

    


dwn_url = "http://vervelogic.a2hosted.com/frsetup/frsetup.exe"
dst_path = "C:\\Users\\abc\\AppData\\Roaming\\FR_Update\\frsetup.exe"
# Ok Done
# Download_MySetup(dwn_url, dst_path )


# def myMainPage(root):    
#     MainGUI(root)
 

# if __name__ == "__main__" :
#     root = tk.Tk()
#     feedback = myMainPage(root)     
#     root.mainloop()
 