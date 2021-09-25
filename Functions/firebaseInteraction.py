import collections as cl
import os
import json

import pyrebase
import threading as thread

from Functions import customExceptions as ce
from Functions import firebaseResetToken as frt
from GlobalVariables import variables as vars


# new data
# db.child().set(data, token=getToken())

# # update
# db.child().update({"barkcount": 25010}, token=getToken())

# # delete
# db.child().remove(token=getToken())

# # get
# result = db.child().get(token=getToken()).val()

# Get data from keys in database
def getFromPath(path):
    if not isinstance(path, list):
        path = [path]

    final = vars.db
    for key in path:
        final = final.child(key)
    return final


# Get Data
def getData(path:list):
    result = getFromPath(path).get(token=vars.getToken()).val()
    
    if not result == None:
        value = result
        if isinstance(value, cl.OrderedDict):
            value = dict(result)
        return value
    else:
        error = "/".join(str(path))
        raise ce.FirebaseNoEntry(f"Data doesn't exist for '{error}'.")
    

# Check if data already exists
def isDataExists(path):
    if not isinstance(path, list):
        path = [path]

    try:
        getData(path)
        return True
    except ce.FirebaseNoEntry:
        return False


# Create
def createData(path, data):
    # if isDataExists(path):
    #     error = "/".join(path)
    #     raise ce.FirebaseNoEntry(f"Data already found for '{error}'.")
    
    pathParse = getFromPath(path)
    pathParse.set(data, token=vars.getToken())

# Edit
def editData(path, data):
    if not isDataExists(path):
        error = "/".join(path)
        raise ce.FirebaseNoEntry(f"Data can't be found for '{error}'.")

    pathParse = getFromPath(path)
    pathParse.update(data, token=vars.getToken())


# Delete
def deleteData(path):
    if isDataExists(path):
        error = "/".join(path)
        raise ce.FirebaseNoEntry(f"Data being deleted doesn't exist for '{error}'.")
    
    pathParse = getFromPath(path)
    pathParse.remove(token=vars.getToken())


newToken = thread.Thread(target=frt.startLoop)
newToken.daemon = True
newToken.start()