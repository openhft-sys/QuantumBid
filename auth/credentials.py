#--------------------------------------------------------------------
#IMPORT ALL EXTERNAL REQUIRED LIBRARIES & DEPENDENCIES
#--------------------------------------------------------------------
import pandas as pd
import datetime
import os
import json
from pandas import json_normalize

#--------------------------------------------------------------------
#LOGIN CREDENTIALS
#SECURE ENCRYPTION NEEDS TO BE ESTABLISHED FOR THIS
#--------------------------------------------------------------------


def api_login():

    from py5paisa import FivePaisaClient
    cred={
        "APP_NAME":"XXXXXX",
        "APP_SOURCE":"YYYY",
        "USER_ID":"ZZZZ",
        "PASSWORD":"EEEEEEE",
        "USER_KEY":"AAAASSSSS",
        "ENCRYPTION_KEY":"SSSDSDSDSDSD"
        }
    
    
    client = FivePaisaClient(cred=cred)
    client.get_totp_session('CLIENTID',input("enter totp >>> "),'DATEOFBIRTH')

    return client