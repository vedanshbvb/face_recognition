import pyttsx3  
import os, shutil
from os.path import dirname
from os.path import abspath
import time

import os.path
from os import path

import sys
 
import cv2  
import numpy as np
from pathlib import Path

from requests.exceptions import HTTPError
# from bs4 import BeautifulSoup
import objcrypt 
import requests
import tkinter.messagebox as msg
import json



from AllStrings import myStrings
strObj  = myStrings()


# URL_TO_VERIFY_KEY = "http://localhost:8000/verifykey/"
URL_TO_VERIFY_KEY = "http://wfh.vervelogic.com:8000/frapp/keyapi/verifykey/"
URL_CHECK_UPDATE =  "http://wfh.vervelogic.com:8000/frapp/keyapi/checkforupdate/"
 


#ROOT_DIR = None
def GetMainFileRootPath():
    #global ROOT_DIR
    ROOT_DIR = os.path.dirname(sys.modules['__main__'].__file__)
    ##print(ROOT_DIR)
    return ROOT_DIR

def GetKeyDirPath():
    strPath = get_file_parent_dir_path() + "\\key_fr\\"
    if not os.path.exists(strPath): ## Ajay
        os.makedirs(strPath)
    return strPath

def GetAppImageDirPath():
    strPath = get_file_parent_dir_path() + "\\src_images\\"
    if not os.path.exists(strPath): ## Ajay
        os.makedirs(strPath)
    return strPath

def GetStaffImageDirPath():
    strPath = get_file_parent_dir_path() + "\\staffImages\\"
    if not os.path.exists(strPath): ## Ajay
        os.makedirs(strPath)
    return strPath

def GetFilePath_StaffImages():
    strPath = get_file_parent_dir_path() + "\\staffImages"
    if not os.path.exists( strPath ):
        os.makedirs(strPath)
    return strPath
    # else:
    #     print(f"File Path not Exists = {strPath}")

def GetExportDirName():
    strPath = get_file_parent_dir_path() + "\\export_excel_db"
    if not os.path.exists( strPath ):
        os.makedirs(strPath)
    return strPath     


def ResizeAllImages(srcImg, dstImg):

    if os.path.isdir(dstImg):
        shutil.rmtree(dstImg) # delete old folder and files... 

    count = 0
    for path, subdirnames, filenames in os.walk(srcImg):
        for filename in filenames:
            if filename.startswith("."):
                print("Skipping this files", filename )
                continue
            img_path = os.path.join(path, filename)     
            print("img_path = ", img_path)
            id = os.path.basename(path)
            img = cv2.imread(img_path)
            if img is None:
                print("Image not loaded properly")
                continue
            resized_image = cv2.resize(img, (100,100))
            new_path = dstImg + "/" + str(id)
            print("resized path is", os.path.join(new_path, "framed%d.jpg" % count  ))
            # if folder not avaliable than create it
            if not os.path.exists(new_path):
                os.makedirs(new_path)
                print(f"Create folder to save image...{new_path}")


            cv2.imwrite(os.path.join(new_path, "frame%d.jpg" % count), resized_image )
            count += 1


# def Convert_colorImg_grayscale_for_datasample():
#     '''
#     Actually, we do not need to use color images as data samples since the 
#     HOG algorithm obtain the face patterns based on the light direction. 
#     Therefore, a grayscale image should be enough. You may want to change your 
#     image to grayscale by using the following source code.
#     '''
#     from PIL import Image
#     import face_recognition
#     import os
#     import numpy
#     count = 1
#     path = "D:\\MyAllProjects\\FaceRecognition\\src\\dataset"
#     for file in os.listdir("dataset"):
#     dirs = os.path.join(path,file)
#     for image_file in os.listdir(dirs):
#         full_file_path = os.path.join(dirs, image_file)
#         image = Image.open(open(full_file_path,'rb'))
#         pil_image = image.convert('L') #convert to gray scale
#         #pil_image = pil_image.rotate(-90)#comment this line if not rotated
#         newPath = os.path.join("result",file) #create result folder to store
#         if not os.path.exists(newPath):
#         os.makedirs(newPath)
#         name = str(count) + ".jpg"
#         img_dir = os.path.join(newPath,name)
#         pil_image.save(img_dir)
#         count = count + 1
#     count = 1

def MakeSound(strMsg):
    engine = pyttsx3.init()    
    engine.say( f" {strMsg} ")      
    engine.runAndWait()


# def SoundInThread(strName, strEmpID=""):
#     engine = pyttsx3.init() 
#     engine.say( f"Hello {strName}")      
#     engine.runAndWait()

