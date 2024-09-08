  
#from tkinter import Tk, Label, Button

from tkinter import *
from AllStrings import myStrings
import common_fun as cf 
import tkinter.messagebox as msg
import time
import tkinter.font as font
 
import tkinter as tk
from cv2 import cv2
import cv2
import os
import common_fun as cf
import numpy as np
import math
from PIL import Image, ImageDraw 
import threading
from PIL import Image
from PIL import ImageTk
#import Tkinter as tki
import imutils
# import time
from AllStrings import myStrings
from sklearn import neighbors
import os.path
import pickle
import face_recognition
from face_recognition.face_recognition_cli import image_files_in_folder
from os.path import dirname
from os.path import abspath
from sklearn import metrics
import StartSystemImageTraining as st
import itertools

# import datetime
import datetime
import time as t

from Mongo_DB import MyMongoDB
import winsound

from math import hypot
import dlib

from scipy.spatial import distance
from imutils import face_utils


# To Detection liveness Face - import the necessary packages





myAppBGColor =  "lavender blush" #   "grey" 
myFont = "Helvetica"
myHeadingTxtFontSize = 15
myTxtFontSize = 10
myTxtColor =   "black" #  "white"
myBtnBGColor= "lavender blush" # "Green"
myBorderColor = "medium violet red"
myBtnTxtColor = "white"


strObj  = myStrings()

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

###------new add---------------------------
import datetime
from datetime import *
class CountsPerSec:
    """
    Class that tracks the number of occurrences ("counts") of an
    arbitrary event and returns the frequency in occurrences
    (counts) per second. The caller must increment the count.
    """
    def __init__(self):
        self._start_time = None
        self._num_occurrences = 0
    def start(self):
        self._start_time = datetime.now()
        return self
    def increment(self):
        self._num_occurrences += 1
    def countsPerSec(self):
        elapsed_time = (datetime.now() - self._start_time).total_seconds()
        return self._num_occurrences / elapsed_time
############---------------------------------------------------------------------------------
      

##//**********************
from threading import Timer
class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        print("1. ini -- RepeatedTimer")
        self._timer     = None
        self.interval   = interval
        self.function   = function
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
        self.start()
    def _run(self):
        print("2. run -- RepeatedTimer")
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)
    def start(self):
        if not self.is_running:
            print("3. start -- RepeatedTimer")
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True
    def stop(self):
        print("4. Stop -- RepeatedTimer")
        self._timer.cancel()
        self.is_running = False

     
##//**********************

