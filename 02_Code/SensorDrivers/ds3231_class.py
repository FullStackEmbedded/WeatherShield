#!/usr/bin/python
##==============================================================================##
## FULL STACK EMBEDDED 2016                                                     ##
##==============================================================================##
## File  :       ds3231_class.py                                                ##
## Author:       FA                                                             ##
## Board :       Raspberry Pi                                                   ##
## Brief :       Sensor layer. Functions for sensor access                      ##
## Note  :                                                                      ##
#===============================================================================##

## IMPORTS
from __future__ import print_function
from datetime import datetime
from smbus import SMBus
import time, requests

##GLOBAL DEFINITION
DEBUG = 0

class SensorError(Exception):
   """Problem occured while communicating with sensor."""
class i2cError(SensorError):
   """Raised when the i2c error occurs"""
class ConnectionError(SensorError):
    """ Raise when the Pi is not connected to the internet"""
class DS3231:
    """Class to read/write time from/to DS3231"""

	## Control constants
    _SLAVE_ADDR         = 0x68
    _TIME_START_ADDR    = 0x00
    _TEMP_START_ADDR    = 0x11

    _REG_SECONDS        = 0x00
    _REG_MINUTES        = 0x01
    _REG_HOURS          = 0x02
    _REG_DAY            = 0x03
    _REG_DATE           = 0x04
    _REG_MONTH          = 0x05
    _REG_YEAR           = 0x06
    _REG_CONTROL        = 0x07


    def __init__(self, device_number = 1):
        """Opens the i2c device (assuming that the kernel modules have been
        loaded) & run soft reset. (user register leaved to default value)"""
        try:
            self.bus = SMBus(device_number)
        except i2cError:
            #raise i2cError
            pass

        if DEBUG:
            print("DS3231 init done.")

    def getTime(self):
        """ """
        try:
            data = self.bus.read_i2c_block_data(self._SLAVE_ADDR,0x00,7)
        except i2cError:
			#raise i2cError
            pass
        sec     = self._bcd_to_int(data[0] & 0x7F)
        min     = self._bcd_to_int(data[1] & 0x3F)
        hour    = self._bcd_to_int(data[2])
        day     = self._bcd_to_int(data[3])
        date    = self._bcd_to_int(data[4])
        month   = self._bcd_to_int(data[5])
        year    = self._bcd_to_int(data[6])
        if DEBUG:
            print(datetime((21-1)*100 + year, month,date,hour,min,sec,0,tzinfo
                = None))
            #print(*data, sep='\t')
        return datetime((21-1)*100 + year, \
                month,date,hour,min,sec,0,tzinfo=None)
    def setTime(self,timetuple):
        """
			write Time/date Information to Ds3231
			Range: seconds [0,59], minutes [0,59], hours [0,23],
					day [0,7], date [1-31], month [1-12], year [0-99].
        """
        if  self.checkTimeDataValidity(timetuple)is True:
            #write seconds
            regSec  = self._int_to_bcd(timetuple[5])
            self.bus.write_byte_data(self._SLAVE_ADDR,self._REG_SECONDS,regSec)
            #write minutes
            regMin  = self._int_to_bcd(timetuple[4])
            self.bus.write_byte_data(self._SLAVE_ADDR,self._REG_MINUTES,regMin)
            #write hours
            regHr = self._int_to_bcd(timetuple[3])
            self.bus.write_byte_data(self._SLAVE_ADDR,self._REG_HOURS,regHr)
            #write Date
            regDate = self._int_to_bcd(timetuple[2])
            self.bus.write_byte_data(self._SLAVE_ADDR,self._REG_DATE,regDate)
            #write month
            regMonth = self._int_to_bcd(timetuple[1])
            self.bus.write_byte_data(self._SLAVE_ADDR,self._REG_MONTH,regMonth)
            #write year
            regYr = self._int_to_bcd(timetuple[0]-2000)
            self.bus.write_byte_data(self._SLAVE_ADDR,self._REG_YEAR,regYr)

    def setTimeNow(self):
        """
            Set time to datetime.now(). Return tuple needed by setTime()
        """
        #TODO:  Get a better function to check  if the pi is online
        if self.checkIfOnline() is not None:
            tmp = datetime.now()
            self.setTime((tmp.year,tmp.month, tmp.day,tmp.hour,tmp.minute,tmp.second ))
        else:
            raise ConnectionError("Please connect your Pi to the internet first...")

    @staticmethod
    def checkIfOnline():
        """ Check if the pi is online """
        try:
            import requests
        except ImportError:
            print('Please make sure Python library requests is installed')
        r = requests.get('https://api.github.com/events')
        if r is True:
            return True
        else:
            return False
    @staticmethod
    def checkTimeDataValidity(timetuple):
        """
            Checks time data inputs
        """
        if 2000 <= timetuple[0] <= 2099 and  \
           1 <= timetuple[1] <= 12 and  \
           1 <= timetuple[2] <= 31 and \
           0 <= timetuple[3] <= 23 and  \
           0 <= timetuple[4] <= 59 and  \
           0 <= timetuple[5] <= 59:
            return True
        else:
            return False


    @staticmethod
    def _bcd_to_int(bcd):
        """
            Decode a 2x4bit BCD to a integer.
        """
        out = 0
        for d in (bcd >> 4, bcd):
            for p in (1, 2, 4 ,8):
                if d & 1:
                    out += p
                d >>= 1
            out *= 10
        return int(out / 10)

    @staticmethod
    def _int_to_bcd(n):
        """
            Encode a one or two digits number to the BCD.
        """
        bcd = 0
        for i in (n // 10, n % 10):
            for p in (8, 4, 2, 1):
                if i >= p:
                    bcd += 1
                    i -= p
                bcd <<= 1
        return bcd >> 1



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

class RTC(SensorInterface):
    """ Implements common interface for MPL3115A2 (AirPressure/Altimeter)"""
    def __init__(self):
        self._hw_sensor = DS3231()
    def _get_value(self): 
        """ Reads sensor value """
        return  self._hw_sensor.getTime()  

if __name__ == "__main__":
    rtc = RTC()
    #rtc.setTimeNow()
    while True:

        print(rtc.get_value())
        time.sleep(2)


