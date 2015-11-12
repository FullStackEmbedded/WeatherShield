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

from __future__ import print_function


import csv
import os
import shutil
import time
from datetime import datetime
from tempfile import NamedTemporaryFile as tmp
from threading import Thread


from sht21_class import TemperatureSensor, HumiditySensor
from mpl3115a2_class import AirPressureSensor
from ds3231_class import RTC


CLOCK = RTC()

class Task(Thread):

    """Safely record observations from sensors."""

    def __init__(self, sensor, period, output_file):
        """Initialize thread, pass on arguments intended for superclass."""
        Thread.__init__(self)
        self.sensor = sensor
        self.period = period
        self.output_file = output_file
        self.daemon = True
        self.start()

    def run(self):
        """Safely remove stale observations and append to target file."""
        if not os.path.exists(self.output_file):
            open(self.output_file, "w").close()
        while True:
            with open(self.output_file) as old, tmp(delete=False) as new:
                reader = csv.reader(old)
                writer = csv.writer(new)
                for line in reader:
                    ts = datetime.strptime(line[0], "%Y-%m-%d %H:%M:%S")
                    now = datetime.now()
                    diff = now - ts
                    if diff.seconds < 60 * 60 * 2:
                        writer.writerow(line)
                try:
                    current_time = CLOCK.get_value()
                    observation = self.sensor.get_value()
                    writer.writerow((current_time, observation))
                except IOError: pass
            os.chmod(new.name, 0644)
            shutil.move(new.name, self.output_file)
            time.sleep(self.period)


if __name__ == "__main__":
    """Dispatch sensor tasks, then stay alive."""
    print("Start time: ", CLOCK.get_value())
    task_sets = ((TemperatureSensor, 1, "/dev/sensor-temp"),
                 (HumiditySensor, 1, "/dev/sensor-humi"),
                 (AirPressureSensor, 1, "/dev/sensor-pres"))
    for sensor, interval, target, in task_sets:
        Task(sensor(), interval, target)
        time.sleep(1)
    while True:
        time.sleep(float('inf'))

