#!/usr/bin/python
##==============================================================================##
## FULL STACK EMBEDDED 2016                                                     ##
##==============================================================================##
## File  :       sht21.py                                                       ##
## Author:       FA                                                             ##
## Board :       Raspberry Pi                                                   ##
## Brief :       Sensor layer. Functions for sensor access                      ##
## Note  :                                                                      ##
#===============================================================================##

## IMPORTS
from __future__ import print_function
from smbus import SMBus
import time

##GLOBAL DEFINITION
DEBUG = 0

class SensorError(Exception):
   """Problem occured while communicating with sensor."""
class i2cError(SensorError):
   """Raised when the i2c error occurs"""

class SHT21:
    """Class to read temperature and humidity from SHT21"""

	## Control constants
    _SOFTRESET                      = 0xFE
    _SLAVE_ADDRESS                  = 0x40
    _TRIGGER_TEMPERATURE_NO_HOLD    = 0xF3
    _TRIGGER_HUMIDITY_NO_HOLD       = 0xF5
    _STATUS_BITS_MASK               = 0xFFFC

	# Wait a bit more than recommended
    _TEMPERATURE_WAIT_TIME          = 0.086  # (datasheet: typ=66, max=85)
    _HUMIDITY_WAIT_TIME             = 0.030  # (datasheet: typ=22, max=29)


    def __init__(self, device_number = 1):
        """Opens the i2c device (assuming that the kernel modules have been
        loaded) & run soft reset. (user register leaved to default value)"""
        self.bus = SMBus(device_number)
        self.bus.write_byte(self._SLAVE_ADDRESS, self._SOFTRESET)
        time.sleep(0.015)
        if DEBUG:
            print("SHT21 init done.")

    def getTemperature(self):
        """Reads the temperature from the sensor.  Not that this call blocks
        for ~86ms to allow the sensor to return the data """
        self.bus.write_byte(self._SLAVE_ADDRESS, self._TRIGGER_TEMPERATURE_NO_HOLD)
        data = []
        time.sleep(self._TEMPERATURE_WAIT_TIME)

        data.append(self.bus.read_byte(self._SLAVE_ADDRESS))
        data.append(self.bus.read_byte(self._SLAVE_ADDRESS))

        Temperature = self._get_temperature_from_buffer(data)
        if DEBUG:
            print("Temp[C] = ", Temperature)
        return Temperature

    def getHumidity(self):
        """Reads the humidity from the sensor.  Not that this call blocks
        for ~30ms to allow the sensor to return the data"""
        self.bus.write_byte(self._SLAVE_ADDRESS, self._TRIGGER_HUMIDITY_NO_HOLD)
        data = []
        time.sleep(self._HUMIDITY_WAIT_TIME)

        data.append(self.bus.read_byte(self._SLAVE_ADDRESS))
        data.append(self.bus.read_byte(self._SLAVE_ADDRESS))

        Humidity = self._get_humidity_from_buffer(data)
        if DEBUG:
            print("Humidity[%] = ", Humidity)

        return Humidity

    @staticmethod
    def _get_temperature_from_buffer(data):
        """This function reads the first two bytes of data and
            returns the temperature in C by using the following function:
            T = =46.82 + (172.72 * (ST/2^16))where ST is the value from the sensor  """
        unadjusted = ((data[0]) << 8) + (data[1])
        unadjusted &= SHT21._STATUS_BITS_MASK  # zero the status bits
        unadjusted *= 175.72
        unadjusted /= 1 << 16  # divide by 2^16
        unadjusted -= 46.85
        return unadjusted


    @staticmethod
    def _get_humidity_from_buffer(data):
        """This function reads the first two bytes of data and returns
            the relative humidity in percent by using the following function:
            RH = -6 + (125 * (SRH / 2 ^16)) where SRH is the value read from the sensor """
        unadjusted = (data[0] << 8) + data[1]
        unadjusted &= SHT21._STATUS_BITS_MASK  # zero the status bits
        unadjusted *= 125.0
        unadjusted /= 1 << 16  # divide by 2^16
        unadjusted -= 6
        return unadjusted


    @staticmethod
    def _calculate_checksum(data, number_of_bytes):
        """5.7 CRC Checksum using the polynomial given in the datasheet"""
        # CRC
        POLYNOMIAL = 0x131  # //P(x)=x^8+x^5+x^4+1 = 100110001
        crc = 0
        # calculates 8-Bit checksum with given polynomial
        for byteCtr in range(number_of_bytes):
            crc ^= (data[byteCtr])
            for bit in range(8, 0, -1):
                if crc & 0x80:
                    crc = (crc << 1) ^ POLYNOMIAL
                else:
                    crc = (crc << 1)
        return crc


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


class SHT21_Sensor(SensorInterface):
    """Sensor using SHT21 hardware."""

    def __init__(self):
        super(SHT21_Sensor, self).__init__()
        self._hw_sensor = SHT21()

class TemperatureSensor(SHT21_Sensor):
    """Implements common interface for temperatur sensor"""

    def _get_value(self):
        """Read sensor value."""
        return self._hw_sensor.getTemperature()

class HumiditySensor(SHT21_Sensor):
    """Implements common interface for humidity sensor"""

    def _get_value(self):
        """Read sensor value."""
        return self._hw_sensor.getHumidity()



if __name__ == "__main__":
    tmpSens = TemperatureSensor()
    humiditySens = HumiditySensor()
    while 1:
        print("Temperature[C] = ",tmpSens.get_value(),"   ","AirHumidity[%] =",
                humiditySens.get_value())
        print("_________________________________________________________________")
        time.sleep(1)
