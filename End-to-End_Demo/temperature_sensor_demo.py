# Using a DHT11 Temperature and Humidity sensor
import send_insert as api_prototype
import RPi.GPIO as GPIO
import dht11
import time

#api_prototype setup broker only
SEND_TOPIC = "testecho"
BROKER_ADDRESS = "192.168.1.15"
client = api_prototype.connect_to_broker(BROKER_ADDRESS, "temp_test", api_prototype.on_message)

# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

instance = dht11.DHT11(pin=17)

api_prototype.start_mqtt_thread(client)
while True:
    reading = instance.read()
    if reading.is_valid():
        print('Temperature = ' + str(reading.temperature) + '*C' + '  Humidity = ' + str(reading.humidity) + '%')
        api_prototype.publish(client, SEND_TOPIC, reading.temperature, 0)
    else:
        print('Unable to Get Reading!')
    time.sleep(10)
api_prototype.stop_mqtt_thread(client)
