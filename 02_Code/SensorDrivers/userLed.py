#!/bin/python
##==============================================================================##
## FULL STACK EMBEDDED 2016                                                     ##
##==============================================================================##
## File  :       userLed.py                                                     ##
## Author:       FA                                                             ##
## Board :       Raspberry Pi                                                   ##
## Brief :       Functions for on board led  access                             ##
## Note  :                                                                      ##
##==============================================================================##

## IMPORTS
from __future__ import print_function
import time
import RPi.GPIO as GPIO


class userLed:
    def __init__(self, period=1):
        self._period = period
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(21, GPIO.OUT)

    def run(self):
        while True:
            GPIO.output(21, not GPIO.input(21))
            time.sleep(self._period)

    def __exit__(self):
        GPIO.cleanup(21)
        print ("Cleaning up ...")

if __name__ == "__main__":
    userLed(1).run()

