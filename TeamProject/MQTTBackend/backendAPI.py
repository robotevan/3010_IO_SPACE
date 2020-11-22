import paho.mqtt.client as mqtt
import pymongo
import datetime

def connect_to_database(connection_string: str, database_name: str) -> pymongo.database.Database:
    mongo = pymongo.MongoClient(connection_string, serverSelectionTimeoutMS=2000)
    db_names = mongo.list_database_names()
    if database_name in db_names:
        print("Connected to MongoDB Server, returning ", database_name, " database")
        return mongo[database_name]
    else:
        raise NameError("database_name doesn't exist on server")

def get_collection(select_database: pymongo.database.Database, collection_name: str) -> pymongo.collection.Collection:
    collection_names = select_database.list_collection_names()
    if collection_name in collection_names:
        print("returning ", collection_name, " collection from database")
        return select_database[collection_name]
    else:
        raise NameError("collection_name doesn't exist on selected database")

def insert_into_collection(select_collection: pymongo.collection.Collection, node_name: str, device_name: str,
                           data: str) -> bool:
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
    print("Connecting to MQTT Server on ", address)
    mqtt_client = mqtt.Client(client_name)
    mqtt_client.CONNECTION_TIMEOUT_DEFAULT = timeout
    mqtt_client.on_message = message_function  # attach function to callback
    mqtt_client.connect(address)
    print("Connected to MQTT Server, Client: ", client_name)
    return mqtt_client

def subscribe(mqtt_client: mqtt.Client, topic: str, qos: int) -> tuple:
    print("Subscribing to ", topic)
    return mqtt_client.subscribe(topic, qos)

def unsubscribe(mqtt_client: mqtt.Client, topic: str) -> tuple:
    print("Unsubscribing to ", topic)
    return mqtt_client.unsubscribe(topic)

def publish(mqtt_client: mqtt.Client, topic: str, message: str, qos: int) -> bool:
    result = mqtt_client.publish(topic, message, qos)
    result.wait_for_publish()
    print("Publishing ", message, " on ", topic, " QoS: ", qos)
    return result.is_published()

def disconnect(mqtt_client: mqtt.Client):
    print("Disconnected from MQTT Server.")
    return mqtt_client.disconnect()

def start_mqtt_thread(mqtt_client: mqtt.Client):
    print("Listening to for messages...")
    mqtt_client.loop_start()

def stop_mqtt_thread(mqtt_client: mqtt.Client):
    print("Stopped listening to for messages.")
    mqtt_client.loop_stop()

def forever_mqtt_thread(mqtt_client: mqtt.Client):
    print("Listening to for messages indefinitely...")
    mqtt_client.loop_forever()

def query_collection(database, collection_name, field, data) -> bool:
    return False
