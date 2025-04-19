#--------------------------------------------------------------------
#IMPORT ALL EXTERNAL REQUIRED LIBRARIES & DEPENDENCIES
#--------------------------------------------------------------------
import pandas as pd
import datetime
import os
import json
from pandas import json_normalize
import time

#--------------------------------------------------------------------
#IMPORT ALL INTERNAL REQUIRED LIBRARIES & DEPENDENCIES
#--------------------------------------------------------------------
from modules.ofi import *

#--------------------------------------------------------------------
#LOGIN CREDENTIALS
#SECURE ENCRYPTION NEEDS TO BE ESTABLISHED FOR THIS
#--------------------------------------------------------------------

def init_pos(client,equitycode):
	pos1=ofi(client,equitycode)
	time.sleep(10)
	#print("Waiting to get data")
	pos2=ofi(client,equitycode)
	time.sleep(10)
	#print("Waiting to get data")
	pos3=ofi(client,equitycode)
	cum_pos=pos1+pos2+pos3
	if cum_pos==3:
		return 1
	else:
		return 0


