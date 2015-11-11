#!/usr/bin/python
##==============================================================================##
## FULL STACK EMBEDDED 2016                                                     ##
##==============================================================================##
## File  :       mpl3115a2.py                                                   ##
## Author:       FA                                                             ##
## Board :       Raspberry Pi                                                   ##
## Brief :       Sensor layer. Functions for sensor access                      ##
## Note  :                                                                      ##
##==============================================================================##

# IMPORTS
from __future__ import print_function
from smbus import SMBus
import time

#GLOBAL DEFINITION
DEBUG = 0

class SensorError(Exception):
    """Problem occured while communicating with sensor."""

class i2cError(SensorError):
    """Raised when the i2c error occurs"""

class MPL3115A2:
    """ Class to read Air pressure """
    # Control constants
    _SLAVE_ADDR     = 0x60
    _CTRL_REG1      = 0x26
    _PT_DATA_CFG    = 0x13
    _WHOAMI_REG     = 0x0C

    # Class variables
    _device_initialised = 0
    def __init__(self,device_number= 1):
        """Opens the i2c device (assuming that the kernel modules have been loaded)"""
        self.bus = SMBus(device_number)
        time.sleep(0.005)
        try:
            whoami = self.bus.read_byte_data(self._SLAVE_ADDR,self._WHOAMI_REG)
        except:
            raise i2cError("i2c error occurs...")

        if whoami == 0xC4:
            if DEBUG:
                print("Successfull Device initialisation")
            self._device_initialised = 1
            self.initBarometer(self)
            self.setActive(self)

        else:
            raise SensorError("Cannot configure the MPL3115A2")

    @staticmethod
    def setActive(self):
		""" Set the device active """
		ctrl_reg1  = self.bus.read_byte_data(self._SLAVE_ADDR,self._CTRL_REG1)
		ctrl_reg1 = ctrl_reg1 | 0x01
		self.bus.write_byte_data(self._SLAVE_ADDR,self._CTRL_REG1,ctrl_reg1)

    @staticmethod
    def setStandby(self):
		""" Set the device in Standby mode """
		self.bus.read_byte_data(self._SLAVE_ADDR,self._CTRL_REG1)
		ctrl_reg1 = ctrl_reg1 & ~0x01
		self.bus.write_byte_data(self._SLAVE_ADDR,self._CTRL_REG1,ctrl_reg1)

    def getAirPressure(self):
        """ Reads the air pressure in Pa """
        if self._device_initialised:
            tmp = self.bus.read_byte_data(self._SLAVE_ADDR,0x01) << 8
            tmp_ = self.bus.read_byte_data(self._SLAVE_ADDR,0x02)
            tmp = tmp + tmp_
            tmp = tmp  << 8
            tmp = tmp + self.bus.read_byte_data(self._SLAVE_ADDR,0x03)

            tmp_m = tmp >> 6
            tmp_l = tmp &  0x30
            pressure = tmp_m + tmp_l/246.0

            if DEBUG:
                print("Air Pressure[Pa] = ",pressure)
            return  pressure


    def getTemperature(self):
        """ Reads the temperature """
        if self._device_initialised:
            tmp = (self.bus.read_byte_data(self._SLAVE_ADDR,0x04)<< 8)
            + self.bus.read_byte_data(self._SLAVE_ADDR,0x05)
            tmp_m =(tmp >> 8) & 0xFF
            tmp_l = tmp & 0xFF
            if tmp_m > 0x7F:
                tmp_m -= 256.0;
            return tmp_m + tmp_l/256.0


    @staticmethod
    def initBarometer(self):
        """ Initialise the Barometer """
        self.bus.write_byte_data(self._SLAVE_ADDR,0x26,0x38)
        self.bus.write_byte_data(self._SLAVE_ADDR,0x27,0x00)
        self.bus.write_byte_data(self._SLAVE_ADDR,0x28,0x11)
        self.bus.write_byte_data(self._SLAVE_ADDR,0x29,0x00)
        self.bus.write_byte_data(self._SLAVE_ADDR,0x2a,0x00)
        self.bus.write_byte_data(self._SLAVE_ADDR,0x13,0x07)
        if DEBUG:
            print("Barometer successfully initialised")

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

class AirPressureSensor(SensorInterface):
    """ Implements common interface for MPL3115A2 (AirPressure/Altimeter)"""
    def __init__(self):
        self._hw_sensor = MPL3115A2()
    def _get_value(self):
        """ Reads sensor value """
        return  self._hw_sensor.getAirPressure()


#TODO: implement the real sensor class
if __name__ == "__main__":
    mpl = MPL3115A2()
    while 1:
        Temperature = mpl.getTemperature()
        Pressure = mpl.getAirPressure()
        print('Temperature[C]=', Temperature, 'Pressure[Pa]=', Pressure)
        print("__________________________________________________")
        time.sleep(1)
