#from tkinter import Tk, Label, Button
from tkinter import *
from tkinter import ttk
from AllStrings import myStrings
import common_fun as cf 
import tkinter.messagebox as msg
import time
import tkinter.font as font
import tkinter as tk
import cv2
import os
import numpy as np
import math
from PIL import Image, ImageDraw 
import threading
from PIL import Image
from PIL import ImageTk
import datetime
from os.path import exists
import shutil
from sklearn import neighbors  ##  
import sklearn.neighbors.typedefs 
import face_recognition 
from face_recognition.face_recognition_cli import image_files_in_folder
import common_fun as cf
from os.path import dirname
from os.path import abspath
from sklearn import metrics
import pickle
from Mongo_DB import MyMongoDB
##
import PIL.Image
import PIL.ImageDraw
import requests
from io import BytesIO
from IPython.display import display
 

myAppBGColor = "lavender blush" # "grey" 
myFont = "Helvetica"
myHeadingTxtFontSize = 15
myTxtFontSize = 10
myTxtColor = "black" #  "white"
myBtnBGColor="lavender blush" # "white smoke" # "Green"
myBorderColor = "medium violet red"
myBtnTxtColor = "white"
myProgressBrBG = "purple"

strObj  = myStrings()
imgPath = cf.GetAppImageDirPath() 