def textToSound(strName, strEmpID=""):
    
    # ##'''
    # import threading
    # thread = threading.Thread(target= SoundInThread( strName, strEmpID) )
    # thread.start() # "This may print while the thread is running."
    # thread.join() # "This will always print after the thread has finished." 
    # return
    # ##'''

    # initialisation 
    engine = pyttsx3.init()     

    # engine.say("Hello Ajay") 
    # engine.say("Thank you") 
    # engine.runAndWait()

    ## engine.say( f"Hello {strName} your attendance has been marked, and your ID is {strEmpID}, Thank you")  
    engine.say( f"Hello {strName}")      
    engine.runAndWait()
    #time.sleep(2)

 
'''
def labels_for_training_data(directory):
    faces=[]
    faceID=[]

    for path, subdirnames, filenames in os.walk(directory):
        for filename in filenames:
            if filename.startswith("."):
                print("Skipping system file")
                continue
            id=os.path.basename(path)
            img_path = os.path.join(path, filename)
            print("img_path = ", img_path)
            print("id: ", id)
            test_img=cv2.imread(img_path)
            if test_img is None:
                print("Image not loaded properly")
                continue
            faces_rect, gray_img = faceDetection(test_img)
            if len(faces_rect) != 1:
                continue # since we are assuming only single person image are being fed to classifier
            (x,y,w,h) = faces_rect[0]
            roi_gray=gray_img[y:y+w, x:x+h]
            faces.append(roi_gray)
            faceID.append(int(id))
    return faces, faceID
    '''

def get_file_parent_dir_path():
    """return the path of the parent directory of current file's directory
        d:\\MyAllProjects\\FaceRecognition
     """
    current_dir_path = dirname(abspath(__file__))
    path_sep = os.path.sep
    components = current_dir_path.split(path_sep)
    return path_sep.join(components[:-1])


def GetAllImagesInfo( ):
    # Store all images file path and file name in list
    strPath = get_file_parent_dir_path() + "//staffImages"
    if not os.path.exists(strPath): ## Ajay
        os.makedirs(strPath)
    if os.path.exists( strPath ):
        return strPath
    else:
        print(f"File Path not Exists = {strPath}")
    #image_name = []
    image_path = []
    for path, subdirnames, filenames in os.walk(strPath):
        for filename in filenames:
            if filename.startswith("."):
                print("Skipping system file")
                continue
            img_path = os.path.join(path, filename)    
            #img_name = os.path.basename(filename)
            #img_name = os.path.splitext(img_name)[0]
            ###print("img_path = ", img_path)
            #print("img_name = ", img_name)           
            #image_name.append( img_name )
            image_path.append( img_path )
    return image_path #, image_name



EmployeeFullDetails = []

def Test():
    '''
    Here we read all images of train dir to GET the following info:
    1. Class
    2. Name 
    3. EmpID - use to display Name of employe when employe comes in group snaps
    '''
    empLst = {}
    train_dir = "D:\\MyAllProjects\\FaceRecognition\\staffImages\\"
     # Loop through each person in the training set
    for class_dir in os.listdir(train_dir):
        if not os.path.isdir(os.path.join(train_dir, class_dir)):
            continue
        strData = class_dir.split('-')
        EmpID = strData[2].lower().replace('empid', '')
        empLst["EmpID"] = EmpID
        empLst["EmpClass"] = strData[0]
        empLst["EmpName"] = strData[1]
        empLst["EmpFullID"] = strData[2]
        EmployeeFullDetails.append(empLst.copy()) 
    ##print(EmployeeFullDetails )
    #    
def GetStop_MongoDB_BatchFilePath():
    strPath = get_file_parent_dir_path() + "//supportingfiles" 
    strPath = strPath + "//stopMongoDb.bat"
    if path.exists( strPath ):
        return strPath
    else:
        print(f"File Path not Exists = {strPath}")

def GetStart_MongoDB_BatchFilePath():
    strPath = get_file_parent_dir_path() + "//supportingfiles" 
    strPath = strPath + "//startMongoDb.bat"
    if path.exists( strPath ):
        return strPath
    else:
        print(f"File Path not Exists = {strPath}")


def GetFilePath_Haarcascade_frontalface():
    ##  use to give "haarcascade_frontalface_default.xml" file path to recognize the face
    strPath = get_file_parent_dir_path() + "//supportingfiles" 
    if not os.path.exists(strPath): ## Ajay
        os.makedirs(strPath)
    strPath = strPath + "//haarcascade_frontalface_default.xml"
    if path.exists( strPath ):
        return strPath
    else:
        print(f"File Path not Exists = {strPath}")

