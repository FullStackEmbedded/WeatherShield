#!/usr/bin/python

##==============================================================================##
## FULL STACK EMBEDDED 2016                                                     ##
##==============================================================================##
## File  :       tmp100_class.py                                                ##
## Author:       FA                                                             ##
## Board :       Raspberry Pi                                                   ##
## Brief :       Sensor layer. Functions for sensor access                      ##
## Note  :                                                                      ##
##==============================================================================##

## IMPORTS
from __future__ import print_function
from smbus import SMBus
import time

##GLOBAL DEFINITION
DEBUG = 1

class SensorError(Exception):
   """Problem occured while communicating with sensor."""
class i2cError(SensorError):
   """Raised when the i2c error occurs"""

class TMP100:
    """Class to read temperature and humidity from SHT21"""

	## Control constants
    _SLAVE_ADDRESS = 0x00
    _config = 

	# Wait a bit more than recommended
    def __init__(self, device_number = 1):
        """Opens the i2c device (assuming that the kernel modules have been
        loaded) & run soft reset. (user register leaved to default value)"""
        self.bus = SMBus(device_number)
        self.bus.write_byte(self._SLAVE_ADDRESS, self._SOFTRESET)
        time.sleep(0.015)
        if DEBUG:
            print("SHT21 init done.")

    def getTemperature(self):
        """Reads the temperature from the sensor."""


    @staticmethod
    def _get_temperature_from_buffer(data):
        """ """



class SensorInterface(object):
    """Abstract common interface for hardware sensors."""
    def __init__(self):
        self.error_count = 0

    def get_value(self):
        try:
            return self._get_value()
        except SensorError as e:
            # TODO: Let errors expire after given time
            if self.error_count < 3:
                pass
            else:
                raise e

    def _get_value():
        raise NotImplementedError

class SHT21_Sensor(SensorInterface):

    """Sensor using SHT21 hardware."""

    def __init__(self):
        super(SHT21_Sensor, self).__init__()
        self._hw_sensor = SHT21()

class TemperatureSensor(SHT21_Sensor):

    """Implements common interface for temperatur sensor"""

    def _get_value(self):
        """Read sensor value."""
        return self._hw_sensor.getTemperature()

class HumiditySensor(SHT21_Sensor):

    """Implements common interface for humidity sensor"""

    def _get_value(self):
        """Read sensor value."""
        return self._hw_sensor.getHumidity()



if __name__ == "__main__":
    sht = SHT21()
    while 1:
        print(sht.getTemperature())
        time.sleep(1)
