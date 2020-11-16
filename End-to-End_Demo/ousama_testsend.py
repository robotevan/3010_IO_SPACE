#import all libraries
import paho.mqtt.client as mqtt
import time
import random

#address of mqtt server
broker_address = "198.91.181.118"
#connecting to server as ousama
print("creating new instance")
client = mqtt.Client("ousama")
#creating connection to mqtt server
print("connecting to broker")
client.connect(broker_address)
#sending random data between 0 and 100
while True:
    rdata=random.randint(0,100)
    client.publish("testecho",rdata)
    print("publshing: ",rdata)
    time.sleep(5)
