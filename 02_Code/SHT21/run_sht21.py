#!/usr/bin/python

##==============================================================================##
## FULL STACK EMBEDDED 2016                                                     ##
##==============================================================================##
## File  :       run_sht21.py                                                   ##
## Author:       FA                                                             ##
## Board :       Raspberry Pi                                                   ##
## Brief :       sht21 main()                      ##
## Note  :                                                                      ##
##==============================================================================##

from sht21_class import TemperatureSensor, HumiditySensor
import time

if __name__ == "__main__":
    """
    Prototype sensor polling scheduler.

    To be implemented:
    1. The value read from the sensor ``val`` needs to be saved
    in a file. Also, the file per sensor needs to be determined.

    2. Logic for failed sensor readings
    """
    start = time.time()
    sensor_list = [(TemperatureSensor(), 60, "/dev/temp-sensor"),
                   (HumiditySensor(), 60, "/dev/hum-sensor")]
    while True:
        runtime = int(time.time() - start)
        for sensor, interval, logfile in sensor_list:
            if not runtime % interval:
                val = sensor.get_value()
        time.sleep(0.2)