def GetFilePath_face_landmarks():
    ##  use to give "shape_predictor_68_face_landmarks.dat" file path to recognize the face
    strPath = get_file_parent_dir_path() + "//MyFRProject//face_recognition_models//models" 
    if not os.path.exists(strPath): ## Ajay
        os.makedirs(strPath)
    strPath = strPath + "//shape_predictor_68_face_landmarks.dat"
    if path.exists( strPath ):
        return strPath
    else:
        print(f"File Path not Exists = {strPath}")


def GetFilePath_Trained_Knn_Model():
    ## use to give "trained_knn_model.clf" file path to recognize the face
    strPath = get_file_parent_dir_path() + "//supportingfiles"
    if not os.path.exists(strPath): ## Ajay
        os.makedirs(strPath)
    strPath = strPath + "//trained_knn_model.clf"
    if path.exists( strPath ):
        return strPath
    else:
        print(f"File Path not Exists = {strPath}")
        ## create empty file
        open(strPath, 'a').close()
        return strPath

def Get_Emp_Tmp_Image_Dir():
    strPath = get_file_parent_dir_path() + "//Emp_Tmp_Image"
    if not os.path.exists(strPath): ## Ajay
        os.makedirs(strPath)
    return strPath


import subprocess
import os
def GetMachineUniqueID():
    machine_unique_id = ''
    cmd = 'wmic csproduct get uuid'
    uuid = str(subprocess.check_output(cmd))
    pos1 = uuid.find("\\n")+2
    uuid = uuid[pos1:-15]
    print("Unique MAc ID = ", uuid )
    machine_unique_id = uuid
    return machine_unique_id

def versiontuple(ver):
    # Version no = '1.0.1.1'
    # Version no = (1, 0, 1, 1)
    return tuple(map(int, (ver.split("."))))

def GetAppVersionNo():
    ver_no = strObj.strVersionNo
    ver_no = versiontuple(ver_no)   
    print(f"Version no = {ver_no}")
    return ver_no



def Encrypt_Data( keyfilePath, file_data):
    crypter = objcrypt.Crypter('key', 'cbc')
    # encrypte now
    encrypted_dict = crypter.encrypt_object(file_data)
    with open(keyfilePath, 'w') as outfile:
        json.dump(encrypted_dict, outfile)
    print("Encrypt_Data done") 

def Decrypt_Data( keyfilePath ):
    crypter = objcrypt.Crypter('key', 'cbc')
    ##Read file to decrypt
    read_file_data = dict()
    with open( keyfilePath ) as f_data:
        read_file_data = json.load( f_data )
    # decrypt now
    dec_dict = crypter.decrypt_object(read_file_data)
    print("Decrypt_Data done")
    return dec_dict 



