import paho.mqtt.client as mqtt
import pymongo
import datetime
import time

def connect_to_database(connection_string: str, database_name: str) -> pymongo.database.Database:
    mongo = pymongo.MongoClient(connection_string, serverSelectionTimeoutMS=2000)
    db_names = mongo.list_database_names()
    if database_name in db_names:
        return mongo[database_name]
    else:
        raise NameError("database_name doesn't exist on server")

def get_collection(select_database: pymongo.database.Database, collection_name: str) -> pymongo.collection.Collection:
    collection_names = select_database.list_collection_names()
    if collection_name in collection_names:
        return select_database[collection_name]
    else:
        raise NameError("collection_name doesn't exist on selected database")

def insert_into_collection(select_collection: pymongo.collection.Collection, node_name: str, device_name: str, data: str) -> bool:

    if type(select_collection) != pymongo.collection.Collection:
        raise TypeError("select_collection MUST be of type pymongo.collection.Collection")
    elif type(node_name) != str:
        raise TypeError("node_name MUST be a string")
    elif type(device_name) != str:
        raise TypeError("device_name MUST be a string")

    try:
        data = float(data)
    except:
        print("data string cannot be converted into a float!")
        return False

    result = select_collection.insert_one({
        "node_name": node_name,
        "device_name": device_name,
        "data": data,
        "date": datetime.datetime.now()
    })
    return result.acknowledged

def connect_to_broker(address: str, client_name: str, message_function, timeout=30) -> mqtt.Client:
    mqtt_client = mqtt.Client(client_name)
    mqtt_client.CONNECTION_TIMEOUT_DEFAULT = timeout
    mqtt_client.on_message = message_function #attach function to callback
    mqtt_client.connect(address)
    return mqtt_client

#Called when a message from subscribed topics is received from broker on client
def on_message(client, userdata, message):
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic =",message.topic)
    print("message qos =",message.qos)
    print("message retain flag =",message.retain)
    print("Is data inserted into db: ",insert_into_collection(collection, "node_test", "temperature", message.payload.decode("utf-8")))

def subscribe(mqtt_client: mqtt.Client, topic: str, qos:int) -> tuple:
    return mqtt_client.subscribe(topic, qos)

def unsubscribe(mqtt_client: mqtt.Client, topic: str) -> tuple:
    return mqtt_client.unsubscribe(topic)

def publish(mqtt_client: mqtt.Client, topic: str, message: str, qos:int) -> bool:
    result = mqtt_client.publish(topic, message, qos)
    result.wait_for_publish()
    return result.is_published()

def disconnect(mqtt_client: mqtt.Client):
    return mqtt_client.disconnect()

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

    client = connect_to_broker(BROKER_ADDRESS, "demo" ,on_message)

    subscribe(client, ECHO_TOPIC, 0)

    start_mqtt_thread(client)
    while True:
        for temp in TEMP_LIST:
            print("Is message published: ",publish(client, SEND_TOPIC, temp, 0))
            time.sleep(5)
    stop_mqtt_thread(client)
