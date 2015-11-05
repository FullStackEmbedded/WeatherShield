#!/bin/python
##==============================================================================##
## FULL STACK EMBEDDED 2016                                                     ##
##==============================================================================##
## File  :       ads1015_class.py                                               ##
## Author:       FA                                                             ##
## Board :       Raspberry Pi                                                   ##
## Brief :       Sensor Layer. Functions for sensor access                      ##
## Date:                                                                        ##
## Note  :                                                                      ##
##==============================================================================##

## IMPORTS
from __future__ import print_function
from smbus import SMBus
import time

##GLOBAL DEFINITION
DEBUG = 0

class SensorError(Exception):
     """Problem occured while communicating with sensor.""" 
class i2cError(SensorError):
    """Raised when the i2c error occurs"""


class ADS1015:
    """ Class ro read analog values"""
    #control constants
    _SLAVE_ADDR = 0x48
    # pointer register
    _POINTER_CONFIG_REG = 0x01
    _POINTER_CONVERT_REG = 0x00

    # config register
    _CONFIG_MUX_SINGLE_0  = 0x4000    # single ended AIN 0
    _CONFIG_MUX_SINGLE_1  = 0x5000    # single ended AIN 1
    _CONFIG_MUX_SINGLE_2  = 0x6000    # single ended AIN 2
    _CONFIG_MUX_SINGLE_3  = 0x7000    # single ended AIN 3

    _CONFIG_PGA_6114    = 0x00
    _CONFIG_MODE_CONT   = 0x00
    _CONFIG_MODE_SINGLE = 0x100

    _CONFIG_OS_SINGLE   = 0x8000
    _CONFIG_OS_BUSY     = 0x00
    _CONFIG_NOT_BUSY    = 0x8000

    _CONFIG_DATA_RATE   = 0x80      #1600 Samples/s
    _CONFIG_COMP_MODE   = 0x00
    _CONFIG_POL         = 0x00
    _CONFIG_LAT         = 0x00
    _CONFIG_QUE         = 0x3


    def __init__(self, device_number = 1):
        """ Open the i2c device and configure the sensor """
        self.bus = SMBus(device_number)
        time.sleep(0.005)
        #write config register
        try:
            config = self._CONFIG_MUX_SINGLE_1 | self._CONFIG_PGA_6114 | self._CONFIG_MODE_CONT | self._CONFIG_DATA_RATE | self._CONFIG_COMP_MODE | self._CONFIG_POL | self._CONFIG_LAT | self._CONFIG_QUE
            self.bus.write_word_data(self._SLAVE_ADDR,self._POINTER_CONFIG_REG, config )
        except Exception as e:
            print(e)
            raise i2cError("I2C error occurs while configuring ADS1015")

        #point to conversion register
        #self.bus.write_byte(self._SLAVE_ADDR, self._POINTER_CONVERT_REG)


    def read(self, channel=0, pga = 6144, sps = 1600):
        """ Gets a single-ended ADC reading from the specified channel in mV. """
        config = self._CONFIG_MUX_SINGLE_1 | self._CONFIG_PGA_6114 | self._CONFIG_MODE_CONT | self._CONFIG_DATA_RATE | self._CONFIG_COMP_MODE | self._CONFIG_POL | self._CONFIG_LAT | self._CONFIG_QUE

        # Set the channel to be converted
        if channel == 3:
            config |= self._CONFIG_MUX_SINGLE_3
        elif channel == 2:
            config |= self._CONFIG_MUX_SINGLE_2
        elif channel == 1:
            config |= self._CONFIG_MUX_SINGLE_1
        else:
            config |= self._CONFIG_MUX_SINGLE_0
        # Begin Conversation
        config |= self._CONFIG_OS_SINGLE

        self.bus.write_word_data(self._SLAVE_ADDR,self._POINTER_CONFIG_REG,config)
        time.sleep(0.005)
        #Read conversation result
        val =self.bus.read_word_data(self._SLAVE_ADDR,self._POINTER_CONVERT_REG)
        return ( val  >> 4 )* pga / 2048.0

if __name__ == "__main__":
    ads1015 = ADS1015()
    while True:
        print(ads1015.read(2, 6144, 1600))
        time.sleep(1)

