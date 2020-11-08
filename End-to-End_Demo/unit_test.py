# https://www.eclipse.org/paho/index.php?page=clients/python/docs/index.php#publishing some documentation on results
import unittest
import send_insert as api
import time
import email_tests as email

MQTT_CLIENT_NAME = "test"
CONNECTION_STRING = "mongodb://192.168.1.48:27017"
BROKER_ADDRESS = "192.168.1.15"

mqtt_client = api.connect_to_broker(BROKER_ADDRESS, MQTT_CLIENT_NAME, api.on_message)
iospace_database = api.connect_to_database(CONNECTION_STRING, "iospace")
test_collection = api.get_collection(iospace_database, "test_unit_test")

class TestMqttCommunication(unittest.TestCase):

    def test_mqtt_connect(self):
        api.start_mqtt_thread(mqtt_client)
        time.sleep(1)
        self.assertTrue(mqtt_client.is_connected())
        api.stop_mqtt_thread(mqtt_client)

    def test_bad_mqtt_connect(self):
        bad_address = "192.168.1.16"
        client_name = "test2"
        with self.assertRaises(ConnectionRefusedError):
            api.connect_to_broker(bad_address, client_name, api.on_message, timeout=2)

    def test_publish(self):
        topic = "testpub"
        self.assertTrue(api.publish(mqtt_client, topic, "test", 0))

    def test_subscribe(self):
        topic = "testsub"
        result = api.subscribe(mqtt_client, topic, 0)
        self.assertEqual(result[0],0)

    def test_unsubscribe(self):
        topic = "testsub"
        result = api.unsubscribe(mqtt_client, topic)
        self.assertEqual(result[0], 0)

    def test_disconnect(self):
        client_name = "test3"
        mqtt_client_2 = api.connect_to_broker(BROKER_ADDRESS, client_name, api.on_message)

        api.disconnect(mqtt_client_2)

        api.start_mqtt_thread(mqtt_client_2)
        time.sleep(1)
        self.assertFalse(mqtt_client_2.is_connected())
        api.stop_mqtt_thread(mqtt_client_2)


class TestMongoDB(unittest.TestCase):

    def test_db_connect(self):
        self.assertNotEqual(type(iospace_database), type(api.pymongo.database.Database))

    def test_bad_db_connect(self):
        bad_connection_string = "mongodb://192.168.1.49:27017"
        with self.assertRaises(api.pymongo.errors.ServerSelectionTimeoutError):
            api.connect_to_database(bad_connection_string, "iospace")

    def test_bad_db_name(self):
        bad_db_name = "badname"
        with self.assertRaises(NameError):
            api.connect_to_database(CONNECTION_STRING, bad_db_name)

    def test_get_collection(self):
        self.assertNotEqual(type(test_collection), type(api.pymongo.collection.Collection))

    def test_get_bad_collection_name(self):
        bad_db_name = "badname"
        with self.assertRaises(NameError):
            api.get_collection(iospace_database, bad_db_name)

    def test_insert_data_type(self):
        self.assertTrue(api.insert_into_collection(test_collection, "test_node", "test_case", 1))

    def test_insert_bad_data_type(self):
        bad_data = "int"
        self.assertFalse(api.insert_into_collection(test_collection, "test_node", "test_case", bad_data))

    def test_insert_bad_device_name_type(self):
        bad_device_name = 1
        with self.assertRaises(TypeError):
            api.insert_into_collection(test_collection, "test_node", bad_device_name, 1)

    def test_insert_bad_node_name_type(self):
        bad_node_name = 1
        with self.assertRaises(TypeError):
            api.insert_into_collection(test_collection, bad_node_name, "test_case", 1)

    def test_insert_bad_collection_type(self):
        bad_collection = "collection"
        with self.assertRaises(TypeError):
            api.insert_into_collection(bad_collection, "test_node", "test_case", 1)

class Testemailserves(unittest.TestCase):
    def test_sendemail(self):
        self.assertTrue( email.sendemail("test","ousama_shami@hotmail.com"))







if __name__ == '__main__':
    unittest.main()
    api.disconnect(mqtt_client)
