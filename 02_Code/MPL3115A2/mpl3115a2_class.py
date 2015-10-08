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

class MPL3115A2:
    """ Class to read Air pressure """
    # Control constants
    _SLAVE_ADDR     = 0x60
    _CTRL_REG1      = 0x26
    _PT_DATA_CFG    = 0x13
    _WHOAMI_REG     = 0x0C

    # Class variables
    _device_initialized = 0
    def __init__(self,device_number= 1):
        """Opens the i2c device (assuming that the kernel modules have been loaded)"""
        try:
		self.bus = SMBus(device_number)
		time.sleep(0.005)
		whoami = self.bus.read_byte_data(self._SLAVE_ADDR,self._WHOAMI_REG)
		if whoami == 0xC4:
			self._device_initialized = 1
			self.initBarometer()
            #self.setActive()
            if DEBUG:
				print("Successfull Device initialisation")

		else:
			print("...")
			raise(i2cError)
        except i2cError:
			print("I2C error occurs. Cannot open devive")
			exit(1)


	def setActive(self):
		""" Set the device active """
		ctrl_reg1  = self.bus.read_byte_data(self._SLAVE_ADDR,self._CTRL_REG1)
		ctrl_reg1 = ctrl_reg1 | 0x01
		self.bus.write_byte_data(self._SLAVE_ADDR,self._CTRL_REG1,ctrl_reg1)

	def setStandby(self):
		""" Set the device in Standby mode """
		self.bus.read_byte_data(self._SLAVE_ADDR,self._CTRL_REG1)
		ctrl_reg1 = ctrl_reg1 & ~0x01
		self.bus.write_byte_data(self._SLAVE_ADDR,self._CTRL_REG1,ctrl_reg1)

    def getAirPressure(self):
        """ Reads the air pressure in  Pa """
    @staticmethod
    def initBarometer(self):
        """ Initialise the Barometer """
        self.bus.write_byte_data(self._SLAVE_ADDR,self._CTRL_REG1,0x38)
        self.bus.write_byte_data(self._SLAVE_ADDR,self._CTRL_REG1,0x00)
        self.bus.write_byte_data(self._SLAVE_ADDR,self._CTRL_REG1,0x11)
        self.bus.write_byte_data(self._SLAVE_ADDR,self._CTRL_REG1,0x00)
        self.bus.write_byte_data(self._SLAVE_ADDR,self._CTRL_REG1,0x00)
        self.bus.write_byte_data(self._SLAVE_ADDR,self._CTRL_REG1,0x07)


class Error(Exception):
   """Base class for other exceptions"""
   pass
class i2cError(Error):
   """Raised when the i2c error occurs"""
   pass


