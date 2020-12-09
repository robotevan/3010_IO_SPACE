import adafruit_dht
import RPi.GPIO as GPIO
import iospaceAPI as api
import random

API_KEY = "i3fy7j98zbqc"
NODE_NAME = "my_node"
LED_DEVICE_NAME = "lights"
DHT_DEVICE_NAME = "temperature"
SERVER_ADDRESS = "192.168.1.15"
LED_PIN = 23
DHT_PIN = 17

DHT_SENSOR = adafruit_dht.DHT22(DHT_PIN)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.output(LED_PIN, GPIO.LOW)


def get_temperature_value():
    try:
        temperature = DHT_SENSOR.temperature
        print("Temp={0:0.1f}*C".format(temperature))
        return temperature
    except RuntimeError as error:
        print(error.args[0])
    except Exception as error:
        DHT_SENSOR.exit()
        raise error


def change_lights(value):
    print(value)
    if value == "on":
        GPIO.output(LED_PIN, GPIO.HIGH)
    elif value == "off":
        GPIO.output(LED_PIN, GPIO.LOW)

def random_int():
    return random.randint(0,10)


dht_device = api.IOSpace(API_KEY, NODE_NAME, SERVER_ADDRESS, False, DHT_DEVICE_NAME, get_temperature_value)


light_device = api.IOSpace(API_KEY, NODE_NAME, SERVER_ADDRESS, True, LED_DEVICE_NAME, change_lights, "switch",debug=True)


rand = api.IOSpace(API_KEY, NODE_NAME, SERVER_ADDRESS, False, "test", random_int,debug=True)


#dht_device.start()
#light_device.start()
rand.start()

#time.sleep(1)

#dht_device.stop()
#dht_device.stop()
