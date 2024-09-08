# -*- coding: utf-8 -*-
# Modal dialog window with Progressbar for the bigger project
import time
import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
import time
import common_fun as cf 
import os.path
from os import path
from urllib.parse import urlparse
 
import threading
import multiprocessing
import urllib.request, io
#import subprocess as sp	
from urllib import request

from urllib.request import urlopen

class MainGUI(ttk.Frame):
    ''' Main GUI window '''
    def __init__(self, master):
        ''' Init main window '''
        ttk.Frame.__init__(self, master=master)
        self.master.title('Main GUI')
        self.master.geometry('300x200')
        self.lst = [
            'Bushes01.png',  'Bushes02.png', 'Bushes03.png', 'Bushes04.png', 'Bushes05.png',
            'Forest01.png',  'Forest02.png', 'Forest03.png', 'Forest04.png', 'Road01.png',
            'Road02.png',    'Road03.png',   'Lake01.png',   'Lake02.png',   'Field01.png']
        b = ttk.Button(self.master, text='Start', command=self.start_progress)
        b.pack()
        b.focus_set()

    def start_progress(self):
        ''' Open modal window '''
        s = ProgressWindow(self, 'MyTest', self.lst)  # create progress window
        self.master.wait_window(s)  # display the window and wait for it to close


