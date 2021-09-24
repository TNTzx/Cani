import collections as cl
import os
import json

import pyrebase
from requests.api import get

from Functions import customExceptions as ce


env = os.environ["CaniDBToken"]
envDict = json.loads(env)

dbKey = envDict["databaseKey"]

fb = pyrebase.initialize_app(dbKey)
db = fb.database()
fbAuth = fb.auth()

envAuth = envDict["auth"]
fbUser = fbAuth.sign_in_with_email_and_password(envAuth["email"], envAuth["password"])
fbToken = fbUser['idToken']


def refreshToken():
    fbAuth.refresh(fbUser['refreshToken'])

# new data
# db.child().set(data, token=fbToken)

# # update
# db.child().update({"barkcount": 25010}, token=fbToken)

# # delete
# db.child().remove(token=fbToken)

# # get
# result = db.child().get(token=fbToken).val()

# Get data from keys in database
def getFromPath(path):
    if not isinstance(path, list):
        path = [path]

    final = db
    for key in path:
        final = final.child(key)
    return final


# Get Data
def getData(path:list):
    result = getFromPath(path).get(token=fbToken).val()
    
    if not result == None:
        value = result
        if isinstance(value, cl.OrderedDict):
            value = dict(result)
        return value
    else:
        error = "/".join(path)
        raise ce.FirebaseNoEntry(f"Data doesn't exist for '{error}'.")
    

# Check if data already exists
def isDataExists(path):
    try:
        getData(path)
        return True
    except ce.FirebaseNoEntry:
        return False


# Create
def createData(path, data):
    if isDataExists(path):
        error = "/".join(path)
        raise ce.FirebaseNoEntry(f"Data already found for '{error}'.")
    
    pathParse = getFromPath(path)
    pathParse.set(data, token=fbToken)

# Edit
def editData(path, data):
    if not isDataExists(path):
        error = "/".join(path)
        raise ce.FirebaseNoEntry(f"Data can't be found for '{error}'.")

    pathParse = getFromPath(path)
    pathParse.update(data, token=fbToken)


# Delete
def deleteData(path):
    if isDataExists(path):
        error = "/".join(path)
        raise ce.FirebaseNoEntry(f"Data being deleted doesn't exist for '{error}'.")
    
    pathParse = getFromPath(path)
    pathParse.remove(token=fbToken)