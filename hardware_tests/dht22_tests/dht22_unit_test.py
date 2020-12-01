#DHT22 Unit Test
import unittest
import adafruit_dht
import time

DHT_PIN = 17

class TestDHT22Sensor(unittest.TestCase):

    def test_temperature_measurement(self):
        DHT_SENSOR = adafruit_dht.DHT22(DHT_PIN)
        time.sleep(1)
        temperature = DHT_SENSOR.temperature
        self.assertEqual(type(temperature), float)
        DHT_SENSOR.exit()

    def test_humdity_measurement(self):
        DHT_SENSOR = adafruit_dht.DHT22(DHT_PIN)
        time.sleep(1)
        humidity = DHT_SENSOR.humidity
        self.assertEqual(type(humidity), float)
        DHT_SENSOR.exit()

    def test_exit_sensor(self):
        DHT_SENSOR = adafruit_dht.DHT22(DHT_PIN)
        time.sleep(1)
        DHT_SENSOR.exit()
        with self.assertRaises(OSError):
            DHT_SENSOR.measure()

    def test_multiple_measurements(self):
        DHT_SENSOR = adafruit_dht.DHT22(DHT_PIN)
        time.sleep(1)
        for i in range(20):
            temperature = DHT_SENSOR.temperature
            humidity = DHT_SENSOR.humidity
            self.assertEqual(type(temperature), float)
            self.assertEqual(type(humidity), float)
        DHT_SENSOR.exit()

    def test_bad_pin(self):
        DHT_BAD_PIN = 18
        DHT_SENSOR = adafruit_dht.DHT22(DHT_BAD_PIN)
        time.sleep(1)
        with self.assertRaises(RuntimeError):
            DHT_SENSOR.measure()
        DHT_SENSOR.exit()

if __name__ == '__main__':
    unittest.main()
