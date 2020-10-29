import unittest

CONNECTION_STRING = "mongodb://192.168.1.48:27017"
BROKER_ADDRESS = "192.168.1.15"

class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, True)

if __name__ == '__main__':
    unittest.main()
