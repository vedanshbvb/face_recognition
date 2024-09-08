from tkinter import *
import tkinter
import cv2
import PIL.Image, PIL.ImageTk
import time
import common_fun as cf
import os
import tkinter as tk 
from PIL import Image, ImageDraw 
import threading
from PIL import Image
from PIL import ImageTk
from AllStrings import myStrings
import datetime
import tkinter.messagebox as msg
import face_recognition
 

myAppBGColor =  "lavender blush" #  "grey" 
myFont = "Helvetica"
myHeadingTxtFontSize = 15
myTxtFontSize = 10
myTxtColor = "black" # "white"
myBtnBGColor= "lavender blush" # "Green"
myBorderColor = "medium violet red"
myBtnTxtColor = "white"
PHOTO_CIRCLE_INCRESE_BY = 20

strObj  = myStrings()


class mainThreadMyPhotoCamera(threading.Thread):
    def __del__(self):
        print("Bye mainThreadMyPhotoCamera")
    def __init__(self, MyPhotoAppPage):
        print("Hi mainThreadMyPhotoCamera")
        threading.Thread.__init__(self)
        self.stop_threads = False
        self._stop_event = threading.Event()

        self.panel = None
        self.gui = MyPhotoAppPage
        self.face_Photo_count = 0  
        self.stop_count = 0

    def stop(self):
        print("T: Stop method called...")
        self.stop_threads = True
        self._stop_event.set()
    def stopped(self): 
        return self._stop_event.is_set()
        
    def SaveEmployePhotoInFolder(self, im_face):         
        new_path = self.gui.save_new_photo_path + "\\" + str( self.face_Photo_count )+ ".png"   

        # Save the captured image into the datasets folder
        ####cv2.imwrite(new_path, im_face   )
        ## to solve Blue color in image during save 
        cv2.imwrite(new_path, cv2.cvtColor( im_face, cv2.COLOR_RGB2BGR)   ) 

        # ----------- this code on 14Sep2020-------------------------------------------------------
        if os.path.exists( new_path ):
            # if photo is not good quality than show msg box for proper lighting 
            image = face_recognition.load_image_file(new_path)
            face_bounding_boxes = face_recognition.face_locations(image) # , model="cnn"
            if len(face_bounding_boxes) != 1:
                ### delete this image file -------------- 
                if os.path.exists( new_path ):
                    os.remove( new_path )
                    self.gui.bIsSavePhoto = False                    
                    self.stop_count -= PHOTO_CIRCLE_INCRESE_BY
                    msg.showinfo(strObj.strMsgTitel, strObj.strImproveProperLight_CameraQuality  )
                    return
                ###--------------------------------------
        # ------------------------------------------------------------------


        print(f"save image...{new_path}")
        self.gui.bIsSavePhoto = False

    def run(self):
        print("Connecting to Photo camera...")
        strFaceFile  = cf.GetFilePath_Haarcascade_frontalface()
        face_detector = cv2.CascadeClassifier( strFaceFile )

        self.cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        if not self.cam.isOpened():
            print( strObj.strInputCam ) # print('Cannot open Input Camera')
            msg.showinfo(strObj.strMsgTitel, strObj.strCamerNotFound )
            self.cam.release() 
            #exit()
            return
        self.cam.set(3, 640) # set video widht
        self.cam.set(4, 480) # set video height
        self.cam.set(10, 100) # screen brightness
        # Define min window size to be recognized as a face
        minW =  0.1*self.cam.get(3)
        minH =  0.1*self.cam.get(4)

        try: 
            while(1): # (not self._stop_event.is_set()):
                global stop_threads
                if self.stop_threads:
                    print("bool - While Loop break")
                    self.cam.release()
                    break
                if self.stopped(): 
                    print("fun stopped() --While Loop break--stopped---")
                    self.cam.release()
                    break
                self.ret, self.camImg =self.cam.read()
                if not self.ret:
                    print('Cannot receive frame from input camera')
                    self.cam.release()
                    break
                gray = cv2.cvtColor(self.camImg, cv2.COLOR_BGR2RGB ) ## COLOR_BGR2GRAY   
                # Resize frame of video to 1/4 size for faster face recognition processing
                small_frame = cv2.resize(self.camImg, (0, 0), fx=0.25, fy=0.25)
                # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
                rgb_small_frame = small_frame[:, :, ::-1]
                # to show blackAndWhiteFrame
                #(thresh, frame) = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)        
                faces = face_detector.detectMultiScale( 
                    gray,
                    scaleFactor = 1.1,
                    minNeighbors = 5,
                    minSize = (int(minW), int(minH)),
                )
                # this is used to detect the face which 
                faces = faces[:1]
                if len(faces) == 1:
                    # this is removing from tuple format       
                    face = faces[0]
                    # storing the coordinates of the 
                    # face in different variables 
                    x, y, w, h = face  
                    ##print(f"{x} - {y} , {w} - {h}")
                    
                    # this is will show the face that is being detected      
                    im_face = gray[y-10:y + h+10, x-1:x + w+1]
                    ####im_face = gray[:, :, :: -1 ] ## full image

                    x = int( w/2+x )
                    y = int( h/2+y  )

                    # Ellipse parameters
                    radius = 170
                    center = ( x , y )
                    axes = (radius, radius)
                    angle = -90
                    startAngle = 0
                    startAngle +=   360 + self.stop_count   ##360-face_count
                    endAngle =  360 
                    # When thickness == -1 -> Fill shape
                    thickness = 3
                    # Draw Green progress bar circle
                    cv2.ellipse(self.camImg , center, axes, angle, startAngle, endAngle, (0, 255, 0), thickness)
                    # fix circle
                    startAngle = 0
                    endAngle = 360
                    thickness = 1
                    axes = (radius - 5, radius - 5)
                    # # Draw a bit smaller Blue half circle
                    cv2.ellipse(self.camImg, center, axes, angle, startAngle, endAngle, (255, 0, 0), thickness)
                    #cv2.imshow("test", self.frame_Photo) # cv2.COLOR_RGB2BGR
                    ##cv2.imshow( "opop", cv2.cvtColor(self.camImg, cv2.COLOR_RGB2BGR))
                    
                    if(self.gui.bIsSavePhoto ):
                        self.SaveEmployePhotoInFolder(im_face)
                        #new_photo_fpath = self.gui.save_new_photo_path + "\\" + str( self.face_Photo_count )+ ".png"   
                        #cv2.imwrite(new_photo_fpath, cv2.cvtColor(im_face, cv2.COLOR_RGB2BGR))
                        #self.gui.bIsSavePhoto = False

                
                self.image1 = cv2.cvtColor(self.camImg,cv2.COLOR_BGR2RGB)
                self.image2 = Image.fromarray(self.image1)
                self.image3 = ImageTk.PhotoImage(self.image2)
                # if the panel is not None, we need to initialize it
                if self.panel is None:
                    ##--self.gui.panel = tk.Label(image=self.image3)
                    self.panel = Label(self.gui.frame , image=self.image3)
                    self.panel.image = self.image3
                    self.panel.pack(side="right", padx=50, pady=0)
                # otherwise, simply update the panel
                else:
                    self.panel.configure(image=self.image3)
                    self.panel.image = self.image3 

        finally: 
            print('ended')   
            #objRepeatTimer.stop()  



