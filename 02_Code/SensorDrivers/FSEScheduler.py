#!/usr/bin/python
##============================================================##
## FULL STACK EMBEDDED 2016                                   ##
##============================================================##
## File  :       FSEScheduler.py                              ##
## Author:       FA                                           ##
## Board :       Raspberry Pi                                 ##
## Brief :       Scheduler                                    ##
## Note  :                                                    ##
##============================================================##

##IMPORTS
from __future__ import print_function
from threading import Thread
import time
from sht21_class import TemperatureSensor, HumiditySensor
from mpl3115a2_class import AirPressureSensor
from ds3231_class import RTC

## GLOBALS
DEBUG = 1
Realtime = RTC()
print("Start time: ", Realtime.get_value())



class Task(Thread):
    def __init__(self,sensorObject,period,outputFile,variable=""):
        Thread.__init__(self)
        self._sensor = sensorObject
        self._sleepTime  = period
        self._logFile    = outputFile
        self._variableName = variable

        self.daemon = True
        self.start()

    def run(self):
        """ """
        while True:
            val = self._sensor.get_value()
            if DEBUG:
                print(Realtime.get_value(), "==> ",self._variableName, " = ", val)
            time.sleep(self._sleepTime)

    def writeLog(self):
        """ 
        #TODO: write Log file
        """
        if DEBUG:
            print(self._logFile,"written")


Task1 = Task(TemperatureSensor(), 3,"/dev/temperature-sensor","Temperatur[C]")
time.sleep(1)
Task2 = Task(HumiditySensor() , 5,"/dev/humidity-sensor","Humidity[%]")
time.sleep(1)
Task3 = Task(AirPressureSensor(), 4, "/dev/AirPressure-sensor","Pressure[Pa]")


while True:
    pass
