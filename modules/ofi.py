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

def ofi(client,equitycode):

	data=client.fetch_market_depth_by_scrip(Exchange="N",ExchangeType="C",ScripCode=equitycode)
	df = pd.DataFrame(data['MarketDepthData'])
	df['BuySell'] = df['BbBuySellFlag'].map({66: 'Buy', 83: 'Sell'})
	#print(df)
	df['Volume'] = df['NumberOfOrders']*df['Quantity']
	mask_1 = (df['BbBuySellFlag'] == 66)
	buy_orderbook = df.loc[mask_1]
	mask_2 = (df['BbBuySellFlag'] == 83)
	sell_orderbook = df.loc[mask_2]
		
	#It is debatable whether max function should be used instead of sum
	cum_bid_qty = buy_orderbook['Volume'].sum()
	cum_ask_qty = sell_orderbook['Volume'].sum()
	ofi=cum_bid_qty-cum_ask_qty
	#print("Order Flow Imbalance is : " + str(ofi))
	cum_bid_price = buy_orderbook['Price'].max()
	cum_ask_price = sell_orderbook['Price'].min()
	mid_price=(cum_bid_price+cum_ask_price)/2

	if ofi>0:
		position=1
	else:
		position=0
	
	return position