class mainThreadMyCamera(threading.Thread):
    def __del__(self):
        print("Bye mainThread")
    def __init__(self, MyFaceRecognitionPage):
        print("Hi mainThread")
        threading.Thread.__init__(self)
        self.stop_threads = False
        self._stop_event = threading.Event()

        self.panel = None
        self.live_face_green_color = False
        self.eyes_detected = dict()


        self.gui = MyFaceRecognitionPage  

        global dict_presentMarked
        self.dict_presentMarked = {}
        self.strObj = myStrings()    
           

    def compare_predict_result(self, X_img, knn_clf=None, model_path=None, distance_threshold=0.4):

        ## Ajay
        ## check file size should greater than 0,  model_path = 'trained_knn_model.clf'
        ## file size zero means user not train the system with employee images 
        fileSize = os.path.getsize(model_path)
        if( fileSize == 0 ):
            msg.showerror(strObj.strMsgTxt_Title, strObj.strMsgTxt_PlsTraingTheSystem)
            return [], False

        """
        With the score threshold 0.6 for asian faces data samples, the classifier will recognize different people with the same label.
        I obtain the better result by setting the distance_threshold = 0.4  or = 0.6
        Recognizes faces in given image using a trained KNN classifier
        :param X_img_path: path to image to be recognized
        :param knn_clf: (optional) a knn classifier object. if not specified, model_save_path must be specified.
        :param model_path: (optional) path to a pickled knn classifier. if not specified, model_save_path must be knn_clf.
        :param distance_threshold: (optional) distance threshold for face classification. the larger it is, the more chance
            of mis-classifying an unknown person as a known one. 
        :return: a list of names and face locations for the recognized faces in the image: [(name, bounding box), ...].
            For faces of unrecognized persons, the name 'unknown' will be returned.
        """     
        if knn_clf is None and model_path is None:
            raise Exception("Must supply knn classifier either thourgh knn_clf or model_path")
        # Load a trained KNN model (if one was passed in)
        if knn_clf is None:
            with open(model_path, 'rb') as f:  ## 'trained_knn_model.clf'
                knn_clf = pickle.load(f)  ## No module named 'sklearn.neighbors._classification'
        
        # X_face_locations = face_recognition.face_locations(X_img, number_of_times_to_upsample=0, model="hog") # , model="cnn"

        ##print(f"my X_img ====> {X_img}")

        X_face_locations = face_recognition.face_locations(X_img)

        ##print(f"my X_face_locations ====> {X_face_locations}")

        # If no faces are found in the image, return an empty result.
        if len(X_face_locations) == 0:
            ###---print( self.strObj.strNoFaceFound ) # print("No face found...")
            return [], True
        # Find encodings for faces in the test iamge
        faces_encodings = face_recognition.face_encodings(X_img, known_face_locations=X_face_locations)
        # Use the KNN model to find the best matches for the test face
        closest_distances = knn_clf.kneighbors(faces_encodings, n_neighbors=1)
        are_matches = [closest_distances[0][i][0] <= distance_threshold for i in range(len(X_face_locations))]
        # Predict classes and remove classifications that aren't within the threshold
        sUnknown =  self.strObj.strUnknown # "unknown"
        return [(pred, loc) if rec else ( sUnknown, loc) for pred, loc, rec in zip(knn_clf.predict(faces_encodings), X_face_locations, are_matches)], True

    def myFunToRemoveEmpNameAfterSetTime(self, tmp_name ):
        # If key exist in dictionary then delete it using del.
        if myEmpNameForAtt_Mark in self.dict_presentMarked :
            print(f"Remove Name After 30 sec = {myEmpNameForAtt_Mark}, to Re-Mark-Attendance")
            del self.dict_presentMarked[myEmpNameForAtt_Mark]  

        self.live_face_green_color = False
        print(f"After 15sec = {self.live_face_green_color}")

        empId_Name_dep = myEmpNameForAtt_Mark.split( "-")
        empName = empId_Name_dep[1]
        self.eyes_detected[empName] = 'None'


    def Mark_Attendance(self, name, emp_photo):                    
        '''
        check name in Dictionary - dict_presentMarked
        if not present in dict:
            add name in this dict {name , "present"}
        else:
            check key_name ==> value
            if not mark present:
                mark present
        '''
        #presentMarked.add( name, "Present" )
        if name not in self.dict_presentMarked:
            self.dict_presentMarked[name] =  self.strObj.strPresent  # = "Present"
            strTmp = name.split('-')  
            strEmpID  = strTmp[0] 
            strName = strTmp[1] 
            strclass_dept = strTmp[2] 

            ## folder name =>used in page_addrecord.py, mongo_db.py, takeempphotopage.py, page_facerecognition.py
            #strName = strName.replace("_", " ")
            #strclass_dept = strclass_dept.replace("_", " ") 
            if( strName.find("_") > 0 ):
                strName = strName.replace("_", " ")
            else:
                strName = strName.strip()
            if( strclass_dept.find("_") > 0 ):
                strclass_dept = strclass_dept.replace("_", " ")
            else:
                strclass_dept = strclass_dept.strip()

            print(f"Present mark.... Name = {strName}, Id = {strEmpID}, Category = {strclass_dept}")
            # save info in db
            obj = MyMongoDB()
            myEmpInfo_Dic = dict()
            myEmpInfo_Dic['empid'] = strEmpID
            myEmpInfo_Dic['name'] = strName
            myEmpInfo_Dic['department'] = strclass_dept
            strCompleteDate = datetime.now().strftime("%A %d %B %Y")
            strTime = datetime.now().strftime("%I:%M:%S%p")
            strMonth = datetime.now().strftime("%B")
            strYear = datetime.now().strftime("%Y")
            strCurrentDate = datetime.now().strftime("%d")
            strCurrentWeekDayName = datetime.now().strftime("%A")
            myEmpInfo_Dic['month'] = strMonth
            myEmpInfo_Dic['year'] = strYear
            myEmpInfo_Dic['month_date'] = strCurrentDate
            myEmpInfo_Dic['weekday_name'] = strCurrentWeekDayName
            myEmpInfo_Dic['complete_date'] = strCompleteDate
            myEmpInfo_Dic['time'] = strTime
            myEmpInfo_Dic['emp_status'] = "IN"
            myEmpInfo_Dic['camera_id'] = "1"
            obj.MarkedAttendanceInDB(myEmpInfo_Dic, emp_photo)

            # thread = threading.Thread(target= cf.textToSound( strName, strclass_dept) )
            # thread.start() # "This may print while the thread is running."
            # thread.join() # "This will always print after the thread has finished."         
            #### ------cf.textToSound( strName, strEmpID) ###( strName, strclass_dept)
            frequency = 2500  # Set Frequency To 2500 Hertz
            duration = 500  # Set Duration To 1000 ms == 1 second
            winsound.Beep(frequency, duration)


        #for p_keyPname, p_valueAttendence in dict_presentMarked.items():
        #    print( f" Name: {p_keyPname} = {p_valueAttendence}" )
 
    # def Test_thread_fun(self ):
    #     # self.StartMyTimer(0.1)
    #     thread = threading.Thread(target= StartMyTimer(0.1) )
    #     thread.start()
    #     thread.join()

    def putIterationsPerSec(self, frame, iterations_per_sec):
        ##Add iterations per second text to lower-left corner of a frame."""
        cv2.putText(frame, "{:.0f} iterations/sec".format(iterations_per_sec), (10, 450), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255))
        return frame 
    def stop(self):
        print("T: Stop method called...")
        self.stop_threads = True
        self._stop_event.set()
    def stopped(self): 
        return self._stop_event.is_set()
    
    #------for live face New Add Start----------------------------------------------------------------------
    def midpoint(self, p1, p2):
        return int( (p1.x + p2.x) / 2 ), int( (p1.y + p2.y) /2 )

    def get_blinking_ration(self, eye_points, facial_landmarks):
        # left_point   = (facial_landmarks.part(36).x, facial_landmarks.part(36).y)
        # right_point  = (facial_landmarks.part(39).x, facial_landmarks.part(39).y)
        # center_top   =  midpoint( facial_landmarks.part(37), facial_landmarks.part(38) )
        # center_bottom = midpoint( facial_landmarks.part(41), facial_landmarks.part(40) )

        left_point   = (facial_landmarks.part(eye_points[0]).x, facial_landmarks.part(eye_points[0]).y)
        right_point  = (facial_landmarks.part(eye_points[3]).x, facial_landmarks.part(eye_points[3]).y)
        center_top   =  self.midpoint( facial_landmarks.part(eye_points[1]), facial_landmarks.part(eye_points[2]) )
        center_bottom = self.midpoint( facial_landmarks.part(eye_points[5]), facial_landmarks.part(eye_points[4]) )

        # To draw line inside eyes
        # left eye ==>  "---|---"   and 
        # right eye ==>  "---|---"   
        # hor_line = cv2.line(frame, left_point, right_point, (0, 255, 0), 2 )
        # ver_line = cv2.line(frame, center_top, center_bottom, (0, 255, 0), 2 )

        hor_line_lenght = hypot((left_point[0] - right_point[0]), (left_point[1] - right_point[1]) )
        ver_line_lenght = hypot((center_top[0] - center_bottom[0]), (center_top[1] - center_bottom[1]) )
        ratio = hor_line_lenght / ver_line_lenght 
        return ratio
            
    def isBlinking(self, history, maxFrames):
        """ @history: A string containing the history of eyes status 
            where a '1' means that the eyes were closed and '0' open.
            @maxFrames: The maximal number of successive frames where an eye is closed """
        for i in range(maxFrames):
            pattern = '1' + '0'*(i+1) + '1'
            if pattern in history:
                return True
        return False

    def Detection_live_Face_EyeBlinkCount(self, gray, face, myframe, empName):
        shape = self.predictor(gray, face)
        shape = face_utils.shape_to_np(shape)#converting to NumPy Array
        leftEye = shape[self.lStart:self.lEnd]
        rightEye = shape[self.rStart:self.rEnd]
        leftEAR = self.eye_aspect_ratio(leftEye)
        rightEAR = self.eye_aspect_ratio(rightEye)
        ear = (leftEAR + rightEAR) / 2.0

        ###print("for live face ")
        ##faces = self.detector(gray)
        landmarks = self.predictor(gray, face)
        left_eye_ratio = self.get_blinking_ration([36,37,38,39,40,41], landmarks )
        right_eye_ratio = self.get_blinking_ration([42,43,44,45,46,47], landmarks )
        blinking_ratio = (left_eye_ratio + right_eye_ratio) / 2
        ##print(f"eye blinking ratio = {blinking_ratio}")
        # if blinking_ratio > 4.0 :  # 5.7 :
        if ear < 0.25:
            # cv2.putText(myframe, "Eye Blinking", (50, 150), font, 3, (255,0,0), 1) 
            # 1. first time eye close
            val = self.eyes_detected.get(empName)
            self.eyes_detected[empName] = str(val) + '0'            
            # return True
        else:
            # return False
            # 2. second time eye open
            val = self.eyes_detected.get(empName)
            self.eyes_detected[empName] = str(val) + '1'

        if self.isBlinking(self.eyes_detected[empName],3):
            return True
        else:
            return False
    
    ## second option for live face recognition....
    def eye_aspect_ratio(self, eye):
        A = distance.euclidean(eye[1], eye[5])
        B = distance.euclidean(eye[2], eye[4])
        C = distance.euclidean(eye[0], eye[3])
        ear = (A + B) / (2.0 * C)
        return ear

    def Detection_live_Face_Eye_Close(self, gray, subject, myframe, empName):
        shape = self.predictor(gray, subject)
        shape = face_utils.shape_to_np(shape)#converting to NumPy Array
        leftEye = shape[self.lStart:self.lEnd]
        rightEye = shape[self.rStart:self.rEnd]
        leftEAR = self.eye_aspect_ratio(leftEye)
        rightEAR = self.eye_aspect_ratio(rightEye)
        ear = (leftEAR + rightEAR) / 2.0
        leftEyeHull = cv2.convexHull(leftEye)
        rightEyeHull = cv2.convexHull(rightEye)
        ###---cv2.drawContours(myframe, [leftEyeHull], -1, (0, 255, 0), 1)
        ###---cv2.drawContours(myframe, [rightEyeHull], -1, (0, 255, 0), 1)
        
        flag=0
        thresh = 0.25
        frame_check = 1
        if ear < thresh:
            flag += 1
            # print (flag)
            if flag >= frame_check:
                 return True
            else:
                return False
        else:
            return False
    #------end New Add Start----------------------------------------------------------------------



    def run(self):
        print("Connecting to camera...")
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        strPath = cf.GetFilePath_Haarcascade_frontalface()
        faceCascade  = cv2.CascadeClassifier( strPath )
        font = cv2.FONT_HERSHEY_SIMPLEX

        # for live face--------------
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor( cf.GetFilePath_face_landmarks() )
        ####------------------------------



        self.cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)

        # Ajay - Test to reduce CPU uses
        self.cam.set(cv2.CAP_PROP_BUFFERSIZE, 2)


        '''
        # Real Time Streaming Protocol (rtsp://) ==> Live Stream from this URl
        myUrl = "rtsp://freja.hiof.no:1935/rtplive/_definst_/hessdalen02.stream"
        # myUrl = "rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mov"
        self.cam = cv2.VideoCapture(myUrl)
        self.cam.open(myUrl)
        '''
        
        if not self.cam.isOpened():
            print( self.strObj.strInputCam ) # print('Cannot open Input Camera')
            msg.showinfo("Camera not found", "Please connect the camera.")
            self.cam.release() 
            #exit()
            return
        self.cam.set(3, 640) # set video widht
        self.cam.set(4, 480) # set video height
        self.cam.set(10, 100) # screen brightness
        # Define min window size to be recognized as a face
        minW =  0.1*self.cam.get(3)
        minH =  0.1*self.cam.get(4)
        ###-----cps = CountsPerSec().start()

        ######*************
        global myEmpNameForAtt_Mark  
        myEmpNameForAtt_Mark = "Jai-Shri-RAM" 
        # it auto-starts function every 30 second, no need of rt.start()
        objRepeatTimer = RepeatedTimer(15.0, self.myFunToRemoveEmpNameAfterSetTime , myEmpNameForAtt_Mark) 
        ######*************
        try: 
            # for live face---
            (self.lStart, self.lEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["left_eye"]
            (self.rStart, self.rEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["right_eye"]

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
                gray = cv2.cvtColor(self.camImg,cv2.COLOR_BGR2GRAY)

                
                # Resize frame of video to 1/4 size for faster face recognition processing
                small_frame = cv2.resize(self.camImg, (0, 0), fx=0.25, fy=0.25)
                # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
                rgb_small_frame = small_frame[:, :, ::-1]
                # to show blackAndWhiteFrame
                #(thresh, frame) = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)        
                
                ## comment for live face detect
                # faces = faceCascade.detectMultiScale( 
                #     gray,
                #     scaleFactor = 1.1,
                #     minNeighbors = 5,
                #     minSize = (int(minW), int(minH)),
                # )
                
                faces = self.detector(gray)

                print(f"AJAY==========> {rgb_small_frame}")

                # this is used to detect the face which 
                # is closest to the web-cam on the first position 
                ##faces = sorted(faces, key = lambda x: x[2]*x[3], reverse = True) 
                # only the first detected face is used 
                ##faces = faces[:1]   
                strUnknown = self.strObj.strUnknown # "Unknown"
                strPath2 = cf.GetFilePath_Trained_Knn_Model()
                response, bValue = self.compare_predict_result( rgb_small_frame, model_path= strPath2 )
                if( bValue == False):
                    self.cam.release()
                    break
                
                self.live_face_green_color = False

                if len(faces)>0 and len(response)>0:
                    ###-----------New--Rectangle for all faces---------------
                    myColor =  (0, 0, 255) # Red color
                    name = strUnknown
                    #nFaceCount = 1
                    xstart = 0
                    ystart = 0

                    
                    #for values in enumerate(faces), response:
                    #for i, face_rect  in enumerate(faces) :
                    ##----for (face_rect, face_name) in zip( enumerate(faces), response): 
                    for (face_rect, face_name) in zip( faces, response):  


                    #for face_rect, face_name in itertools.product( faces, response ):
                        #for myname, (top, right, bottom, left) in response:                    
                        #itr  = iter(response) 
                        #nextValue_response = next(itr)
                                                
                        ##---x, y, w, h = face_rect[1]  

                        ## for live face
                        x, y = face_rect.left(), face_rect.top()
                        w, h = face_rect.right(), face_rect.bottom()

                                              
                        #face_name = nextValue_response[0]
                        ##print(f"name = {face_name[0]} - rect = {x}, {y}, {w}, {h}")                        
                        name = face_name[0]
                        noOfFaces = len(faces)
                        if name is None:
                            name = strUnknown
                        if name.lower() == strUnknown.lower():
                            myColor =  (0, 0, 255) # Red color - Unknown Person
                        else:
                            if noOfFaces == 1:
                                myColor = (255, 0, 0)  # Blue color  - (0, 255, 0)  # Green color - Attendance mark
                            else:       
                                # Mark Blue Color Rectangle
                                myColor = (255, 0, 0)  # Blue color  - Staff But Attendance not mark
                        # drawing a rectangle on the detected face 

                        #1. Face - Rectangle-----------------
                        ##--cv2.rectangle(self.camImg, (x, y), (x + w, y + h), myColor, 2)
                        #-------cv2.rectangle(self.camImg, (x, y), ( w, h), myColor, 2)

                        # adding detected/predicted name for the face             
                        strTmp = name.split('-')
                        strEmpID = strTmp[0]

                        #2. ID - Rectangle--------------
                        #-------if len(faces) == 1:                
                        #-------    cv2.putText(self.camImg, strEmpID, (x+5,y-7), font, 0.9, myColor, 1)
                        ##print(f"Class & Name = {name}")
                        if name.lower() != strUnknown.lower():
                            strName = strTmp[1]
                            if len(faces) == 1:
                            
                                ## folder name =>used in page_addrecord.py, mongo_db.py, takeempphotopage.py, page_facerecognition.py
                                if( strName.find("_") > 0 ):
                                    strName = strName.replace("_", " ")
                                else:   
                                    strName = strName.strip()

                                #----Live Face ---Add new by Ajay--------------------------------------------------------
                                # default value eye close '0' - value = d.get(key)
                                #val = self.eyes_detected.get(strName) 
                                #self.eyes_detected[strName] = str(val) + '0'

                                # # here we check face is live or its photo
                                #3. Name - Rectangle--------------
                                #-------cv2.putText(self.camImg, strName,  (x+5,h-5), font, 0.9, myColor, 1)
                                live_face =  self.Detection_live_Face_EyeBlinkCount( gray, face_rect, self.camImg, strName )
                                ##---live_face =  self.Detection_live_Face_Eye_Close( gray, face_rect, self.camImg, strName)
                                if(live_face ):                                     
                                #------------------------------------------------------------
                                    self.live_face_green_color = True
                                    self.eyes_detected[strName] = 'None'
                                    ##save_gray_img = cv2.cvtColor(self.camImg,cv2.COLOR_BGR2GRAY)

                                    # Attendance Mark work
                                    ##--Mark_Attendance(name)
                                    myEmpNameForAtt_Mark = name    
                                    thread = threading.Thread(target= self.Mark_Attendance( name,  gray ) )
                                    thread.start() # "This may print while the thread is running."
                                    thread.join() # "This will always print after the thread has finished."
                                
                                if (self.live_face_green_color ):
                                   ##--cv2.putText(self.camImg, strName,  (x+5,y+h-5), font, 0.9, myColor, 1)
                                    myColor = (0, 255, 0)  # Green color
                                    #1.Face
                                    cv2.rectangle(self.camImg, (x, y), ( w, h), myColor, 2)
                                    #2.ID
                                    cv2.putText(self.camImg, strEmpID, (x+5,y-7), font, 0.9, myColor, 1)
                                    #3.Name
                                    cv2.putText(self.camImg, strName,  (x+5,h-5), font, 0.9, myColor, 1) 
                                else:
                                    # Face is not live....
                                    myColor = (255, 0, 0)  # Blue color
                                    #1.Face
                                    cv2.rectangle(self.camImg, (x, y), ( w, h), myColor, 2)
                                    #2.ID
                                    cv2.putText(self.camImg, strEmpID, (x+5,y-7), font, 0.9, myColor, 1)
                                    #3.Name
                                    cv2.putText(self.camImg, strName,  (x+5,h-5), font, 0.9, myColor, 1)

                            else:                        
                                xstart = 15
                                ystart = 25
                                # strTxtShow = str(nFaceCount) + ". " + strName + " - Present"
                                strTxtMsg = self.strObj.strCamHelpToKnow # "In a group, the camera will help you to identify an 'unknown' person"
                                cv2.putText(self.camImg, strTxtMsg,  (xstart, ystart), cv2.FONT_HERSHEY_PLAIN , 0.9, (217, 14, 245), 1)
                                ystart += 15
                                strMsg0 = self.strObj.strMarkIndi # "and attendance will be marked individually"
                                cv2.putText(self.camImg, strMsg0,  (xstart, ystart), cv2.FONT_HERSHEY_PLAIN , 0.9, (217, 14, 245), 1)
                                ystart += 15
                                strMsg1 = self.strObj.strRedUnknown # "1. Red Color - Unknown Person" 
                                cv2.putText(self.camImg, strMsg1,  (xstart, ystart), cv2.FONT_HERSHEY_PLAIN , 0.9, (0, 0, 255), 1)
                                ystart += 15
                                strMsg2 = self.strObj.strBlueStaff #"2. Blue Color - Staff member but attendance Not mark" 
                                cv2.putText(self.camImg, strMsg2,  (xstart, ystart), cv2.FONT_HERSHEY_PLAIN , 0.9, (255, 0, 0), 1) 
                                #nFaceCount += 1
                                ##print(f"Name = {strName}, Class = {strclass}")
                        else:
                            # myColor =  (0, 0, 255) # Red color - Unknown Person
                            #1.Face
                            cv2.rectangle(self.camImg, (x, y), ( w, h), myColor, 2)
                            #2.ID = Unknown
                            cv2.putText(self.camImg, strEmpID, (x+5,y-7), font, 0.9, myColor, 1)
                             
                ###-------------------------------------------------------------------
                # draw the text and timestamp on the frame
                cv2.putText( self.camImg, datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"), (10, self.camImg.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (193,255,193), 1)
                ####---End----

                key = cv2.waitKey(1)  & 0xff  # to Avoid cpu max use
                # if key == ord('q'):
                #     break
                ##--time.sleep(2)

                ###-----self.camImg = self.putIterationsPerSec(self.camImg, cps.countsPerSec())
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
                ###-----cps.increment()
        finally: 
            print('ended')   
            objRepeatTimer.stop()        
############---------------------------------------------------------------------------------

 


class MyFaceRecognitionPage(tk.Frame):
    def __del__(self):
        print("Bye MyFaceRecognitionPage-6")
         

    def __init__(self, tkFrame, Parent=None):
        print("Hi MyFaceRecognitionPage-6")

        #self._frame = None
        tk.Frame.__init__(self, tkFrame, Parent)


        self.myParent = Parent
        self.myParent.bPlsStopCameraBeforeMoveNextPage = True
        
        
        self.myroot = tkFrame
        # create and start thread running the main loop
        ####self.camera_thread = threading.Thread(target=self.mainThreadMyCamera, args=())
        self.camera_thread = mainThreadMyCamera(self)
        self.camera_thread.setName("mycamera_thread")
        self.camera_thread.start()
       
        # bind on close callback that executes on close of the main window
        #self.myroot.protocol("WM_DELETE_WINDOW", self.on_close)
        ###------------------------------------------------

        #self._frame = tkFrame

        # define font - weight − "bold" for boldface, "normal" for regular weight
        #self.myFont = font.Font(family='Helvetica', size=13, weight='normal')

        self.frame = tk.Frame(tkFrame, width=385, height=460, borderwidth=1, bg= myAppBGColor , relief=SUNKEN   )
        #self.frame.pack(side = LEFT, anchor = "nw", fill=Y, expand=YES)
        self.frame.place(x=200-4, y=1, anchor="nw", width=758+6, height=621-1)

        self.panel = None

      
        self.myroot.grid_columnconfigure((0,1), weight=1)

        xLblVal = 80
        yVal = 32
        ctrlHeight = 2
        ctrlWidth = 60 # width of top heading....

        # Heading...
        self.heading = Label(self.frame, text= strObj.strFR_Heading  , fg=myTxtColor, bg=myAppBGColor, font=(myFont, myHeadingTxtFontSize), compound="left" , justify=LEFT, anchor=W)
        self.heading.configure(height=ctrlHeight, width=ctrlWidth)
        self.heading.place(x=xLblVal,y=10)

        # Stop Button
        # rounded_btn_dark.png  
        imgPath = cf.GetAppImageDirPath()       
        btnImg_N0 = imgPath + "rounded_btn.png"
        self.img_N0=PhotoImage(file=btnImg_N0 ) 
        ctrlHeight_New = 36
        ctrlWidth_New = 180

        xbtnVal = 545
        yBtnVal = 564
        self.btnStop = Button(self.frame, image=self.img_N0, text=strObj.strFR_btnStop, command=self.onBtnClickStop , justify = RIGHT, fg=myBtnTxtColor, font=(myFont, myTxtFontSize) , bg=myBtnBGColor , border=0,   highlightthickness = 0, borderwidth = 0)
        #-self.btnStop.configure(height=ctrlHeight, width=20 , compound=CENTER)
        self.btnStop.configure(height=ctrlHeight_New, width=ctrlWidth_New , compound=CENTER)
        self.btnStop.place(x=xbtnVal, y=yBtnVal) 


    def onBtnClickStop(self):
        self.oncloseMyCameraThread()
        self.myParent.bPlsStopCameraBeforeMoveNextPage = False
        #msg.showinfo("Camera", f"Image Capturing process is stopped!!!")
        msg.showinfo( strObj.strMsgTxt_Title,  strObj.strFR_MsgProcessStop)
         

    #def onStartMyCameraThread(self):
    #    # msg.showinfo("Title 666666 ", "Face Recognition System click")
    #    MyFaceRecognitionPage(self.myroot)


    def oncloseMyCameraThread(self):
        print("from Main UI stop camera thread")        
        self.camera_thread.stop()
        print(f"Get Camera thread name = {self.camera_thread.getName()}")
        ####self.camera_thread.stop_threads = True
        #--time.sleep(3.0)
        t.sleep(3.0)

        #self.main_thread.join() 
        if self.camera_thread.isAlive():
            print("Alive() My Camera thread.....  :( ")
        else:
            print("Kill My Camera thread..... Gr8  :) ")
        self.camera_thread.__del__()



 
def myFaceRecognitionMain(root):
    
    MyFaceRecognitionPage(root)
    

if __name__ == "__main__" :
    root = Tk()
    root.geometry("960x640")
    root.title( "strApptitle" )     
    root.resizable(False, False)
    root.configure(background="black" )

    myFaceRecognitionMain(root)

    root.mainloop()


