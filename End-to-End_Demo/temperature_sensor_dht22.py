import adafruit_dht
import send_insert as api_prototype
import time

#api_prototype setup broker only
SEND_TOPIC = "testecho"
BROKER_ADDRESS = "192.168.1.15"
client = api_prototype.connect_to_broker(BROKER_ADDRESS, "temp_test", api_prototype.on_message)

DHT_PIN = 17
DHT_SENSOR = adafruit_dht.DHT22(DHT_PIN)

api_prototype.start_mqtt_thread(client)
while True:
    try:
        temperature = DHT_SENSOR.temperature
        humidity = DHT_SENSOR.humidity
        print("Temp={0:0.1f}*C  Humidity={1:0.1f}%".format(temperature, humidity))
        api_prototype.publish(client, SEND_TOPIC, temperature, 0)
        time.sleep(10)
    except RuntimeError as error:
        print(error.args[0])
        time.sleep(10)
        continue
    except Exception as error:
        DHT_SENSOR.exit()
        raise error
api_prototype.stop_mqtt_thread(client)
