import math
from sklearn import neighbors
import os
import os.path
import pickle
from PIL import Image, ImageDraw
import face_recognition
from face_recognition.face_recognition_cli import image_files_in_folder
import threading
import common_fun as cf 
import cv2
import numpy as np

from os.path import dirname
from os.path import abspath
from sklearn import metrics
import StartSystemImageTraining as st
import itertools

import datetime
import imutils
import time


winTitle = "Ajay - Alert System"

# USAGE
# python real_time_object_detection.py --prototxt MobileNetSSD_deploy.prototxt.txt --model MobileNetSSD_deploy.caffemodel
# python .\src\LineAlert.py --prototxt MobileNetSSD_deploy.prototxt.txt --model MobileNetSSD_deploy.caffemodel


# import the necessary packages
from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import argparse
import imutils
import time
import cv2

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--prototxt", required=True, help="path to Caffe 'deploy' prototxt file")
ap.add_argument("-m", "--model", required=True, help="path to Caffe pre-trained model")
ap.add_argument("-c", "--confidence", type=float, default=0.2, help="minimum probability to filter weak detections")
args = vars(ap.parse_args())

# initialize the list of class labels MobileNet SSD was trained to
# detect, then generate a set of bounding box colors for each class
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
	"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
	"dog", "horse", "motorbike", "person", "pottedplant", "sheep",
	"sofa", "train", "tvmonitor"]
COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

# load our serialized model from disk
print("[INFO] loading model...")
net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])

# initialize the video stream, allow the cammera sensor to warmup,
# and initialize the FPS counter
print("[INFO] starting video stream...")
def StartObjectDetectLineAlert():
    vs = VideoStream(src=0).start()
    time.sleep(2.0)
    fps = FPS().start()

    # loop over the frames from the video stream
    while True:
        # grab the frame from the threaded video stream and resize it
        # to have a maximum width of 400 pixels
        frame = vs.read()
        frame = imutils.resize(frame, width=400)

        # grab the frame dimensions and convert it to a blob
        (h, w) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)),
            0.007843, (300, 300), 127.5)

        # pass the blob through the network and obtain the detections and
        # predictions
        net.setInput(blob)
        detections = net.forward()

        # loop over the detections
        for i in np.arange(0, detections.shape[2]):
            # extract the confidence (i.e., probability) associated with
            # the prediction
            confidence = detections[0, 0, i, 2]

            # filter out weak detections by ensuring the `confidence` is
            # greater than the minimum confidence
            if confidence > args["confidence"]:
                # extract the index of the class label from the
                # `detections`, then compute the (x, y)-coordinates of
                # the bounding box for the object
                idx = int(detections[0, 0, i, 1])
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")

                # draw the prediction on the frame
                label = "{}: {:.2f}%".format(CLASSES[idx],
                    confidence * 100)
                cv2.rectangle(frame, (startX, startY), (endX, endY),
                    COLORS[idx], 2)
                y = startY - 15 if startY - 15 > 15 else startY + 15
                cv2.putText(frame, label, (startX, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)

        # show the output frame
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break

        # update the FPS counter
        fps.update()

    # stop the timer and display FPS information
    fps.stop()
    print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
    print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

    # do a bit of cleanup
    cv2.destroyAllWindows()
    vs.stop()



##--------START--------------------------------------------------------
boxes = [ [0, 0], [0, 0]]
line_start_point = (0, 0)
line_end_point = (0, 0) 
def on_mouse(event, x, y, flags, params):

    global line_start_point
    global line_end_point

    if event == cv2.EVENT_LBUTTONDOWN:
        print( f'Start Mouse Position: {str(x)},  {str(y)} ' )
        sbox = [x, y]        
        boxes.append(sbox)
        line_start_point = (x, y)
    elif event == cv2.EVENT_LBUTTONUP:
        print( f'End Mouse Position: {str(x)}, {str(y)}')
        ebox = [x, y]        
        boxes.append(ebox)
        line_end_point = (x, y)

def AlertWhenLineCross(winTitle, img):
        cv2.setMouseCallback(winTitle, on_mouse, 0)
        color = (255, 0, 0)
        thickness=3
        img = cv2.line(img, line_start_point, line_end_point, color, thickness )
        lineX, lineY = line_start_point 
        ftop = 0
        fright = 0
        fbottom = 0
        fleft = 0
        faceXY = face_recognition.face_locations(img) # (top, right, bottom, left)
        if len(faceXY) > 0:
            for ftop, fright, fbottom, fleft in faceXY:
                # print(f" ftop = {ftop}, fright= {fright}, fbottom= {fbottom}, fleft= {fleft} ")
                #if  lineX >= fleft or lineY >= ftop:
                if  ( lineX < fleft or lineX > fleft ) and ( lineY < ftop or lineY > ftop ):
                    print("Alert line touch!!!!")
                    cf.MakeSound("Alert Some one cross the line")
##--------END--------------------------------------------------------

 
'''
def StartFaceRecognition( ):
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    strPath = cf.GetFilePath_Haarcascade_frontalface()
    faceCascade  = cv2.CascadeClassifier( strPath )
    font = cv2.FONT_HERSHEY_SIMPLEX

    # Initialize and start realtime video capture
    cam = cv2.VideoCapture(0)
    ##cam = cv2.VideoCapture(ipcam_streaming_url)


    if not cam.isOpened():
        print('Cannot open camera for input')
        cam.release() 
        exit()

    cam.set(3, 640) # set video widht
    cam.set(4, 480) # set video height
    cam.set(10, 100) # screen brightness

    # Define min window size to be recognized as a face
    minW =  0.1*cam.get(3)
    minH =  0.1*cam.get(4)
    
    while True:
        ret, frame =cam.read()
        if not ret:
            print('Cannot receive frame from input camera')
            cam.release()
            break

        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # to show blackAndWhiteFrame
        #(thresh, frame) = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)        
        faces = faceCascade.detectMultiScale( 
            gray,
            scaleFactor = 1.1,
            minNeighbors = 5,
            minSize = (int(minW), int(minH)),
        )

        # this is used to detect the face which 
        # is closest to the web-cam on the first position 
        ##faces = sorted(faces, key = lambda x: x[2]*x[3], reverse = True) 
        # only the first detected face is used 
        ##faces = faces[:1]   
                 
        ###-------------------------------------------------------------------
        ### add new
        AlertWhenLineCross(winTitle, frame)
        ###-------------------------------------------------------------------
        # draw the text and timestamp on the frame
        cv2.putText( frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (193,255,193), 1)
            
        cv2.imshow(winTitle, frame) 
        key = cv2.waitKey(1)     
        if key & 0xFF == ord("q") : 
            break    
    cam.release() 
    cv2.destroyAllWindows() 
'''

if __name__ == "__main__":
        
    ## 1. STEP 1:call AutoCaptureFaceForTraining
    

    ## 2. STEP 2: Train the KNN classifier and save it to disk
    #####st.StartImageTraining()
    
    ## 3.  STEP 3: Using the trained classifier, make predictions for unknown images  
    ###---StartFaceRecognition()

    StartObjectDetectLineAlert()

 

        
 