class ProgressWindow(simpledialog.Dialog):
    def __init__(self, parent, name, lst):
        ''' Init progress window '''
        tk.Toplevel.__init__(self, master=parent)
        self.name = name
        self.lst = lst
        self.length = 400

        self.myParent = parent
        #
        self.create_window()
        self.create_widgets()

    def create_window(self):
        ''' Create progress window '''
        self.focus_set()  # set focus on the ProgressWindow
        self.grab_set()  # make a modal window, so all events go to the ProgressWindow
        self.transient(self.master)  # show only one window in the task bar
        #
        self.title(u'New Setup is {}'.format(self.name))
        self.resizable(False, False)  # window is not resizable
        # self.close gets fired when the window is destroyed
        self.protocol(u'WM_DELETE_WINDOW', self.close)
        # Set proper position over the parent window
        dx = (self.master.master.winfo_width() >> 1) - (self.length >> 1)
        dy = (self.master.master.winfo_height() >> 1) - 50
        self.geometry(u'+{x}+{y}'.format(x = self.master.winfo_rootx() + dx,
                                         y = self.master.winfo_rooty() + dy))
        self.bind(u'<Escape>', self.close)  # cancel progress when <Escape> key is pressed

    def create_widgets(self):
        ''' Widgets for progress window are created here '''
        self.var1_FName = tk.StringVar()
        self.var2_FCount = tk.StringVar()
        self.num_ProgressBar = tk.IntVar()
        self.maximum =   len(self.lst)
        self.tmp_str = ' / ' + str(self.maximum)
        #
        # pady=(0,5) means margin 5 pixels to bottom and 0 to top
        ttk.Label(self, textvariable=self.var1_FName).pack(anchor='w', padx=2)
        
        #self.progress = ttk.Progressbar(self, maximum=self.maximum, orient='horizontal', length=self.length, variable=self.num_ProgressBar, mode='determinate')
        #self.progress.pack(padx=2, pady=2)

        self.progress = ttk.Progressbar(self, maximum=self.maximum, orient='horizontal', length=self.length, mode='determinate')
        self.progress.pack(padx=2, pady=2)
        self.progress.start(25)


        ttk.Label(self, textvariable=self.var2_FCount).pack(side='left', padx=2)
        ttk.Button(self, text='Cancel', command=self.close).pack(anchor='e', padx=1, pady=(0, 1))
        #
        self.next()

        # self.do_something_with_file(2, self.lst[0]) 
        # wait_window( self.myParent )

        
        

    def next(self):
        ''' Take next file from the list and do something with it '''
        n = self.num_ProgressBar.get()
        
        if( n == 0):
            self.do_something_with_file(n+1, self.lst[n])  # some useful operation
        else:
            self.master.wait_window(  self.do_something_with_file(n+1, self.lst[n])   )

        self.var1_FName.set('File name: ' + self.lst[n])
        n += 1
        self.var2_FCount.set(str(n) + self.tmp_str)
        self.num_ProgressBar.set(n)

        if n < self.maximum:
            
            self.after(500, self.next)  # call itself after some time  
        else:
            self.close()  # close window


    def do_something_with_file(self, number, name):
        print(number, name)
        if(name == ""):
            return

        
        # Start Downloading file....
        dwn_url = name
        tmp = urlparse( dwn_url )         
        location_ToSave_setup  = cf.GetAppDataFolderPath() 
        setup_file_name = os.path.basename( tmp.path )     
        
        self.var1_FName.set('Downloading File name: ' +  setup_file_name )  
        self.var2_FCount.set( "Please wait while the Setup is being downloaded. This might take several minutes.") 
          
        # Use to Download from net
        # urllib.request.urlretrieve(dwn_url, location_ToSave_setup + setup_file_name) 
        
        self.thread = threading.Thread(target= self.DownloadInThread( dwn_url, location_ToSave_setup + setup_file_name) )
        self.thread.start()
        self.thread.join()
         
    def Update_UI_Download_Info(self, blocknum, blocksize, totalsize):
        # Ajay: Show download file info.
        readsofar = blocknum * blocksize
        if totalsize > 0:
            percent = readsofar * 1e2 / totalsize
            # s = "\r%5.1f%% %*d / %d" % ( percent, len(str(totalsize)), readsofar, totalsize)
            # sys.stderr.write(s)

            download_in_percentage  = "%5.1f%% (%*d / %d)" % ( percent, len(str(totalsize)), readsofar, totalsize)

            dwn_percentage = f"Download in Percentage: { download_in_percentage } "
            print(f"{dwn_percentage}")
            self.var2_FCount.set( dwn_percentage ) 
            if( readsofar >= totalsize ): # near the end
                # sys.stderr.write("\n")
                strComp = "Downloading process finished successfully"
                print(f"strComp")
                self.var2_FCount.set(strComp)
            else: # total size is unknown
                # sys.stderr.write("read %d\n" % (readsofar,))
                strTmp = f"Download file size = {readsofar}"
                print(strTmp)
                self.var1_FName.set( strTmp )

    # import sys
    def download_reporthook(self, blocknum, blocksize, totalsize):
        myDwnInfoThrd = threading.Thread(target= self.Update_UI_Download_Info(blocknum, blocksize, totalsize) )
        myDwnInfoThrd.start()
        myDwnInfoThrd.join()

        # readsofar = blocknum * blocksize
        # if totalsize > 0:
        #     percent = readsofar * 1e2 / totalsize
        #     s = "\r%5.1f%% %*d / %d" % ( percent, len(str(totalsize)), readsofar, totalsize)
        #     # sys.stderr.write(s)
        #     print(f"Ajay 1- s = {s}")
        #     self.var2_FCount.set( str(s) )
        #     if( readsofar >= totalsize ): # near the end
        #         # sys.stderr.write("\n")
        #         print(f"Ajay 3 Complete downloading... ")
        #     else: # total size is unknown
        #         # sys.stderr.write("read %d\n" % (readsofar,))
        #         print(f"Ajay 2 - read per % = {readsofar}")


    def DownloadInThread(self, dwn_url, dst_path):

        urllib.request.urlretrieve(dwn_url,  dst_path , self.download_reporthook )
       
        # path = urllib.request.urlopen(dwn_url)
        # meta = path.info()
        # file_size = meta.get(name="Content-Length")
        # print(f"Download file size = {file_size}")


        # resp = urllib.request.urlopen(dwn_url)
        # with open(dst_path, 'wb') as f:
        #     f.write(resp.read())
        #     file_size = f.get(name="Content-Length")
        #     print(f"Download file size = {file_size}")



    def get_file_size(self, url):
        r = request.Request(url)
        r.get_method = lambda : 'HEAD'
        response = request.urlopen(r)
        length = response.getheader("Content-Length")
        return int(length)

    def close(self, event=None):
        # # Terminate the process
        # self.proc.terminate()     
        
        # self.thread._stop()

        ''' Close progress window '''
        if self.progress['value'] == self.maximum:
            print('Ok: process finished successfully')
        else:
            print('Cancel: process is cancelled')
                
        self.master.focus_set()  # put focus back to the parent window
        self.destroy()  # destroy progress window

# root = tk.Tk()
# feedback = MainGUI(root)
# root.mainloop()


def myMainPage(root):    
    MainGUI(root)
 

if __name__ == "__main__" :
    root = tk.Tk()
    feedback = myMainPage(root)     
    root.mainloop()


