#!/bin/python
##==============================================================================
## FULL STACK EMBEDDED 2016
##==============================================================================
## File  :       windVane.py
## Author:       FA
## Board :       Raspberry Pi
## Brief :       Sensor Layer. Functions for sensor access
## Date:
## Note  :
##==============================================================================

## IMPORTS
from __future__ import print_function
from ads1015_class import ADS1015
import time

##GLOBAL DEFINITION
DEBUG = 0

class SensorError(Exception):
     """Problem occured while communicating with sensor.""" 
class i2cError(SensorError):  
    """Raised when the i2c error occurs"""


class WINDVANE:
    """ class to read wind direction from wind vane sensor """
    def __init__(self):
        self.WVchannel = 0
        self.windVane = ADS1015(1,self.WVchannel)

    def getWindDirection(self):
        """ """
        return self.windVane.readAnalogChannel()



class SensorInterface(object):
    """ Abstract common interface for hardware  sensors."""
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


class WindVaneSensor(SensorInterface):
    """ Implement common interface for wind vane sensor"""
    def __init__(self):
        self._hw_sensor = WINDVANE()

    def _get_value(self):
        """ reads sensor value"""
        return self._hw_sensor.getWindDirection()



if __name__ == "__main__":
    WV =  WindVaneSensor()
    while True:
        print("Wind direction [deg] = ", WV.get_value())
        time.sleep(0.1)
