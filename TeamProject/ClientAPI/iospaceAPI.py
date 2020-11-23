#IOSpace Client Side API
import paho.mqtt.client as mqtt

class MQTT:

    def __init__(self, address, client_name, timeout=30):
        self.client_name = client_name
        self.address = address
        self.timeout = timeout
        self.mqtt_client = self.connect_to_broker(self.address, self.client_name, self.on_message, self.timeout)

    def on_message(self, client, userdata, message):
        print("message received ", str(message.payload.decode("utf-8")))
        print("message topic =", message.topic)
        print("message qos =", message.qos)
        print("message retain flag =", message.retain)
        print(self.client_name)

    def connect_to_broker(self, address: str, client_name: str, message_function, timeout) -> mqtt.Client:
        print("Connecting to MQTT Server on", address)
        mqtt_client = mqtt.Client(client_name)
        mqtt_client.CONNECTION_TIMEOUT_DEFAULT = timeout
        mqtt_client.on_message = message_function  # attach function to callback
        mqtt_client.connect(address)
        print("Connected to MQTT Server, Client:", client_name)
        return mqtt_client

    def subscribe(self, topic: str, qos: int) -> tuple:
        print("Subscribing to ", topic)
        return self.mqtt_client.subscribe(topic, qos)

    def unsubscribe(self, topic: str) -> tuple:
        print("Unsubscribing to ", topic)
        return self.mqtt_client.unsubscribe(topic)

    def publish(self, topic: str, message: str, qos: int) -> bool:
        result = self.mqtt_client.publish(topic, message, qos)
        result.wait_for_publish()
        print("Publishing", "message:", message, "on", topic, " QoS: ", qos)
        return result.is_published()

    def disconnect(self):
        print("Disconnected from MQTT Server.")
        return self.mqtt_client.disconnect()

    def start_mqtt_thread(self):
        print("Listening for messages...")
        self.mqtt_client.loop_start()

    def stop_mqtt_thread(self):
        print("Stopped listening for messages.")
        self.mqtt_client.loop_stop()

    def forever_mqtt_thread(self):
        print("Listening for messages indefinitely...")
        self.mqtt_client.loop_forever()

    def is_connected(self):
        return self.mqtt_client.is_connected()

    # Splits a topic into a list
    def parse_topic(topic: str) -> list:
        return topic.split("/")

    # Reassmbels topic back into a string
    def construct_topic(topic_list: list) -> str:
        return "/".join(topic_list)


class Node:

    def __init__(self, apikey, node_name, address):
        self.device_list = []
        self.node_ready = False
        self.apikey = apikey
        self.node_name = node_name
        self.client_name = apikey + "_" + node_name
        self.MQTT = MQTT(self.client_name, address)
        node_ready = self.authenticate_request(self.MQTT)

    def authenticate_node_request(self, MQTT):
        request_topic = "Authenticate/" + self.apikey + "/" + self.node_name
        MQTT.publish("connection_request", request_topic, 1)
        response_received = False
        while not response_received:
            response_received = True
        return False

    def add_new_device(self, device_type, device_name):
        device = Device(device_type, device_name)
        self.device_list.append(device)

class Device:

    def __init__(self, device_type, device_name, device_function):
        self.device_ready = False
        self.device_type = device_type
        self.device_name = device_name
        self.device_function = device_function
        self.device_ready = self.authenticate_device_request(self.MQTT)

    def authenticate_device_request(self, MQTT):
        return False

    def start_device(self):
        return False


if __name__ == "__main__":
    m = MQTT("client", "192.168.1.15")
    m.subscribe("test", 1)
    m.forever_mqtt_thread()
