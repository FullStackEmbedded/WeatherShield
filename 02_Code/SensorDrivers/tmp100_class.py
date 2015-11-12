#!/usr/bin/python
##==============================================================================##
## FULL STACK EMBEDDED 2016                                                     ##
##==============================================================================##
## File  :       ds3231                                                         ##
## Author:       FA                                                             ##
## Board :       Raspberry Pi                                                   ##
## Brief :       Sensor Layer. Functions for sensor access                      ##
## Date  :       08.11.2015
## Note  :                                                                      ##
##==============================================================================##

## IMPORTS
from __future__ import print_function
import time
from smbus import SMBus

##GLOBAL DEFINITION
DEBUG = 0

class SensorError(Exception):
     """Problem occured while communicating with sensor.""" 
class i2cError(SensorError):  
    """Raised when the i2c error occurs"""
class ConfigError(SensorError):
    """Raised when the i2c error occurs"""

class TMP100:
    """ Class to read the onboard temperatur Sensor"""

    _SLAVE_ADDR = 0x49
    _CONFIG_REG = 0x01
    _TEMP_REG = 0x00
    # config register
    _CONFIG_REG_OS = 0x01
    _CONFIG_REG_RES_9B = 0x00
    _CONFIG_REG_RES_12B = 0x03
    _CONFIG_REG_TRIG_OS = 0x80
    def __init__(self,device_number = 1):
        """ """
        try:
            self.bus = SMBus(device_number)
        except Exception:
            raise i2cError()
        configList = [self._CONFIG_REG_OS, self._CONFIG_REG_RES_12B]
        self.configTMP100(configList)

    def configTMP100(self, list):
        """ Write list elements to tmp100#s configuration register"""
        reg = (list[1] << 5) + list[0]
        # write to config register
        self.bus.write_byte_data(self._SLAVE_ADDR,self._CONFIG_REG,reg)
        if DEBUG:
            # read config register back
            tmpReg = self.bus.read_byte_data(self._SLAVE_ADDR,self._CONFIG_REG)
            print(reg,tmpReg)

    def  getTemperature(self):
        """ Get temperature readings """
        # read first config register
        config = self.bus.read_byte_data(self._SLAVE_ADDR,self._CONFIG_REG)
        #trigger single shot
        newConfig = config + self._CONFIG_REG_TRIG_OS
        # write config register new value back
        self.bus.write_byte_data(self._SLAVE_ADDR,self._CONFIG_REG,newConfig)
        time.sleep(0.001) # wait a bit
        #read temperature register
        raw = self.bus.read_i2c_block_data(self._SLAVE_ADDR,self._TEMP_REG)[:2]
        val = ((raw[0] << 8) + raw[1]) >> 4

        #TODO: get resolution factor properly :)
        return val*0.0625

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

class OnBoardTemperaturSensor(SensorInterface):
    """ Implements common interface for MPL3115A2 (AirPressure/Altimeter)"""
    def __init__(self):
        self._hw_sensor = TMP100()
    def _get_value(self):
        """ Reads sensor value """
        return  self._hw_sensor.getTemperature()


if __name__ == "__main__":
    OnBoardTmp =OnBoardTemperaturSensor()
    while True:
        time.sleep(1)
        print(OnBoardTmp.get_value())
