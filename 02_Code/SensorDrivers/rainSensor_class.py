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
import RPi.GPIO as GPIO
import time, sys


##GLOBAL DEFINITION
DEBUG = 0

class SensorError(Exception):
   """Problem occured while communicating with sensor."""

class i2cError(SensorError):
   """Raised when the i2c error occurs"""

class RAINGAUGE:
    """Class to read the rain gauge sensor """

    python_version = sys.version_info.major

    def __init__(self, channel):
        """  """
        self._rGChannel =  channel
        self._rGCount   = 0
        try:
            GPIO.setmode(GPIO.BCM)
            # Set as input and activate pull-down
            GPIO.setup(self._rGChannel, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
            # Add interrupt event "_rGChannel", count on rising edge and add callback function "_rainGaugeCallback()"
            GPIO.add_event_detect(self._rGChannel, GPIO.RISING, callback =
                    self.rGCallback , bouncetime = 10)
            if DEBUG:
                print("Rain gauge successfully initialised")
        except Exception as e:
            print(e)
            raise SensorError('Rain gauge initialisation failed...')

    def rGCallback(self, channel):
        """ """
        self._rGCount += 1
        if DEBUG:
            print("Rain gauge returns ", self._rGCount, "counts")

    def rGread(self):
        """ Return Rain gauge value in [mm]"""
        return self._rGCount * 0.279

    def rGreset(self):
        """ resets RG counts"""
        self._rGCount = 0
        if DEBUG:
            print("Rain gauge reseted")

class SensorInterface(object):
    """ Abstract common interface for hardware sensors."""
    def __init__(self):
        self.error_count = 0
    def get_value(self):
        try:
            return self._get_value()
        except SensorError as e:
            if self.error_count < 3:
                pass
            else:
                raise e

    def _get_value():
        raise NotImplementedError

class RainGaugeSensor(SensorInterface):
    """ Implements common interface for rain gauge"""
    def __init__(self, channel):
        self._hw_sensor = RAINGAUGE(channel)
    def _get_value(self):
        """ Reads sensor value """
        return  self._hw_sensor.rGread()



if __name__ == "__main__":
    try:
        rG = RainGaugeSensor(18)
        while True:
            time.sleep(2)
            print(rG.get_value())
    except (KeyboardInterrupt, SystemExit):
        raise
    except Exception as e:
        print(e)
        GPIO.cleanup()
        sys.exit
