import paho.mqtt.client as mqtt
import pymongo
import datetime
import time

client = pymongo.MongoClient("mongodb://192.168.1.48:27017")
database = client.iospace
collection = database.test

def on_message(client, userdata, message):
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic =",message.topic)
    print("message qos =",message.qos)
    print("message retain flag =",message.retain)
    collection.insert_one({
        "node_name": "node",
        "device_type": "sensor",
        "device_name": "temperature",
        "data": int(message.payload.decode("utf-8")),
        "date": datetime.datetime.now()
    })
    
temp_list = [23, 24, 25, 26, 27]

broker_address="192.168.1.15"

print("creating new instance")
client = mqtt.Client("backend")

client.on_message=on_message #attach function to callback

print("connecting to broker")
client.connect(broker_address)

print("Subscribing to topic","testecho")
client.subscribe("testecho")

client.loop_start()

while True:
    for temp in temp_list:
        print("publishing on test Temp: ", temp)
        client.publish("test", temp)
        time.sleep(5)
        
client.loop_stop()