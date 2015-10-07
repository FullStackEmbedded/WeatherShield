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
mpl3115a2.SHT21()

while 1:
	print(sht21_class.getTemperature())
	time.sleep(1)