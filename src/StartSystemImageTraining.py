
"""
This is an example of using the k-nearest-neighbors (KNN) algorithm for face recognition.
When should I use this example?
This example is useful when you wish to recognize a large set of known people,
and make a prediction for an unknown person in a feasible computation time.
Algorithm Description:
The knn classifier is first trained on a set of labeled (known) faces and can then predict the person
in an unknown image by finding the k most similar faces (images with closet face-features under eucledian distance)
in its training set, and performing a majority vote (possibly weighted) on their label.
For example, if k=3, and the three closest face images to the given image in the training set are one image of Biden
and two images of Obama, The result would be 'Obama'.
* This implementation uses a weighted vote, such that the votes of closer-neighbors are weighted more heavily.
Usage:
1. Prepare a set of images of the known people you want to recognize. Organize the images in a single directory
   with a sub-directory for each known person.
2. Then, call the 'train' function with the appropriate parameters. Make sure to pass in the 'model_save_path' if you
   want to save the model to disk so you can re-use the model without having to re-train it.
3. Call 'predict' and pass in your trained model to recognize the people in an unknown image.

"""


import math
from sklearn import neighbors
import os
import os.path
import pickle
from PIL import Image, ImageDraw
import face_recognition
from face_recognition.face_recognition_cli import image_files_in_folder
import cv2
import numpy as np
import common_fun as cf
from os.path import dirname
from os.path import abspath
from sklearn import metrics
import threading



ListCtrlObject = None

 
def train(train_dir, model_save_path=None, n_neighbors=None, knn_algo='ball_tree', verbose=False):
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

    # Loop through each person in the training set
    for class_dir in os.listdir(train_dir):
        if not os.path.isdir(os.path.join(train_dir, class_dir)):
            continue

        # Loop through each training image for the current person
        for img_path in image_files_in_folder(os.path.join(train_dir, class_dir)):
            # print(f"File under Training = {img_path}")
            strText = f"File under Training = {img_path}"
            print(strText)
            ShowAllOnGoingProcess(strText)
            image = face_recognition.load_image_file(img_path)
            face_bounding_boxes = face_recognition.face_locations(image) # , model="cnn"

            if len(face_bounding_boxes) != 1:
                # If there are no people (or too many people) in a training image, skip the image.
                if verbose:
                    print("Image {} not suitable for training: {}".format(img_path, "Didn't find a face" if len(face_bounding_boxes) < 1 else "Found more than one face"))
                    print("")
                    sTxt = ""
                    if( len(face_bounding_boxes) < 1 ):
                        sTxt = "Didn't find a face"
                    else:
                        sTxt = "Found more than one face"                    
                    strText = f"Image {img_path} not suitable for training: {sTxt}" 
                    print(strText)
                    ShowAllOnGoingProcess(strText)
            else:
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
            strText = f"Chose n_neighbors automatically: {n_neighbors} "
            print(strText)
            ShowAllOnGoingProcess(strText)

    # Create and train the KNN classifier
    knn_clf = neighbors.KNeighborsClassifier(n_neighbors=n_neighbors, algorithm=knn_algo, weights='distance')
    knn_clf.fit(X, y)

    #
    if os.path.exists(model_save_path):
        os.remove(model_save_path)

    # Save the trained KNN classifier
    if model_save_path is not None:
        with open(model_save_path, 'wb') as f:
            pickle.dump(knn_clf, f)

    return knn_clf




def StartImageTraining():

    # STEP 1: Train the KNN classifier and save it to disk
    # Once the model is trained and saved, you can skip this step next time.

    '''
        The number of nearest neighbors is 2 which means the unknown face will be tested based on the weight of its two nearest neighbors. 
        The Euclidean distance is used in this case
    '''

    strText = "Start System Image Training (KNN classifier)..."
    print(strText)
    ShowAllOnGoingProcess(strText)

    strPath1 = cf.GetFilePath_StaffImages()
    strPath2 = cf.GetFilePath_Trained_Knn_Model()
      
    classifier = train(strPath1, model_save_path= strPath2, n_neighbors=2)

    # thread = threading.Thread(target= train(strPath1, model_save_path= strPath2, n_neighbors=2)  )
    # thread.start() # "This may print while the thread is running."
    # thread.join() # "This will always print after the thread has finished." 

   
    strText = "System Image Training Completed!"
    print(strText)
    ShowAllOnGoingProcess(strText)
   
    return classifier



def StartImageTraining_GUI(lstCtrlObj=None):
    if(lstCtrlObj is not None):
        # for x in range(100):
        #     lstCtrlObj.insert('end', x)
        global ListCtrlObject
        ListCtrlObject = lstCtrlObj

        StartImageTraining()


def ShowAllOnGoingProcess(strText):
    #print(strText)
    ListCtrlObject.insert('end', strText)
