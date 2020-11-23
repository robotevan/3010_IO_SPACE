from hardware_tests.temp_scoretests.sense import sense
import unittest

sensehat=sense()
class TestSenseHat(unittest.TestCase):
    def test_createsensehat(self):
        self.assertIsNotNone(sensehat)

    def test_readtemp(self):
        self.assertIsNotNone(sensehat.temperature)

    def test_humidity(self):
        self.assertIsNotNone(sensehat.humidity)

    def test_gyroscope(self):
        self.assertIsNotNone(sensehat.get_gyroscope())

    def test_accl(self):
        self.assertIsNotNone(sensehat.get_accelerometer())

    def test_comp(self):
        self.assertIsNotNone(sensehat.compass)

    def test_pres(self):
        self.assertIsNotNone(sensehat.pressure)

    if __name__ =='__main__':
        unittest.main()
