#!/usr/bin/python
##===============================================================##
## FULL STACK EMBEDDED 2016                                      ##
##===============================================================##
## File  :       FSEScheduler.py                                 ##
## Author:       FA                                              ##
## Board :       Raspberry Pi                                    ##
## Brief :       Anemometer & Wind direction                     ##
##               ToDo:                                           ##
##                      - Check the real name of wind dir sensor ##
##                      - Add comments                           ##
## Note  :                                                       ##
##===============================================================##

## IMPORTS
from __future__ import print_function
from smbus import SMBus
from datetime import datetime, timedelta
import RPi.GPIO as GPIO
import time

##GLOBAL DEFINITION
DEBUG = 1 #DEBUG flag. Set to 1 to see outputs

class SensorError(Exception):
   """Problem occured while communicating with sensor."""
class i2cError(SensorError):
   """Raised when the i2c error occurs"""

class WINDSENSOR:
    """Class to read the anemometer and the wind vane """
    python_version = sys.version_info.major
    
    def __init__(self, AnemometerChannel):
        """ """
        self._anemoCh       = AnemometerChannel
        self._anemoCount    = 0
        self._anemolastCountTimeDelta = datetime.now()
        try:
            GPIO.setmode(GPIO.BCM)
            # Set as input and activate pull-down
            GPIO.setup(self._anemoCount, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
            # Add interrupt event "_rGChannel", count on rising edge and add callback function "_rainGaugeCallback()"
            GPIO.add_event_detect(self._anemoCount, GPIO.RISING, callback = self.AnemometerCallback, bouncetime = 10)
            if DEBUG:
                print("Rain gauge successfully initiallised")
        except Exception as e:
            print(e)
            raise SensorError('Rain gauge initialisation failed...')

    def AnemometerCallback(self):
        """ """
        tmp = datetime.now()
        t_elapsed_s = self._anemolastCountTimeDelta - tmp
        if DEBUG:
            print("wind speed = ", 2.401 / t_elapsed_s)
        
        self._anemolastCountTimeDelta = tmp

            
            
            
            
            
            
            
            
            
            
            
            
            
            
            