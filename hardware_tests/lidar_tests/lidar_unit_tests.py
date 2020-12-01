
import unittest

from smbus2 import *

DEFAULT_ADDRESS = 0x62 # Address of the device
#Internal registers
ACQ_COMMAND = 0x00 # W: 0x00 Reset all registers to default
                   # W: 0x03 Measure distance (no correction)
                   # W: 0x04 Measure distance (Bias correction)
ACQ_CONFIG_REG = 0x04 # R/W: Configuration of the device
STATUS = 0x01 # R: Status register of the device
DISTANCE_OUTPUT = 0x8f # R: Distance measurement in cm (2 Bytes)
VELOCITY_OUTPUT = 0x09 # R: Velocity measurement in cm/s (1 Byte, 2's complement)
POWER_CONTROL = 0x65 # R/W: Configure power mode of the device
SIG_COUNT_VAL = 0x02 # R/W: Max times a pulse can be sent


"""
Interface for the Garmin Lidar-Lite v3
"""
class Lidar:
    """
    @:param SMBus, a bus for the device to use
    """
    def __init__(self, bus=None):
        if bus is None:
            self.bus = SMBus(1)
        else:
            self.bus = bus
        self.is_on = False # Represents the on/off state of the receiver circuit

    """ 
    Take one measurement in cm, if the receiver circuit is disabled, it will enable the circuit before 
    taking a distance measurement
    If taking many measurements, it is recommended to take a bias corrected measurement every 100 readings
    @:param: bias_correction boolean, determines if measurement uses bias correction or not
    @:return int distance in cm
    """
    def read_distance(self, bias_correction=True):
        if not self.is_on:
            self.power_on()
        if bias_correction:
            # Write 0x04 to 0x00 for bias corrected measurement
            self.bus.write_byte_data(DEFAULT_ADDRESS, ACQ_COMMAND,0x04)
        else:
            # Write 0x03 to 0x00 for no bias correction
            self.bus.write_byte_data(DEFAULT_ADDRESS, ACQ_COMMAND, 0x03)
        # Wait for device to receive distance reading
        self._wait_for_ready_()
        # Read HIGH and LOW distance registers
        distance = self.bus.read_i2c_block_data(DEFAULT_ADDRESS, DISTANCE_OUTPUT, 2)
        return distance[0] << 8 | distance[1] # combine both bytes

    """
    Read the velocity of an object, if the receiver circuit is disabled, it will be 
    enabled before taking a velocity measurement
    @:return int velocity in cm/s
        positive = away from lidar
        negative = towards lidar
    """
    def read_velocity(self):
        if not self.is_on:
            self.power_on()
        # Take two distance measurements to store in registers
        self.read_distance()
        self.read_distance()
        # Read the velocity register (8 bits, 2's complement)
        velocity = self.bus.read_byte_data(DEFAULT_ADDRESS, VELOCITY_OUTPUT)
        if velocity > 127:
            velocity = (256 - velocity)*(-1)
        return velocity

    """
    Read the current configuration of the device
    @:return list of ints, 7 bits
        bit 6: 0 = Enable reference process
               1 = Disable reference process
        bit 5: 0 = Use default delay for burst
               1 = Use custom delay from 0x45, HZ
        bit 4: 0 = Enable reference filter
               1 = Disable reference filter
        bit 3: 0 = Enable measurement quick termination
               1 = Disable measurement quick termination
        bit 2: 0 = Use default reference acquisition
               1 = Use custom  reference acquisition from 0x12
        bits 1-0: 00 = Default PWM mode
                  01 = Status output mode
                  10 = Fixed delay PWM mode
                  11 = Oscillator output mode (nominal 31.25kHz output)
        default config = 0x08 (0001000)
    """
    def read_device_config(self):
        config = int(self.bus.read_byte_data(DEFAULT_ADDRESS, ACQ_CONFIG_REG))
        config = bin(config)[2:].zfill(7)
        return [int(bit) for bit in str(config)]

    """
    Set the device config
    @:param list of ints, provide all 7 bits for config register
        bit 6: 0 = Enable reference process
               1 = Disable reference process
        bit 5: 0 = Use default delay for burst
               1 = Use custom delay from 0x45, HZ
        bit 4: 0 = Enable reference filter
               1 = Disable reference filter
        bit 3: 0 = Enable measurement quick termination
               1 = Disable measurement quick termination
        bit 2: 0 = Use default reference acquisition
               1 = Use custom  reference acquisition from 0x12
        bits 1-0: 00 = Default PWM mode
                  01 = Status output mode
                  10 = Fixed delay PWM mode
                  11 = Oscillator output mode (nominal 31.25kHz output)
        default config = 0x08 (0001000)
    """
    def write_device_config(self, bits):
        bits = [str(bit) for bit in bits]
        bits = int("".join(bits),2) # Convert to dec for i2c reg
        self.bus.write_byte_data(DEFAULT_ADDRESS, ACQ_CONFIG_REG, bits)

    """
    Read the current status of the device
    :return: list of ints
        bit 6: Process error flag
        bit 5: Health flag
        bit 4: Secondary return flag
        bit 3: Invalid signal flag
        bit 2: Signal overflow flag
        bit 1: Reference overflow flag
        bit 0: Busy flag
    """
    def read_device_status(self):
        # Read the STATUS register, bits 0-6 only
        status = int(self.bus.read_byte_data(DEFAULT_ADDRESS, STATUS))
        # Convert to binary, fill rest with 0's
        status = bin(status)[2:].zfill(7)
        return [int(bit) for bit in str(status)]

    """
    Check if the device is busy
    @:return boolean, true = busy
    """
    def device_busy(self):
        # STATUS register bit 0 represents busy flag, 0 for ready, 1 for busy
        return self.read_device_config()[-1]

    """
    Wait for the device to be ready
    """
    def _wait_for_ready_(self):
        while self.device_busy(): pass

    """
    Set the maximum number of measurements the device can take before taking a reading
    note: the device will not always take this amount, only if required
          ex: surface is not very reflective, long distance
    The lower the number, the faster the measurement, values can range from 30 to 255
    @:param count max number of pulses (default 128) 
    """
    def maximum_acquisition_count(self, count):
        if 30 < count < 255:
            raise Exception("Value must be between 30 and 255")
        self.bus.write_byte_data(DEFAULT_ADDRESS, SIG_COUNT_VAL, count)
        print(self.bus.read_byte_data(DEFAULT_ADDRESS,SIG_COUNT_VAL))

    """
    Turn the device receiver circuit on or off, This will save roughly 40mA
    Turning the receiver back on takes roughly the same amount of time as 
    receiving a measurement
    @:param on boolean, represents the action
    """
    def power_on(self, on=True):
        if on:
            # Enable the receiver circuit
            self.is_on = True
            self.bus.write_byte_data(DEFAULT_ADDRESS, POWER_CONTROL, 0x80)
        else:
            # Disable the receiver circuit off
            self.is_on = False
            self.bus.write_byte_data(DEFAULT_ADDRESS, POWER_CONTROL, 0x81)


lidar_sensor = Lidar()


class LidarLiteHardware(unittest.TestCase):
    def test_create_lidar_instance(self):
        self.assertIsNotNone(lidar_sensor.bus)

    def test_lidar_read_distance(self):
        distance = lidar_sensor.read_distance()
        self.assertIsNot(distance, 0)

    def test_lidar_read_velocity(self):
        velocity = lidar_sensor.read_velocity()
        self.assertGreater(velocity, 0)

    def test_power_off(self):
        lidar_sensor.power_on(False)
        self.assertFalse(lidar_sensor.is_on)

    def test_power_on(self):
        lidar_sensor.power_on(True)
        self.assertTrue(lidar_sensor.is_on)

    def test_read_device_config(self):
        device_config_vals = lidar_sensor.read_device_config()
        self.assertIsNotNone(device_config_vals)

    def test_read_device_status(self):
        device_status = lidar_sensor.read_device_status()
        self.assertIsNotNone(device_status)

    def test_device_health(self):
        device_health = lidar_sensor.read_device_config()[5]
        self.assertEqual(device_health, 0)

    def test_read_ready(self):
        device_ready = lidar_sensor.read_device_status()
        self.assertEqual(device_ready, 0)

if __name__ == "__main__":
    unittest.main()