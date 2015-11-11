#!/usr/bin/python
##======================================================================================
## FULL STACK EMBEDDED 2016
##=======================================================================================
## File  :       FSEScheduler.py
## Author:       FA
## Board :       Raspberry Pi
## Brief :       Anemometer & Wind direction
##               ToDo:
##                      - Check the real name of wind dir sensor
##                      - Add comments
## Note  :      This file:
##                  - implements an anemoter sensor class
##                  - initialise the GPIO pin used  time measurement
##                  - initialise timeout timer to recognise <No wind> condition
##=======================================================================================

## IMPORTS
from __future__ import print_function
from datetime import datetime, timedelta
import RPi.GPIO as GPIO
import time, sys, signal

##GLOBAL DEFINITION
DEBUG = 0 #DEBUG flag. Set to 1 to see outputs

class SensorError(Exception):
   """Problem occured while communicating with sensor."""
class i2cError(SensorError):
   """Raised when the i2c error occurs"""

class ANEMOMETER:
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
        self.timerTimeout           = 5 # [s]
        # init anemoter
        try:
            GPIO.setmode(GPIO.BCM)
            # Set as input and activate pull-down
            GPIO.setup(self._anemoCh, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
            # Add interrupt event "_rGChannel", count on rising edge and add callback function "_rainGaugeCallback()"
            GPIO.add_event_detect(self._anemoCh, GPIO.RISING, callback = self.AnemometerCallback, bouncetime = 10)

            self.initTimeoutTimer()

            if DEBUG:
                print("Anemometer successfully initialised")
        except Exception as e:
            print(e)
            raise SensorError("Anemometer s initialisation failed...")

    def AnemometerCallback(self,channel):
        """ """
        signal.alarm(0)# desactivate timeout timer
        actualTime = datetime.now()
        t_elapsed = actualTime - self._anemolastCountTime
        t_elapsed_s = (t_elapsed.microseconds + (t_elapsed.seconds +t_elapsed.days * 24.0 * 3600) * 10**6) / 10**6

        #TODO: prevent division against zero
        try:
            self.actualWindSpeed = self.anemoterConvFactor/ t_elapsed_s
        except:
            self.actualWindSpeed =self.actualWindSpeed

        self._anemolastCountTime = actualTime
        signal.alarm(self.timerTimeout)# set timeout timer

        if DEBUG:
            print("wind speed =  ", self.actualWindSpeed, "  [km/h]")

    def initTimeoutTimer(self):
        """ Init timeout time to handle No wind state"""
        # Set the signal handler and a 5-second alarm
        signal.signal(signal.SIGALRM, self.timeoutHandler)
        signal.alarm(0)

    def timeoutHandler(self, signum, frame):
        """  handles timeout events to detect <No wind> condition """
        # set actual wind speed to 0
        self.actualWindSpeed = 0
        print("Speed set to 0 ")

    def getWindSpeed(self):
        """ returns the actual wind speed in [km/h]"""
        return self.actualWindSpeed

    def exit(self):
        """ set of functions to be executed when leaving """
        GPIO.cleanup()
        signal.alarm(0) # Disable the alarm

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


class Anemometer(SensorInterface):
    """ Implement common interface for anemoter """
    def __init__(self):
        self._hw_sensor = ANEMOMETER(17)

    def _get_value(self):
        """Read sensor value."""
        return self._hw_sensor.getWindSpeed()

if __name__== "__main__":
    try:
        AM = Anemometer()
        while True:
            time.sleep(0.1)
            val = AM.get_value()
            print("WindSpeed = ", AM.get_value(),"   [km/h]")
    except (KeyboardInterrupt,SystemExit):
        raise
    except Exception as e:
        print(e)
        GPIO.cleanup()
        sys.exit

