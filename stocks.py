#!/usr/bin/env python3

#Programmer: Nicholas Grosso
#Program: Project 2
#Date: 4/24/2019

import sys
import re
import requests

url = 'http://tophat.sunywcc.edu/~smiller/stock.py'

#Pre-condition: Successful process
#Post-condition: Returns the name of the company 
def getName(S):
#Get to the proper line with the name of the company
	companyNamefull = S.split('\n', 5)[2]
#Subtracting the constant length of the line by the length of the companies name as a string
	length = len(companyNamefull) - 12
	return companyNamefull[-length:]

#Pre-condition: Successful process
#Post-condition: Returns the current price of the company's stock
def getPrices(S):
	pricelinefull = S.split('\n', 5)[4]
	plength = len(pricelinefull) - 12
	return pricelinefull[-plength:]

#Pre-condition: Successful process
#Post-condition: Returns the highest price within 52 weeks of the company's stock
def getHPrices(S):
	Hpricelinefull = S.split('\n', 9)[6]
	Hplength = len(Hpricelinefull) - 11
	return Hpricelinefull[-Hplength:]

#Pre-condition: Successful process
#Post-condition: Return the lowest price within 52 weeks of the company's stock
def getLPrices(S):
	Lpricelinefull = S.split('\n', 9)[7]
	Llength = len(Lpricelinefull) - 10
	return Lpricelinefull[-Llength:]

#Pre-condition: Successful process
#Post-condition: Return the ratio of the company's stock
def getRatio(S):
	Ratiolinefull = S.split('\n', 9)[8]
	Rlength = len(Ratiolinefull) - 18
	Rreturn = Ratiolinefull[-Rlength:]
	return re.sub('\t', '', Rreturn)

#Pre-condition: Whats being passed has not failed the processing and the checkpoints
#Post-condition: Displays data to stdout cleanly
def display(price, high, low, ratio, index2, R):
	spacenum0 = 11 - len(sys.argv[index2])
	length0 = spacenum0 * " "
	spacenum1 = 10 - len(price)
	length1 = spacenum1 * " "
	spacenum2 = 9 - len(high)
	length2 = spacenum2 * " "
	spacenum3 = 8 - len(low)
	length3 = spacenum3 * " "
	spacenum4 = 10 - len(ratio)
	length4 = spacenum4 * " "
	if R == False:
		R = "Buy"
	else:
		R = "Sell"
	spacenum5 = 7 - len(R)
	length5 = spacenum5 * " "	
	print(sys.argv[index2], length0, price, length1, high, length2, low, length3, ratio, length4, R)

#Pre-condition: Successful process
#Post-condition: Returns true to say that the average price is greater than the current price
def recomend(x, y, z):
#Calculating the average price using the lowest and highest price of 52 weeks
	avg = ((float(y) + float(z)) / 2.0)
	if avg > float(x):
		return True
	else:
		return False
	

#If statement will output an error to stderr if there are 0 arguemnts being passed through
if len(sys.argv) == 1:
	print("Error: No arguemnts have been passed through", file=sys.stderr)
	sys.exit(1)

def todo():
#Displays a sperate area for the data of the company
	print("\nSymbol       Price       High       Low       Ratio       Rec")

	for index2 in range(len(sys.argv)):
		if sys.argv[index2] == sys.argv[0]:
			pass
		else:
			stockinfo = requests.get(url, {'ticker':sys.argv[index2]})
#As said on line 72, this will be cleaning up the wasteful space in stockstring... not needed
			stock = re.sub("Content-type: text/html", "", stockinfo.text)
			stock = re.sub("Unknown symbol", "", stock)
			stock = re.sub("\n\s*\n*", "\n", stock)
			R = recomend(getPrices(stock), getHPrices(stock), getLPrices(stock))
			display(getPrices(stock), getHPrices(stock), getLPrices(stock), getRatio(stock), index2, R)

e = False
for index in range(len(sys.argv)):
	r = requests.get(url, {'ticker':sys.argv[index]})
#Cleaning up the look of output... not needed
	s = re.sub("Content-type: text/html", "", r.text)
	s = re.sub("Unknown symbol", "", s)
	s = re.sub("\n\s*\n*", "\n", s)
#If statements will remove the first arguemnt from the list, and process acceptable arguemnts
	if sys.argv[index] == sys.argv[0]:
                pass
	elif not re.findall(sys.argv[index], s) == []:
		print("Processing:", getName(s))
		e = True
	else:
		print("Processing failure of ticker:", sys.argv[index])
		

#Displays a sperate area for the data of the company, if any only if there is at least one succesful process of a ticker
if e == True:
	print("\nSymbol       Price       High       Low       Ratio       Recomendation")

#check will prevent an if statement from exiting before all arguemnts have been read
check = False

for index2 in range(len(sys.argv)):
	stockinfo = requests.get(url, {'ticker':sys.argv[index2]})
#As said on line 72, this will be cleaning up the wasteful space in stockstring
	stock = re.sub("Content-type: text/html", "", stockinfo.text)
	stock = re.sub("Unknown symbol", "", stock)
	stock = re.sub("\n\s*\n*", "\n", stock)

#If the arguemnt being passed is the very 1st thing, (the ./stocks), ignore it
	if sys.argv[index2] == sys.argv[0]:
		pass
#If argument being passed is not processed...
	elif re.findall(sys.argv[index2], stock) == []:
#and is the last arguemnt, send message to stderr
		if index2 == len(sys.argv):
			print("Error: nope", file=sys.stderr)
			sys.exit(2)
#else, make check true so it can be passed on by the next check to exit after everything has been read
		else:
			check = True
	elif index2 == len(sys.argv) and check == True:
		if re.findall(sys.argv[index2], stock) == []:
			print("Error: nope2", file=sys.stderr)
			sys.exit(3)
		else:
			display(getPrices(stock), getHPrices(stock), getLPrices(stock), getRatio(stock), index2)
#Send all data to stdout
	else:
		R = recomend(getPrices(stock), getHPrices(stock), getLPrices(stock))
		display(getPrices(stock), getHPrices(stock), getLPrices(stock), getRatio(stock), index2, R)

sys.exit(0)
