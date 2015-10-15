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
    _SLAVE_ADDRESS = 0x48
    _TEMP_REGISTER = 0x00
    _CONFIGURATION_REGISTER = 0x1

	# Wait a bit more than recommended
    def __init__(self, device_number = 1):
        """Opens the i2c device (assuming that the kernel modules have been
        loaded)"""
        self.bus = SMBus(device_number)
        # set pointerregister -> configuration register
        #self.bus.write_byte_data(self._SLAVE_ADDRESS,self._CONFIGURATION_REGISTER,0x60)
        #self.bus.write_byte(self._SLAVE_ADDRESS,self._CONFIGURATION_REGISTER)
        #self.bus.write_byte(self._SLAVE_ADDRESS,0xE1)
        self.bus.write_byte(self._SLAVE_ADDRESS,self._TEMP_REGISTER)

        time.sleep(0.015)
        if DEBUG:
            print("TMP100 init done.")

    def getTemperature(self):
        """Reads the temperature from the sensor."""
        tmp_msb = self.bus.read_byte(self._SLAVE_ADDRESS)
        tmp_lsb = self.bus.read_byte(self._SLAVE_ADDRESS)
        #return hex(self.bus.read_byte(self._SLAVE_ADDRESS))
        return   tmp_msb + (tmp_lsb >>4)

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

class TMP100_Sensor(SensorInterface):
    """Sensor using SHT21 hardware."""

    def __init__(self):
        super(TMP100_Sensor, self).__init__()
        self._hw_sensor = TMP100()

class TemperatureSensor(TMP100_Sensor):
    """Implements common interface for temperatur sensor"""

    def _get_value(self):
        """Read sensor value."""
        return self._hw_sensor.getTemperature()



if __name__ == "__main__":
    tmp100 = TMP100()
    while 1:
        print(tmp100.getTemperature())
        time.sleep(1)
