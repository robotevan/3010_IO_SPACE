import unittest
import send_insert as api

CONNECTION_STRING = "mongodb://192.168.1.48:27017"
BROKER_ADDRESS = "192.168.1.15"

d = api.connect_to_database(CONNECTION_STRING, "iospace")

class TestMqttCommunication(unittest.TestCase):

    def setUp(self) -> None:
        self.test = 1

    def test_mqtt_connect(self):
        self.assertEqual(True, True)

    def test_bad_mqtt_connect(self):
        self.assertEqual(1,1)

    def test_publish(self):
        self.assertEqual(1,1)

    def test_subscribe(self):
        self.assertEqual(1,1)

    def test_unsubscribe(self):
        self.assertEqual(1,1)

    def test_disconnect(self):
        self.assertEqual(1,1)

class TestMongoDB(unittest.TestCase):

    def setUp(self) -> None:
        self.test = 1

    def test_db_connect(self):
        self.assertEqual(1,1)

    def test_bad_db_connect(self):
        self.assertEqual(1,1)

    def test_insert_data(self):
        self.assertEqual(1,1)

    def test_insert_bad_data(self):
        self.assertEqual(1,1)

    def test_fetch_data(self):
        self.assertEqual(1,1)

    def test_fetch_bad_data(self):
        self.assertEqual(1,1)

if __name__ == '__main__':
    unittest.main()
