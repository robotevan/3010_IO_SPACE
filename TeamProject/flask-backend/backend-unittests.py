import unittest
import pymongo

client = pymongo.MongoClient("mongodb://192.168.1.48:27017")
db = client['iospace']


class FlaskTests(unittest.TestCase):
    def test_create_mongo_connection(self):
        self.assertIsNotNone(client)

    def test_retrieve_db(self):
        self.assertIsNotNone(db)

    def test_retrieve_user_data(self):
        user_data_collection = db['user_data']
        doc = user_data_collection.find_one({'api_key': "test"})
        self.assertIsNotNone(doc)

    def test_get_nodes(self):
        user_data_collection = db['user_data']
        doc = user_data_collection.find_one({'api_key': "test"})
        nodes = doc['nodes']
        self.assertIsNotNone(nodes)

    def test_get_devices(self):
        user_data_collection = db['user_data']
        doc = user_data_collection.find_one({'api_key': "test"})
        devices = doc['devices']
        self.assertIsNotNone(devices)