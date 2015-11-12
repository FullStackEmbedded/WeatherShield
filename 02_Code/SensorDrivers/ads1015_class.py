#!/usr/bin/python
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
DEBUG = 1

class SensorError(Exception):
     """Problem occured while communicating with sensor.""" 
class i2cError(SensorError):
    """Raised when the i2c error occurs"""
class ConfigError(SensorError):
    """ Cannot configure ADS1015"""


class ADS1015:
    """ Class ro read analog values"""
    #control constants
    _SLAVE_ADDR = 0x48
    # pointer register
    _POINTER_REG_CONVERSION = 0x00
    _POINTER_REG_CONFIG     = 0x01

    # configuration register
    _CONFIG_REG_MUX_CH0 = 0x04
    _CONFIG_REG_MUX_CH1 = 0x05
    _CONFIG_REG_MUX_CH2 = 0x06
    _CONFIG_REG_MUX_CH3 = 0x07
    _CONFIG_REG_PGA_6144 = 0x00
    _CONFIG_REG_PGA_4096 = 0x01
    _CONFIG_REG_MODE_CONT = 0x00
    _CONFIG_REG_MODE_SING = 0x01
    _CONFIG_REG_DR_250SPS = 0x01
    _CONFIG_REG_COMP_OFF = 0x3

    def __init__(self,device_number,channel):
        """ """
        try:
            self.bus = SMBus(device_number)
        except Exception:
            raise i2cError()

        try:
            if channel ==3:
                self.CH = self._CONFIG_REG_MUX_CH3
            elif channel == 2:
                self.CH = self._CONFIG_REG_MUX_CH2
            elif channel == 1:
                self.CH = self._CONFIG_REG_MUX_CH1
            else:
                self.CH = self._CONFIG_REG_MUX_CH0

            # MUX PGA MODE DR COMP_QUE
            confList =  [ self.CH,      \
                          self._CONFIG_REG_PGA_4096,     \
                          self._CONFIG_REG_MODE_CONT,    \
                          self._CONFIG_REG_DR_250SPS,    \
                          self._CONFIG_REG_COMP_OFF ]
            self.configADS1015(confList)
            # set conversion factor
            if confList[1] == self._CONFIG_REG_PGA_6144:
                self.convFactor = 6.144*2.0/4096
            elif confList[1] == self._CONFIG_REG_PGA_4096:
                self.convFactor = 4.096*2.0/4096



        except Exception as e:
            print(e)
            raise ConfigError()

    def configADS1015(self, list):
        """ configure the chip according to list"""
        MSB = (list[0]<<4)+ (list[1]<<1) + list[2]
        LSB = (list[3]<<5) + list[4]

        # write list to config register
        self.bus.write_i2c_block_data(self._SLAVE_ADDR,self._POINTER_REG_CONFIG,[MSB, LSB])
        if DEBUG:
            print("configList:", list)
            print("MSB: ", MSB, "LSB: ", LSB)
            #read register back
            Data = self.bus.read_i2c_block_data(self._SLAVE_ADDR,self._POINTER_REG_CONFIG)[:2]
            #print ( "To be written: ",MSB, LSB)
            print (" Read back :  ",Data[0], Data[1])


    def readAnalogChannel(self):
        """ reads single ended analog channel"""
        #read config register and overwrite MUX
        configTmp = self.bus.read_i2c_block_data(self._SLAVE_ADDR,self._POINTER_REG_CONFIG)[:2]
        bitmask  = 0x8F
        tmp = (configTmp[0] & bitmask)|(self.CH << 4)
        self.bus.write_i2c_block_data(self._SLAVE_ADDR,self._POINTER_REG_CONFIG,[tmp,configTmp[1]])
        # get conversion value
        tmp = self.bus.read_i2c_block_data(self._SLAVE_ADDR,self._POINTER_REG_CONVERSION)[:2]
        val = ((tmp[0] << 8) + tmp[1]) >> 4

        return val * self.convFactor

if __name__ == "__main__":

    CH3 = ADS1015(1,2)
    count = 0
    values = []
    while True:
        values.append(CH3.readAnalogChannel())
        if count== 19:
            count=0
            average = reduce(lambda x, y: x + y, values) / len(values)
            print("Voltage = ",average)
            values = []
        count+=1

        #print("CH2:  ",CH3.readAnalogChannel())
        time.sleep(0.01)

