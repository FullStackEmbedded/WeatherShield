#!/usr/bin/python
##===============================================================##
## FULL STACK EMBEDDED 2016                                      ##
##===============================================================##
## File  :       FSEScheduler.py                                 ##
## Author:       FA                                              ##
## Board :       Raspberry Pi                                    ##
## Brief :       Anemometer & Wind direction					 ##
##				 ToDo:                                    	     ##
##						- Check the real name of wind dir sensor ##
##						- Add comments							 ##
## Note  :                                                       ##
##===============================================================##

## IMPORTS
from __future__ import print_function
from smbus import SMBus
import RPi.GPIO as GPIO
import time

##GLOBAL DEFINITION
DEBUG = 0

class SensorError(Exception):
   """Problem occured while communicating with sensor."""
class i2cError(SensorError):
   """Raised when the i2c error occurs"""

class WINDSENSOR:
    """Class to read ..."""
