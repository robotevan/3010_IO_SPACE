import paho.mqtt.client as mqtt
import time

def on_message(client, userdata, message):
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic =",message.topic)
    print("message qos =",message.qos)
    print("message retain flag =",message.retain)
    print("Publishing message to topic","testecho")
    client.publish("testecho",str(message.payload.decode("utf-8")))
    
broker_address="192.168.1.15"

print("creating new instance")
client = mqtt.Client("P1")

client.on_message=on_message #attach function to callback

print("connecting to broker")
client.connect(broker_address)

print("Subscribing to topic","test")
client.subscribe("test")

client.loop_forever()