class MyPhotoAppPage(tk.Frame):
    def __del__(self):
        print("Bye MyPhotoAppPage-photo")    

    def __init__(self, tkFrame, Parent=None):
        #self._frame = None
        tk.Frame.__init__(self, tkFrame, Parent)

        self.myParent = Parent  
        self.myroot = tkFrame
        
        self.myParent.myParent.bPlsStopCameraBeforeMoveNextPage = True

        self.camera_thread = mainThreadMyPhotoCamera(self)
        self.camera_thread.setName("mycamera_thread")
        self.camera_thread.start()

        self.frame = tk.Frame(tkFrame, width=385, height=460, borderwidth=1, bg= myAppBGColor , relief=SUNKEN   )
        self.frame.place(x=200-4, y=1, anchor="nw", width=758+6, height=621-1)
        self.panel = None

        self.myroot.grid_columnconfigure((0,1), weight=1)

        xLblVal = 80
        yVal = 32
        ctrlHeight = 2
        ctrlWidth = 80

        # Heading...
        self.heading = Label(self.frame, text= strObj.strPhotoPageHeading  , fg=myTxtColor, bg=myAppBGColor, font=(myFont, myHeadingTxtFontSize), compound="left" , justify=LEFT, anchor=W)
        self.heading.configure(height=ctrlHeight, width=ctrlWidth)
        self.heading.place(x=xLblVal,y=32)

        imgPath = cf.GetAppImageDirPath() 
        # rounded_btn_dark.png        
        btnImg_N0 = imgPath + "rounded_btn_dark.png"
        self.img_N0=PhotoImage(file=btnImg_N0 ) 
        ctrlHeight_New = 36
        ctrlWidth_New = 180

        # Take Photo Button
        xbtnVal = 300 + 20
        yBtnVal = 564
        self.btnClose = Button(self.frame , image=self.img_N0, text= strObj.strBtnClose , command=self.onBtnClose , justify = RIGHT, fg=myBtnTxtColor, font=(myFont, myTxtFontSize) , bg=myBtnBGColor , border=0,   highlightthickness = 0, borderwidth = 0 )
        self.btnClose.configure(  height=ctrlHeight_New, width=ctrlWidth_New, compound=CENTER )
        self.btnClose.place(x=xbtnVal, y=yBtnVal)         

        
        btnImg_N01 = imgPath + "rounded_btn.png"
        self.img_N01=PhotoImage(file=btnImg_N01 ) 
        xbtnVal = 540
        yBtnVal = 564
        self.btnTakePhoto = Button(self.frame, image=self.img_N01, text= strObj.strTakePhoto , command=self.onBtnTakePhoto , justify = RIGHT, fg=myBtnTxtColor, font=(myFont, myTxtFontSize) , bg=myBtnBGColor , border=0,   highlightthickness = 0, borderwidth = 0)
        self.btnTakePhoto.configure( height=ctrlHeight_New, width=ctrlWidth_New, compound=CENTER )
        self.btnTakePhoto.place(x=xbtnVal, y=yBtnVal)         


        self.bIsSavePhoto = False
        dept_value = self.myParent.dept_field.get()
        name_value = self.myParent.name_field.get()
        empid_value = self.myParent.empid_field.get()
        self.SetEmpDetails( dept_value  , name_value, empid_value )

    def SetEmpDetails(self, emp_dpt1, emp_name1, emp_empID1):
        self.emp_dpt = emp_dpt1.strip()
        self.emp_name = emp_name1.strip()
        self.emp_empID = emp_empID1.strip()

    def onBtnTakePhoto(self):  
        ## folder name =>used in page_addrecord.py, mongo_db.py, takeempphotopage.py, page_facerecognition.py
        if( self.emp_name.find(" ") > 0 ):
            nameTmp = self.emp_name.replace(" ", "_")
        else:
            nameTmp = self.emp_name.strip()
        if( self.emp_dpt.find(" ") > 0 ):
            depTmp = self.emp_dpt.replace(" ", "_")
        else:
            depTmp = self.emp_dpt.strip()
        ##self.strFileName = self.emp_empID.strip()  +"-" + self.emp_name.strip() + "-" + self.emp_dpt.strip()
        self.strFileName = self.emp_empID.strip()  +"-" + nameTmp  + "-" + depTmp
        self.save_new_photo_path =  cf.GetFilePath_StaffImages() + "\\" + self.strFileName 


        self.bIsSavePhoto = True
        self.camera_thread.face_Photo_count +=1
        self.camera_thread.stop_count += PHOTO_CIRCLE_INCRESE_BY
        if self.camera_thread.stop_count > 360: # Take 30 face sample and stop video
            print("Stop photo Capturing....")
            self.camera_thread.stop()
            msg.showinfo(strObj.strMsgTitel, strObj.strMsgEmpPhotoComplete )
            self.btnTakePhoto['state'] = 'disable'


 
        if not os.path.exists(self.save_new_photo_path):
            os.makedirs(self.save_new_photo_path)
            print(f"Create folder to save image in = {self.save_new_photo_path}")

        # after taking image - display same image in label
        empPhoto_value = self.save_new_photo_path + "\\" +  '1.png' 
        if os.path.exists(empPhoto_value):
            self.myParent.SetImageInLabel( empPhoto_value  )         
        
    def onBtnClose(self):
        print("Bye MyPhotoAppPage-photo")
        self.camera_thread.stop()
        self.myParent.myParent.bPlsStopCameraBeforeMoveNextPage = False
        ##time.sleep(3.0)
        msg.showinfo(strObj.strMsgTitel, strObj.strMsgStopEmpPhoto )
        self.frame.destroy()



def StartPhotoCaptureMain(root):
    MyPhotoAppPage(root)
	

if __name__ == "__main__" :
	
    root = Tk()
    root.geometry("960x640")
    root.title( "strApptitle" )     
    root.resizable(False, False)
    root.configure(background="black" )

    #myFaceRecognitionMain(root)
    StartPhotoCaptureMain(root)

    root.mainloop()

#test_photo_btn_click