import time
import datetime
import pytz
from Functions import firebaseInteraction as fi
from GlobalVariables import variables as vars

loop = True

def stopLoop():
    loop = False

def startLoop():
    loop = True
    while loop:
        time.sleep(60 * 30)
        vars.fbUser = vars.fbAuth.refresh(vars.fbUser['refreshToken'])
    
        tz = pytz.timezone('Asia/Manila') 
        timeObj = datetime.now(tz)
        timeStr = timeObj.strftime("%I:%M:%S %p | %a, %d/%m/%Y ")

        print(f"Token refreshed at {timeStr}.")
        