def VerifyKeyOnOur_WebServer( strKey, keycheckonrun = ""):
        # now_dd, now_mm, now_yy = datetime.now().strftime("%d-%m-%Y").split('-')
        # now_date_Info = date( int(now_yy), int(now_mm), int(now_dd) )
        
        # 0. SEND following information to our web server
        send_info_to_server = dict()
        myMacID = GetMachineUniqueID()
        myAppVerNo = GetAppVersionNo()
        send_info_to_server = {  
                    'key' : strKey, 
                    ##'current_date': now_date_Info, 
                    'mac_id' : myMacID,
                    'keycheckonrun' : keycheckonrun,
                    'ver_no': myAppVerNo
                }
        ###send_info_to_server = {'username':'Ajay','password':'ajay123'}
        ##--ajay----my_response = requests.post( self.strMyWebServeUrl, data = send_info_to_server)
        
        ## just to check------------------------------------------------------
        my_response = None
        try:
            sUrl =  URL_TO_VERIFY_KEY  +  strKey  + "/"
            ##---headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
            ##---my_response = requests.get(url=sUrl, params=send_info_to_server, headers=headers)
            my_response = requests.get( sUrl, data = send_info_to_server)
            
            print( my_response.status_code )
            my_response.raise_for_status()
            # access JSOn content
            jsonResponse = my_response.json()
            print(jsonResponse)
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
            msg.showinfo( strObj.strMsgTxt_TrialVer, strObj.strEnterValidKey )
            return (False, "")
        except Exception as err:
            print(f'Other error occurred: {err}')
            msg.showinfo( strObj.strMsgTxt_TrialVer, strObj.strFailedCon  )
            return (False, "")
        ##--------------------------------------------------------------------

        ###soup = BeautifulSoup(my_response.content)
        ## The result obtained from the above code is Python dictionary and is also in 'key-value'
        my_response_dictionary = my_response.json()
        print( my_response_dictionary )
        print(f" Final Status ==>{ my_response_dictionary['app_final_status'] } " )

        ##-----Get Response from WEB Server with following info--------------------------------server_response_
        # 1. verify key on our web server and Return True/ False according to key_DB
        # 2. and also return Expire Date in formate as "09-07-2020" 
        server_response_data = dict()
        if( 1 == my_response_dictionary['app_final_status'] ):

            server_response_bIsKeyVerify = True   

            server_response_Key = str(strKey)
            server_response_ExpireDate = my_response_dictionary['expire_date'] ## str("30-09-2020") ## "10-08-2020"
            server_response_allow_total_emp_count = my_response_dictionary['allow_emp_count'] ## str('10')
            server_response_machine_id = my_response_dictionary['mac_id'] ##  str("A63E11FF-7D9D-11E3-9DE6-618FE803C0FF")
            server_response_msg = my_response_dictionary['show_msg'] ## 'msg'
            
            server_response_data['key']  = str(server_response_Key)
            server_response_data['key2'] = str(server_response_ExpireDate)
            server_response_data['key3'] = str(server_response_allow_total_emp_count)
            server_response_data['key4'] = str(server_response_machine_id)
            server_response_data['key5'] = str(server_response_msg)


        else:
            server_response_data['key']  = str(my_response_dictionary['msg'])
            server_response_data['key2'] = str(my_response_dictionary['app_final_status'])            
            server_response_bIsKeyVerify = False
        ##-------------------------------------------------------------------------------------

        #3. Retuen both variables to set Aplication State
        return server_response_bIsKeyVerify, server_response_data  

def GetAppDataFolderPath():
    # C:\\ProgramData
    # sAppDir = os.environ['ALLUSERSPROFILE']
    # C:\\ProgramData\\log.txt
    # myappdir = os.path.join(sAppDir, "log.txt")

    # "sC:\\Users\\abc\\AppData\\Roaming"
    sAppDir = os.getenv('APPDATA')
    dirname =  strObj.strAppDataFolderName
    dir_path = f"{sAppDir}\\{dirname}\\"
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    print(dir_path)
    return dir_path

def GetUpdateFilePath():
        myfilePath = GetAppDataFolderPath()
        myfilePath = myfilePath + "update.fr"
        return myfilePath

def CheckIsUpdateAvailable():   
        bIsUpdateAvailable = False
        my_response = None
        try:
            send_info_to_server = dict()
            myAppVerNo = GetAppVersionNo()
            send_info_to_server = {  
                    'ver_no': myAppVerNo
                }
            sUrl =  URL_CHECK_UPDATE   
            ##---headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
            ##---my_response = requests.get(url=sUrl, params=send_info_to_server, headers=headers)
            my_response = requests.get( sUrl, data = send_info_to_server)
            
            print( my_response.status_code )
            my_response.raise_for_status()
            # access JSOn content
            jsonResponse = my_response.json()
            print(jsonResponse)
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')            
            return bIsUpdateAvailable
        except Exception as err:
            print(f'Other error occurred: {err}')            
            return bIsUpdateAvailable
        
        my_response_data = my_response.json()
        print( my_response_data )
        
        # save these info. in file 'update.fr' and save in '%appdata%' folder        
        myfilePath = GetUpdateFilePath()
        
        # # Let these data come from server
        # test_json = dict()
        # test_json = {
        #     'new_ver_no' : '1.0.1.9.9.9',
        #     'new_setup_url' : 'http://abcdef.com/setup99999.exe'
        # }

        with open( myfilePath, "w") as outfile: 
            # json.dump(test_json, outfile)
            json.dump(my_response_data, outfile)
            bIsUpdateAvailable = True

        print("Done")
        return bIsUpdateAvailable
        
import urllib.request 
def download_setup(dwn_url, dst_file_path, file_name):
    print('Beginning file download ...')    
    # response_data = requests.get(dwn_url, allow_redirects=True)
    # outfile = open( file_name, 'wb').write( response_data.content)
    # outfile.close()
    urllib.request.urlretrieve(dwn_url, dst_file_path + file_name) 

import subprocess as sp	
def install_setup(prog_path):
    process = sp.Popen(prog_path, shell=True)
    process.wait()

    