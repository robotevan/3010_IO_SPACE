#IOSpace Client Side API
import paho

node_ready = False
MQTT_ADDRESS = ""

class MQTT:

    def __init__(self, client_name):
        self.client_name = client_name


class Node:
    def __init__(self, name):
        MQTT.__init__()

    def setup(self):
        print()

class Device:
    def __init__(self, name):
        print(name)