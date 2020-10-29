import paho.mqtt.client as mqtt
import pymongo
import datetime
import time

def connect_to_database(connection_string: str, database_name: str) -> pymongo.database.Database:
    try:
        client = pymongo.MongoClient(connection_string, serverSelectionTimeoutMS=2000)
        client.server_info()
        return client[database_name]
    except pymongo.errors.ServerSelectionTimeoutError as error:
        print ("Unable to connect to mongodb server ERROR:", error)
        return None

def get_collection(database: pymongo.database.Database, collection_name: str) -> pymongo.collection.Collection:
    return database[collection_name]

def insert_into_collection(collection: pymongo.collection.Collection, data: int) -> bool:
    result = collection.insert_one({
        "node_name": "node1",
        "device_name": "temperature",
        "data": data,
        "date": datetime.datetime.now()
    })
    return result.acknowledged

def connect_to_broker(address: str, message_function):
    try:
        client = mqtt.Client("backend")
        client.on_message = message_function #attach function to callback
        client.connect(BROKER_ADDRESS)
        return client
    except ConnectionRefusedError as error:
        print("Unable to connect to broker ERROR: ", error) 
        return None

def on_message(client, userdata, message):
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic =",message.topic)
    print("message qos =",message.qos)
    print("message retain flag =",message.retain)
    print("Is data inserted into db: ", insert_into_collection(collection, int(message.payload.decode("utf-8"))))
    
def subscribe(client, topic: str):
    client.subscribe(topic)
    
def unsubscribe(client, topic: str):
    client.unsubscribe(topic)    

def publish(client, topic: str, message: str) -> bool:
    result = client.publish(topic, message)
    result.wait_for_publish()
    return result.is_published()

def start_mqtt_thread(client):
    client.loop_start()

def stop_mqtt_thread(client):
    client.loop_stop()

if __name__ == "__main__":
    SEND_TOPIC = "test"
    ECHO_TOPIC = "testecho"
    CONNECTION_STRING = "mongodb://192.168.1.48:27017"
    TEMP_LIST = [23, 24, 25, 26, 27]
    BROKER_ADDRESS ="192.168.1.15"
    
    database = connect_to_database(CONNECTION_STRING, "iospace")
    collection = get_collection(database, "test")
    client = connect_to_broker(BROKER_ADDRESS, on_message)

    subscribe(client, ECHO_TOPIC)

    start_mqtt_thread(client)
    while True:
        for temp in TEMP_LIST:
            print("Is message publsihed: ",publish(client, SEND_TOPIC, temp))
            time.sleep(5)
    stop_mqtt_thread(client)
            

