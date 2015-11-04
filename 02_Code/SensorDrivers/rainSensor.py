#!/usr/bin/python
##============================================================##
## FULL STACK EMBEDDED 2016                                   ##
##============================================================##
## File  :       rainSensor.py                                ##
## Author:       FA                                           ##
## Board :       Raspberry Pi                                 ##
## Brief :       Rain gauge function                          ##
##				 ToDo:                                    	  ##
##						- Add comments 						  ##
## Note  :                                                    ##
##============================================================##

## IMPORTS
from __future__ import print_function
#from datetime import datetime, timedelta
import RPi.GPIO as GPIO
import time, sys


##GLOBAL DEFINITION
DEBUG = 0

class SensorError(Exception):
   """Problem occured while communicating with sensor."""
class i2cError(SensorError):
   """Raised when the i2c error occurs"""

class RAINGAUGE:
    """Class to read ..."""

    python_version = sys.version_info.major

    def __init__(self,channel = 18):
        """  """
        self._rGChannel = channel
        self._rGCount   = 0
        try:
            # SoC as Pinreferenz
            GPIO.setmode(GPIO.BCM)
            # declare _rGChannel as input 6 activate Pull-Down
            GPIO.setup(self._rGChannel, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
            # Add interrupt event "_rGChannel", count on rising edge and add callback function "_rainGaugeCallback()"
            GPIO.add_event_detect(self._rGChannel, GPIO.RISING, callback = self.rainGaugeCallback, bouncetime = 10)
        except Exception as e:
            print(e)
            raise SensorError('Rain gauge initialisation failed...')

	def rainGaugeCallback(self):
		""" """
		self._rGCount += 1

	def readrG(self):
		""" """
		return self._rGValToBebeReturned


if __name__ == "__main__":
    rG = RAINGAUGE()
    while True:
        time.sleep(2)
