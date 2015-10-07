#!/usr/bin/python

##==============================================================================##
## FULL STACK EMBEDDED 2016                                                     ##
##==============================================================================##
## File  :       run_sht21.py                                                   ##
## Author:       FA                                                             ##
## Board :       Raspberry Pi                                                   ##
## Brief :       sht21 main()                      ##
## Note  :                                                                      ##
##==============================================================================##

import sht21_class
import time


# Create an instance 
sht21 = sht21_class.SHT21()


while 1:
    sht21.getTemperature()
    sht21.getHumidity()
    time.sleep(1)
