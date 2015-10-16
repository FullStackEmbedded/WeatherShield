#!/usr/bin/python
##==============================================================================##
## FULL STACK EMBEDDED 2016                                                     ##
##==============================================================================##
## File  :       run_sht21.py                                                   ##
## Author:       FA                                                             ##
## Board :       Raspberry Pi                                                   ##
## Brief :       Scheduler                                                      ##
## Note  :                                                                      ##
##==============================================================================##

##IMPORTS
from __future__ import print_function
from sht21_class import TemperatureSensor, HumiditySensor
from mpl3115a2_class import AirPressureSensor
import time

count = 0
if __name__ == "__main__":
    """ Prototype sensor polling scheduler """
    start = time.time()
    sensor_list = [(TemperatureSensor(), 2, "/dev/temperature-sensor"),
                   (HumiditySensor()   , 1, "/dev/humidity-sensor"),
                   (AirPressureSensor(), 5, "/dev/Pressure-sensor")]
    while True:
        runtime = int(time.time() - start)
        for index,(sensor, interval, logfile) in enumerate(sensor_list,1):
            if not runtime % interval:
                val = sensor.get_value()

                if index == 1:
                    print("Temperatur[C] = ", val)
                elif index == 2:
                    print("Humdidity[%] = ", val)
                elif index  == 3:
                    print("AirPressure [Pa] = ", val)
                elif index ==4:
                    print
                else:
                    pass

                #if not count % 3:
                    #print('______________________________________________')
                count = count+1
        #time.sleep(0.2)
