import paho.mqtt.client as mqtt
import pymongo
import datetime
import time

def connect_to_database(connection_string: str, database_name: str) -> pymongo.database.Database:
    try:
        mongo = pymongo.MongoClient(connection_string, serverSelectionTimeoutMS=2000)
        mongo.server_info()
        return mongo[database_name]
    except pymongo.errors.ServerSelectionTimeoutError as error:
        print ("Unable to connect to mongodb server ERROR:", error)
        return None

def get_collection(select_database: pymongo.database.Database, collection_name: str) -> pymongo.collection.Collection:
    return select_database[collection_name]

def insert_into_collection(select_collection: pymongo.collection.Collection, data: int) -> bool:
    result = select_collection.insert_one({
        "node_name": "node1",
        "device_name": "temperature",
        "data": data,
        "date": datetime.datetime.now()
    })
    return result.acknowledged

def connect_to_broker(address: str, message_function) -> mqtt.Client:
    try:
        client = mqtt.Client("backend")
        client.on_message = message_function #attach function to callback
        client.connect(address)
        return client
    except ConnectionRefusedError as error:
        print("Unable to connect to broker ERROR: ", error)
        return None

#Called when a message from subscribed topics is received from broker on client
def on_message(client, userdata, message):
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic =",message.topic)
    print("message qos =",message.qos)
    print("message retain flag =",message.retain)
    print("Is data inserted into db: ", insert_into_collection(collection, int(message.payload.decode("utf-8"))))

def subscribe(mqtt_client: mqtt.Client, topic: str) -> tuple:
    return mqtt_client.subscribe(topic)

def unsubscribe(mqtt_client: mqtt.Client, topic: str) -> tuple:
    return mqtt_client.unsubscribe(topic)

def publish(mqtt_client: mqtt.Client, topic: str, message: str) -> bool:
    result = mqtt_client.publish(topic, message)
    result.wait_for_publish()
    return result.is_published()

def start_mqtt_thread(mqtt_client: mqtt.Client):
    mqtt_client.loop_start()

def stop_mqtt_thread(mqtt_client: mqtt.Client):
    mqtt_client.loop_stop()

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
            

