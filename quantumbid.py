#--------------------------------------------------------------------
#IMPORT ALL EXTERNAL REQUIRED LIBRARIES & DEPENDENCIES
#--------------------------------------------------------------------
import pandas as pd
import datetime
import os
import json
from pandas import json_normalize
import time
import math
#import termplotlib as tpl
import plotext as plt
import datetime;


#--------------------------------------------------------------------
#IMPORT ALL INTERNAL REQUIRED LIBRARIES & DEPENDENCIES
#--------------------------------------------------------------------
from auth.credentials import *
from modules.ofi import *
from modules.init_pos import *
from modules.orderbook import *


#--------------------------------------------------------------------
#SET UP GLOBAL PARAMETERS
#--------------------------------------------------------------------
equitycode="17963"
equityname="NESTLEIND"
hol_vol=0
pos_size=25
avg_price=0
hol_threshold=200
epsilon=1.05


#--------------------------------------------------------------------
#SET UP LOG TABLE
#--------------------------------------------------------------------
#log= pd.DataFrame(columns=['Timestamp','Equityname','OrderType','PositionSize','Price','Cost'])
log=[]
column_names=['Timestamp','Equityname','OrderType','PositionSize','Price','Cost']
#log.append([a, b, c])

#--------------------------------------------------------------------
#LOGIN CREDENTIALS
#SECURE ENCRYPTION NEEDS TO BE ESTABLISHED FOR THIS
#--------------------------------------------------------------------

client=api_login()


while True:

	print("-------------------------------------------------------------")
	print("-------------------------QUANTUM BID-------------------------")
	print("-------------------------------------------------------------")
	print(" ")
	print(" ")
	
	print("Fetching OrderBook data to determine Bid-Ask quantity for "+str(equityname))
	print(" ")
	df=orderbook(client,equitycode)
		
	x = df['NumberOfOrders']
	y = df['Price']

	#Take Decision on whether Charts look better or actual DataFrame
	plt.simple_bar(x, y,width = 100, title = 'Orderbook Data')
	plt.show()
	

	pos=init_pos(client,equitycode)
	#print("The position is " + str(pos))
	if pos==1 and hol_vol<hol_threshold:
		print("Entering Long Trade with position size of "+str(pos_size))
		#client.place_order(OrderType='B',Exchange='N',ExchangeType='C', ScripCode = equitycode, Qty=pos_size, Price=0, AHPlaced="Y")
		scrip_info=client.query_scrips("N","C",equityname,"0","XX","")
		price=float(scrip_info['StrikeRate'])
		log.append([datetime.datetime.now(),equityname,'Buy',pos_size,price,pos_size*price])
		avg_price=((avg_price*hol_vol)+(price*pos_size))/hol_vol+pos_size
		hol_vol=hol_vol+pos_size


	else:
		if hol_vol>0:
			scrip_info=client.query_scrips("N","C",equityname,"0","XX","")
			price=float(scrip_info['StrikeRate'])
			if price>=(avg_price*epsilon):
				#client.place_order(OrderType='S',Exchange='N',ExchangeType='C', ScripCode = equitycode, Qty=hol_vol, Price=price, AHPlaced="Y")
				print("Position Cleared at "+str(price)+" with total outflow of "+str(price*hol_vol))
				log.append([datetime.datetime.now(),equityname,'Sell',hol_vol,price,hol_vol*price])
				hol_vol=0
			else:
				print("Liquidation Price is not favorable hence no trade initiated for existing portfolio")


		else:
			print("Order Flow is Negative with more sellers than buyers")
			print("No Long Trade was intiated")
			print("No Holding Position to liquidate")
			log.append([datetime.datetime.now(),equityname,'No Action',0,0,0])
			print(" ")
				
	print("----------------------------------------------------------------")
	print("Waiting for 10 secs before executing next order flow transaction")
	#print("Printing LOG")
	#print(log)
	log_df = pd.DataFrame(log, columns=column_names)
	log_df.to_csv('data/execution_log.csv', index=False)
	#print(log_df)
	time.sleep(10)
	os.system('cls')