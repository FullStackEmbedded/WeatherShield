#!/usr/bin/python

##==============================================================================##
## FULL STACK EMBEDDED 2016                                                     ##
##==============================================================================##
## File  :       run_mpl3115a2.py                                                   ##
## Author:       FA                                                             ##
## Board :       Raspberry Pi                                                   ##
## Brief :       sht21 main()                      ##
## Note  :                                                                      ##
##==============================================================================##
import mpl3115a2_class
import time

# Create an instance
mpl3115a2 = mpl3115a2_class.MPL3115A2()

while 1:
	#mpl3115a2.getAirPressure()
	time.sleep(1)