class MyTrainedSystemPage(tk.Frame):
    def __del__(self):
        print("Bye MyTrainedSystemPage-4")

    def __init__(self, tkFrame, Parent=None):
        print("Hi MyTrainedSystemPage-4")
        #self._frame = None
        tk.Frame.__init__(self, tkFrame, Parent)

        #self._frame = tkFrame
        self.myParent = Parent
        self.myroot = tkFrame

        self.bIsTrainingDone = False

        # define font - weight − "bold" for boldface, "normal" for regular weight
        #self.myFont = font.Font(family='Helvetica', size=13, weight='normal')

        self.frame = tk.Frame(tkFrame, width=385, height=460, borderwidth=0, bg= myAppBGColor , relief=SUNKEN   )
        #self.frame.pack(side = LEFT, anchor = "nw", fill=Y, expand=YES)
        self.frame.place(x=200-4, y=1, anchor="nw", width=758+6, height=621-1)

        self.panel = None
        self.CreateTrainingPageGUI()

        self.bIsTrainingStop = False
        self.btnStartTraining['state']="normal" 
        self.btnStopTraining['state']="disabled"

        self.CheckAvailablePhotoOfEmpIsInDBTable()


    def CreateTrainingPageGUI(self):
        self.myroot.grid_columnconfigure((0,1), weight=1)

        xLblVal = 80
        yVal = 32
        ctrlHeight = 3
        ctrlWidth = 80

        # Heading...
        self.heading = Label(self.frame, text=strObj.strTrainingPageH , fg=myTxtColor, bg=myAppBGColor, font=(myFont, myHeadingTxtFontSize), compound="left" , justify=LEFT, anchor=W  )
        self.heading.configure(height=ctrlHeight, width=ctrlWidth)
        self.heading.place(x=xLblVal,y=32)  #.pack(expand=YES, fill=BOTH)     

        s = ttk.Style()
        s.theme_use('clam')
        s.configure("colour.Horizontal.TProgressbar", foreground='red', background= myProgressBrBG )

        ctrlHeight = 1 
        ctrlWidth = 20
        yVal += 85 + 30
        # add avi file for showing progress....
        self.my_progress = ttk.Progressbar(self.frame , style="colour.Horizontal.TProgressbar", orient=HORIZONTAL, length=580, mode='determinate' ) # indeterminate -- for infinite 
        self.my_progress.place(x=xLblVal, y=yVal )
 


        yVal += 85  

        ####------Y--side-scrollbar------------
        self.frm1 = Frame(self.frame)
        self.frm1.configure(height=300, width=620 )
        self.frm1.place(x=xLblVal, y=yVal)          
        self.y_scrollbar = Scrollbar(self.frm1, orient="vertical")
        self.y_scrollbar.pack(side=RIGHT, fill=Y) 
        self.listNodes = Listbox(self.frm1,width=65, height=14, yscrollcommand=self.y_scrollbar.set, font=("Helvetica", 12))
        self.listNodes.pack(side="left", fill="y")
        self.y_scrollbar.config( command=self.listNodes.yview )

        ####------X-side-scrollbar------------
        self.x_scrollbar = Scrollbar(self.frm1, orient=HORIZONTAL)
        self.x_scrollbar.pack(side=TOP, fill=X) 
        #self.listNodes = Listbox(self.frm1,width=65, height=14, xscrollcommand=self.x_scrollbar.set, font=("Helvetica", 12))
        self.listNodes.config(xscrollcommand=self.x_scrollbar.set)
        self.listNodes.pack(side=TOP, fill=X)
        self.x_scrollbar.config( command=self.listNodes.xview )
        ####-------------------
         

        btnImg_N1 = imgPath + "rounded_btn_dark.png"
        self.img_N1=PhotoImage(file=btnImg_N1 ) 
        ctrlHeight = 36
        ctrlWidth = 180
        xbtnVal = 245 + 70
        yBtnVal  = 575
        self.btnStopTraining = Button(self.frame, image=self.img_N1, text=strObj.strBtnStopTrain, command=self.onBtnClickStopTraining , justify = RIGHT, fg=myBtnTxtColor, font=(myFont, myTxtFontSize) , bg=myBtnBGColor, border=0,   highlightthickness = 0, borderwidth = 0)
        self.btnStopTraining.configure(height=ctrlHeight, width=ctrlWidth, compound=CENTER)
        self.btnStopTraining.place(x=xbtnVal, y=yBtnVal) 

        # at end Show Thank you info.
        btnImg_N2 = imgPath + "rounded_btn.png"
        self.img_N2=PhotoImage(file=btnImg_N2 ) 
        ctrlHeight = 36
        ctrlWidth = 180

        xbtnVal = 545 
        yBtnVal  = 575
        self.btnStartTraining = Button(self.frame, image=self.img_N2, text=strObj.strBtnStartTrain, command=self.onBtnClickStartTraining, justify = RIGHT, fg=myBtnTxtColor, font=(myFont, myTxtFontSize) , bg=myBtnBGColor, border=0,   highlightthickness = 0, borderwidth = 0)
        self.btnStartTraining.configure(height=ctrlHeight, width=ctrlWidth, compound=CENTER)
        self.btnStartTraining.place(x=xbtnVal, y=yBtnVal) 

    def onBtnClickStopTraining(self):
        self.my_progress.stop()
        self.bIsTrainingStop = True
        self.btnStartTraining['state']="normal" 
        self.btnStopTraining['state']="disabled"
        if( self.ReStartSystemTraining  == False ):
            if(self.bIsTrainingDone):
                msg.showinfo( strObj.strMsgTitel, strObj.strMsgTxt_TrainComplet)

    def onBtnClickStartTraining(self):
        #print("onBtnClickStartTraining")
        #self.my_progress['value'] += 20
        self.btnStartTraining['state']="disabled"
        self.btnStopTraining['state']="normal"
        self.bIsTrainingStop = False

        self.bIsTrainingDone = False
        self.listNodes.delete(0,'end') # to clean the list box

        self.my_progress.start(25)
        self.StartImageTraining()

    ##############################################----------Training Start---------------------###############################################
    def train(self, train_dir, model_save_path=None, n_neighbors=None, knn_algo='ball_tree', verbose=False):
        """
        Trains a k-nearest neighbors classifier for face recognition.
        :param train_dir: directory that contains a sub-directory for each known person, with its name.
        (View in source code to see train_dir example tree structure)
        Structure:
            <train_dir>/
            ├── <person1>/
            │   ├── <somename1>.jpeg
            │   ├── <somename2>.jpeg
            │   ├── ...
            ├── <person2>/
            │   ├── <somename1>.jpeg
            │   └── <somename2>.jpeg
            └── ...
        :param model_save_path: (optional) path to save model on disk
        :param n_neighbors: (optional) number of neighbors to weigh in classification. Chosen automatically if not specified
        :param knn_algo: (optional) underlying data structure to support knn.default is ball_tree
        :param verbose: verbosity of training
        :return: returns knn classifier that was trained on the given data.
        """
        X = []
        y = []

        sFolderName = os.listdir(train_dir) 
        number_files = len(sFolderName)
        if(number_files == 0):
            msg.showerror(strObj.strMsgTitel, strObj.strMsgTxt_No_Img )
            self.bIsTrainingStop = True
            
            # In case of "Image not found" delete 
            # delete already created "trained_knn_model.clf" file
            #strPath2 = cf.GetFilePath_Trained_Knn_Model()
            # if os.path.exists(model_save_path):
            #     os.remove(model_save_path)
            return

        self.ReStartSystemTraining = False
        bIsAllImagesAreTrained = True

        # Loop through each person in the training set
        for class_dir in os.listdir(train_dir):
            if not os.path.isdir(os.path.join(train_dir, class_dir)):
                continue

            if(self.bIsTrainingStop):
                strText = strObj.strMsgTxt_trainStop # "Training is Stopped!!!"
                self.ShowAllOnGoingProcess(strText, 'black')
                return

            # Loop through each training image for the current person
            for img_path in image_files_in_folder(os.path.join(train_dir, class_dir)):

                if(self.bIsTrainingStop):
                    strText = strObj.strMsgTxt_trainStop # "Training is Stopped!!!"
                    self.ShowAllOnGoingProcess(strText, 'black')
                    return

                '''
                # print(f"File under Training = {img_path}")
                # strMyTxt = strObj.strMsgTxt_FUT # "File under Training" 
                # strText = f"{strMyTxt} = {img_path}"
                # print(strText)
                # self.ShowAllOnGoingProcess(strText)
                image = face_recognition.load_image_file(img_path)  ## , mode='RGB'

                #  model="cnn" ==>  cnn (convolutional neural network)
                #  model="hog" ==>  hog (histogram of oriented gradients)
                # face_bounding_boxes = face_recognition.face_locations(image, number_of_times_to_upsample=0 , model="hog") # , model="cnn"

                face_bounding_boxes = face_recognition.face_locations(image  )
                '''

                '''
                # load the input image and convert it from BGR (OpenCV ordering)
                # to dlib ordering (RGB)
                image = cv2.imread(img_path)
                rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                #Use Face_recognition to locate faces
                face_bounding_boxes = face_recognition.face_locations(rgb,model='hog')
                '''
                
                image = face_recognition.load_image_file(  img_path  )
                face_bounding_boxes = face_recognition.face_locations(image)
                number_of_faces = len(face_bounding_boxes)



                if len(face_bounding_boxes) != 1:
                    # If there are no people (or too many people) in a training image, skip the image.
                    if verbose:
                        print("Image {} not suitable for training: {}".format(img_path, "Didn't find a face" if len(face_bounding_boxes) < 1 else "Found more than one face"))
                        print("")
                        sTxt = ""
                        if( len(face_bounding_boxes) < 1 ):
                            sTxt = strObj.strMsgTxt_NotFindFace # "Didn't find a face"
                        else:
                            sTxt = strObj.strMsgTxt_MoreFace # "Found more than one face"     
                        #strTxtImg =  strObj.strMsgTxt_Img # Image   
                        strTxtNotSuitable =  strObj.strMsgTxt_NotSuitable  # not suitable for training:           
                        strText = f"{strTxtNotSuitable} = {img_path}  {sTxt}" 
                        print(strText)
                        self.ShowAllOnGoingProcess(strText, 'red')
                        bIsAllImagesAreTrained = False
                        ### delete this image file -------------- 
                        if os.path.exists( img_path ):
                            os.remove( img_path)
                        ###--------------------------------------
                    else:
                        strTxtNotSuitable =  strObj.strMsgTxt_NotSuitable  # not suitable for training:           
                        strText = f"{strTxtNotSuitable} = {img_path}  " 
                        print(strText)
                        self.ShowAllOnGoingProcess(strText, 'red')
                        bIsAllImagesAreTrained = False

                        ### delete this image file -------------- 
                        if os.path.exists( img_path ):
                            os.remove( img_path)
                        ###--------------------------------------

                else:
                    strMyTxt = strObj.strMsgTxt_FUT # "File under Training" 
                    strText = f"{strMyTxt} = {img_path}"
                    print(strText)
                    self.ShowAllOnGoingProcess(strText, 'green')
                    # Add face encoding for current image to the training set
                    X.append(face_recognition.face_encodings(image, known_face_locations=face_bounding_boxes)[0])
                    ##-- y.append(class_dir)
                    filename_w_ext = os.path.basename(img_path )
                    filename, file_extension = os.path.splitext(filename_w_ext)
                    face_category_with_name = class_dir  # + "-" + filename
                    y.append(face_category_with_name)

        # Determine how many neighbors to use for weighting in the KNN classifier
        if n_neighbors is None:
            n_neighbors = int(round(math.sqrt(len(X))))
            if verbose:            
                # print("Chose n_neighbors automatically:", n_neighbors)
                strTxt1 = strObj.strMsgTxt_CNNA # Chose n_neighbors automatically: 
                strText = f"{strTxt1} {n_neighbors} "
                print(strText)
                self.ShowAllOnGoingProcess(strText, 'black')

        # Create and train the KNN classifier
        knn_clf = neighbors.KNeighborsClassifier(n_neighbors=n_neighbors, algorithm=knn_algo, weights='distance')
        if( len(y) == 0 & len(X) == 0 ):
            msg.showerror(strObj.strMsgTitel, strObj.strMsgTxt_AllImagesAreNotSuitable)
            self.bIsTrainingStop = True
            self.btnStopTraining['state'] = 'disable'
            self.btnStartTraining['state'] = 'normal'
            return
        elif( False == bIsAllImagesAreTrained   ):
            msg.showerror(strObj.strMsgTitel, strObj.strMsgTxt_FewImageAreNotTrained )
            self.ReStartSystemTraining = True

        knn_clf.fit(X, y)

        #
        if os.path.exists(model_save_path):
            os.remove(model_save_path)

        # Save the trained KNN classifier
        if model_save_path is not None:
            with open(model_save_path, 'wb') as f:
                pickle.dump(knn_clf, f)

        return knn_clf

    def StartImageTraining(self):
        # STEP 1: Train the KNN classifier and save it to disk
        # Once the model is trained and saved, you can skip this step next time.
        '''
            The number of nearest neighbors is 2 which means the unknown face will be tested based on the weight of its two nearest neighbors. 
            The Euclidean distance is used in this case
        '''
        strText = "Start System Image Training..." ### (KNN classifier)...
        print(strText)
        self.ShowAllOnGoingProcess(strText, 'black')

        strPath1 = cf.GetFilePath_StaffImages()
        strPath2 = cf.GetFilePath_Trained_Knn_Model()
        
        classifier = self.train(strPath1, model_save_path= strPath2, n_neighbors=2)
    
        if(self.bIsTrainingStop):
            strText = strObj.strMsgTxt_TrainNotComplet # "System Image Training Not Completed!"
            txtColor = 'red'
        else:
            self.bIsTrainingDone = True
            if( self.ReStartSystemTraining  == False ):
                strText = strObj.strMsgTxt_TrainComplet  # "System Image Training Completed!"
                txtColor = 'green'
            else:
                strText = strObj.strMsgTxt_ReStart_Train   # "Re-Start System Training as some images are not suitable"
                txtColor = 'red'                
            self.onBtnClickStopTraining()

        self.my_progress.stop()
        print(strText)
        self.ShowAllOnGoingProcess(strText, txtColor)    
        return classifier

    def ShowAllOnGoingProcess(self, strText, txtColorValue):
        #print(strText)
        self.listNodes.insert(END, strText) 

        self.listNodes.see ( END ) ## to see the last added item in list

        # way to pass the colour
        ##self.listNodes.itemconfig(END, bg= 'yellow' )
        self.listNodes.itemconfig(END, foreground= txtColorValue  ) 

        #update_idletasks() 
        self.myroot.update()

    def CheckAvailablePhotoOfEmpIsInDBTable(self):
        # if employ id, name, dest is NOT available in DB table than 
        # DELETE its photo image folder before start training...
        strStaffImagFolderPath = cf.GetStaffImageDirPath()
        # Loop through each person in the training set
        for dir_name in os.listdir( strStaffImagFolderPath ):
            strSplitDirName = dir_name.split('-')
            emp_id = strSplitDirName[0]
            emp_name = strSplitDirName[1]
            emp_desc   = strSplitDirName[2]
            OldfolderName = emp_id  + "-" + emp_name + "-" +  emp_desc 
            # check in DB if not available than delete this folder with all its images...
            objDB = MyMongoDB()
            folder_As_db  = objDB.CheckEmpIDExistInDB(emp_id)             
            if( folder_As_db.lower() != OldfolderName.lower() ):
                path = os.path.join(strStaffImagFolderPath, OldfolderName) 
                if(os.path.exists(path)):
                    # Remove the specified dir
                    shutil.rmtree(path) 

            


    ##############################################----------Training End---------------------#################################################
 
def myTrainedSystemMain(root):
    
    MyTrainedSystemPage(root)
    

if __name__ == "__main__" :
    root = Tk()
    root.geometry("960x640")
    root.title( "strApptitle" )     
    root.resizable(False, False)
    root.configure(background="black" )

    myTrainedSystemMain(root)

    root.mainloop()

