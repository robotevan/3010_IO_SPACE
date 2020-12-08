#Backend unit test
import iospaceAPI_old as api
import unittest
import time

BROKER_ADDRESS = "198.91.181.118"
mqtt_instance = api.MQTT(BROKER_ADDRESS, "test")

class TestClientMQTT(unittest.TestCase):

    def test_mqtt_connect(self):
        mqtt_instance.start_mqtt_thread()
        time.sleep(1)
        self.assertTrue(mqtt_instance.is_connected())
        mqtt_instance.stop_mqtt_thread()

    def test_bad_mqtt_connect(self):
        bad_address = "192.168.1.16"
        client_name = "test2"
        with self.assertRaises(ConnectionRefusedError):
            bad_mqtt_instance = api.MQTT(bad_address, client_name)

    def test_publish(self):
        topic = "testpub"
        self.assertTrue(mqtt_instance.publish(topic, "test", 0))

    def test_subscribe_unsubscribe(self):
        topic = "testsub"
        result = mqtt_instance.subscribe(topic, 0)
        self.assertEqual(result[0],0)
        result = mqtt_instance.unsubscribe(topic)
        self.assertEqual(result[0], 0)

    def test_disconnect(self):
        client_name = "test3"
        disconnect_test_mqtt_instance = api.MQTT(BROKER_ADDRESS, client_name)
        disconnect_test_mqtt_instance.disconnect()

        disconnect_test_mqtt_instance.start_mqtt_thread()
        time.sleep(1)
        self.assertFalse(disconnect_test_mqtt_instance.is_connected())
        disconnect_test_mqtt_instance.stop_mqtt_thread()

if __name__ == "__main__":
    unittest.main()