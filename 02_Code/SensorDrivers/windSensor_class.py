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
DEBUG = 0 #DEBUG flag. Set to 1 to see outputs

class SensorError(Exception):
   """Problem occured while communicating with sensor."""
class i2cError(SensorError):
   """Raised when the i2c error occurs"""

class WINDSENSOR:
    """Class to read the anemometer and the wind vane """
    #python_version = sys.version_info.major
    anemoterConvFactor = 2.401  # [km/h]
    actualWindSpeed = 0         # [km/h]
    actualWindDirection = 0     # [Degree]

    def __init__(self, AnemometerChannel):
        """ """
        self._anemoCh               = AnemometerChannel
        self._anemoCount            = 0
        self._anemolastCountTime    = datetime.now()

        try:
            GPIO.setmode(GPIO.BCM)
            # Set as input and activate pull-down
            GPIO.setup(self._anemoCh, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
            # Add interrupt event "_rGChannel", count on rising edge and add callback function "_rainGaugeCallback()"
            GPIO.add_event_detect(self._anemoCh, GPIO.RISING, callback = self.AnemometerCallback, bouncetime = 10)
            if DEBUG:
                print("Rain gauge successfully initiallised")
        except Exception as e:
            print(e)
            raise SensorError('Rain gauge initialisation failed...')

    def AnemometerCallback(self,channel):
        """ """
        actualTime = datetime.now()
        t_elapsed = actualTime - self._anemolastCountTime
        t_elapsed_s = (t_elapsed.microseconds + (t_elapsed.seconds +t_elapsed.days * 24.0 * 3600) * 10**6) / 10**6

        #TODO: prevent division against zero
        try:
            self.actualWindSpeed = self.anemoterConvFactor/ t_elapsed_s
        except:
            self.actualWindSpeed =self.actualWindSpeed

        self._anemolastCountTime = actualTime
        if DEBUG:
            print("wind speed =  ", self.actualWindSpeed, "  [km/h]")

    def getWindSpeed(self):
        """ returns the actual wind speed in [km/h]"""
        #TODO.
        # build deltas to get zero state
        return self.actualWindSpeed


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



class WIND_Sensor(SensorInterface):
    """Sensor using SHT21 hardware."""

    def __init__(self):
        super(WIND_Sensor, self).__init__()
        self._hw_sensor = WINDSENSOR(17)

class Anemometer(WIND_Sensor):
    """ Implement common interface for anemoter """
    def _get_value(self):
        """Read sensor value."""
        return self._hw_sensor.getWindSpeed()

if __name__== "__main__":
    try:
        AM = Anemometer()
        valOld = 0
        while True:
            time.sleep(2)
            #detect zero state(no rotation).. these are float numbers so they never can be equal
            #TODO: Get a better methof :)
            val = AM.get_value()

            if val == valOld:

                print ("WindSpeed = ", "0","   [km/h]")
            else:
                print("WindSpeed = ", AM.get_value(),"   [km/h]")
            valOld = val
    except (KeyboardInterrupt,SystemExit):
        raise
    except Exception as e:
        print(e)
        GPIO.cleanup()
        sys.exit

