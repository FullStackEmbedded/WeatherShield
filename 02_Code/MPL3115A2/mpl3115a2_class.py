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
from smbus import SMBus
import time

#GLOBAL DEFINITION
DEBUG = 1


#SENSOR CLASS DEFINITION
class MPL3115A2:
    # Control constants
    _SLAVE_ADDR 	= 0x60
    _CTRL_REG1 		= 0x26
    _PT_DATA_CFG 	= 0x13
	_WHOAMI_REG 	= 0x0C

    def __init__(self,device_number= 1):
        """Opens the i2c device (assuming that the kernel modules have been loaded)"""
        try:
			bus = SMBus(device_number)
			time.sleep(0.005)
			whoami = hex(bus.read_byte_data(_SLAVE_ADDR,_WHOAMI_REG))
			if whoami == 0xC4:
				print("Correct whoami")
			else:
				raise(i2cError)
				
		except i2cError:
			print("I2C error occurs. Cannot open devive")
			exit(1)
		
	def getAirPressure(self):
	"""" Gets the air pressure in PA """"
		if DEBUG:
			print("The air pressure is 10kPa ")

		
class Error(Exception):
   """Base class for other exceptions"""
   pass
class i2cError(Error):
   """Raised when the i2c error occurs"""
   pass
   
MPL3115A2(1)