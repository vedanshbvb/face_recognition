from pymongo import MongoClient
import os 
import subprocess

## Install Mongodb setup "mongodb-win32-x86_64-2008plus-ssl-3.4.10-signed.msi"

def StartMyMongoDB():

    # Prevent cmd.exe window from popping up
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= (
            subprocess.STARTF_USESTDHANDLES | subprocess.STARTF_USESHOWWINDOW
            )
    startupinfo.wShowWindow = subprocess.SW_HIDE

    ## for .bat file ===>  mongod --port 27017 --dbpath "C:\data\db"
    path_to_database = "C:\data\db"
    connection = subprocess.Popen(  ['mongod', '--dbpath', os.path.expanduser(path_to_database)],  startupinfo=startupinfo  )
    ##print(f"MongoDb connection status = {connection} ")
     
    return connection

def StopMyMongoDB():
    ## for .bat file ===> mongo admin --eval "db.shutdownServer()"
    client = MongoClient()
    client.close()
    print("Stop Mongodb")
     