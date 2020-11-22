from hardware_tests.lidar_tests.Lidar import Lidar
import unittest

lidar_sensor = Lidar()

class TestLidarLiteHardware(unittest.TestCase):
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
        self.assertEqual(device_health, 1)

    def test_read_ready(self):
        device_ready = lidar_sensor.read_device_status()
        self.assertEqual(device_ready, 0)