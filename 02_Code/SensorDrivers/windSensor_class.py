#!/usr/bin/python
##===============================================================##
## FULL STACK EMBEDDED 2016                                      ##
##===============================================================##
## File  :       FSEScheduler.py                                 ##
## Author:       FA                                              ##
## Board :       Raspberry Pi                                    ##
## Brief :       Anemometer & Wind direction                     ##
##               ToDo:                                           ##
##                      - Check the real name of wind dir sensor ##
##                      - Add comments                           ##
## Note  :                                                       ##
##===============================================================##

## IMPORTS
from __future__ import print_function
from smbus import SMBus
from datetime import datetime, timedelta
import RPi.GPIO as GPIO
import time, sys

##GLOBAL DEFINITION
DEBUG = 1 #DEBUG flag. Set to 1 to see outputs

class SensorError(Exception):
   """Problem occured while communicating with sensor."""
class i2cError(SensorError):
   """Raised when the i2c error occurs"""

class WINDSENSOR:
    """Class to read the anemometer and the wind vane """
    python_version = sys.version_info.major

    def __init__(self, AnemometerChannel):
        """ """
        self._anemoCh       = AnemometerChannel
        self._anemoCount    = 0
        self._anemolastCountTimeDelta = datetime.now()
        self._actualVelocity_kmph = 0

        try:
            GPIO.setmode(GPIO.BCM)
            # Set as input and activate pull-down
            GPIO.setup(self._anemoCh, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
            # Add interrupt event, count on rising edge and add callback function
            GPIO.add_event_detect(self._anemoCh, GPIO.RISING, callback = self.AnemometerCallback, bouncetime = 10)
            if DEBUG:
                print("Rain gauge successfully initiallised")
        except Exception as e:
            print(e)
            raise SensorError('Rain gauge initialisation failed...')

    def AnemometerCallback(self, channel):
        """ """
        tmp = datetime.now()
        t_elapsed_s = (tmp - self._anemolastCountTimeDelta).total_seconds()
        self._actualVelocity_kmph =  2.401 / t_elapsed_s
        self._anemoCount += 1
        if DEBUG:
            print(self._anemoCount)
            print("wind speed[km/h] = ", self._actualVelocity_kmph)

        self._anemolastCountTimeDelta = tmp

    def getWindDirection(self):
        """"""
        pass

    def getWindSpeed(self):
        """ return wind speed in km/h """
        return self._actualVelocity_kmph

class SensorInterface(object):
    """ Abstract common interface for hardware sensors."""
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

class WIND_Sensor(SensorInterface):
    """ Wind Sensors: Anemometer & wind vane"""
    def __init__(self):
        super(WIND_Sensor, self).__init__()
        self._hw_sensor = WINDSENSOR(17)

class AnemometerSensor(WIND_Sensor):
    """ Implements common interface for anemometer"""
    def _get_value(self):
        """ Reads sensor value """
        return  self._hw_sensor.getWindSpeed()

class WindVane(WIND_Sensor):
    """ Implements common interface for wind vane"""
    def _get_value(self):
        """ Reads sensor value """
        return  self._hw_sensor.getWindDirection()




if __name__ == "__main__":
    try:
       anemo = AnemometerSensor()
       while True:
           time.sleep(2)
           print(anemo.get_value())
    except (KeyboardInterrupt, SystemExit):
        raise
    except Exception as e:
        print(e)
        GPIO.cleanup()
        sys.exit


