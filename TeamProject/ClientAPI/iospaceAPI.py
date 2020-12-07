# IOSpace Client Side API
import paho.mqtt.client as mqtt
import threading
import time

class IOSpace:

    def on_message(self, client, userdata, message):
        msg = message.payload.decode("utf-8")
        topic_list = self._parse_topic(message.topic)
        if self.debug: print("Message on Topic: ", message.topic, "QoS: ", message.qos)
        if self.debug: print("Message:", msg)

        if msg == "connection_accepted":
            self.node_ready = True
        elif "error" in msg.lower():
            print(msg)
        elif topic_list[0] == "Feedback_receive":
            self.feedback_request_pending = True
            self.feedback_value = msg

    def __init__(self, apikey: str, node_name: str, address: str, feedback: bool, device_name:str, device_function, feedback_device_type=None ,timeout=30, debug=False):
        self.node_ready = False
        self.apikey = apikey
        self.node_name = node_name.lower()
        self.device_name = device_name.lower()
        self.device_started = False

        if feedback:
            if  feedback_device_type == None or (feedback_device_type.lower() != "value" and feedback_device_type.lower() != "switch"):
                raise ValueError("feedback_device_type required for feedback devices. Options: \"Value\" or \"Switch\"")
            else:
                self.feedback_device_type = feedback_device_type.lower()
                self.send_topic = "Feedback/" + self.apikey + "/" + self.node_name + "/" + self.device_name + "/" + self.feedback_device_type
                self.receive_topic = "Feedback_receive/" + self.apikey + "/" + self.node_name + "/" + self.device_name + "/" + self.feedback_device_type
                self.device_type = "feedback"
                self.feedback_request_pending = False
                self.feedback_value = None
        else:
            self.device_type = "sensor"
            self.send_topic = "Data/" + self.apikey + "/" + self.node_name + "/" + self.device_name
            self.receive_topic = "Data_reply/" + self.apikey + "/" + self.node_name + "/" + self.device_name

        self.client_name = apikey + "_" + self.node_name + "_" + self.device_type + "_" + device_name
        self.address = address
        self.timeout = timeout
        self.message_function = self.on_message
        self.debug = debug
        self.device_function = device_function
        self.mqtt_client = self.connect_to_broker(self.address, self.client_name, self.message_function, self.timeout)
        if not self._authenticate_node_request():
            raise ConnectionError("Device authentication request failed, no response from server!")
        self.device_thread = None
        self.thread_running = False

    def connect_to_broker(self, address: str, client_name: str, message_function, timeout) -> mqtt.Client:
        if self.debug: print("Connecting to MQTT Server on", address)
        mqtt_client = mqtt.Client(client_name)
        mqtt_client.CONNECTION_TIMEOUT_DEFAULT = timeout
        mqtt_client.on_message = message_function  # attach function to callback
        mqtt_client.connect(address)
        if self.debug: print("Connected to MQTT Server, Client:", client_name)
        return mqtt_client

    def _subscribe(self, topic: str, qos: int) -> tuple:
        if self.debug: print("Subscribing to", topic)
        return self.mqtt_client.subscribe(topic, qos)

    def _unsubscribe(self, topic: str) -> tuple:
        if self.debug: print("Unsubscribing from", topic)
        return self.mqtt_client.unsubscribe(topic)

    def _publish(self, topic: str, message: str, qos: int) -> bool:
        if self.debug: print("Publishing", "message:", message, "on", topic, "QoS: ", qos)
        result = self.mqtt_client.publish(topic, message, qos)
        result.wait_for_publish()
        return result.is_published()

    def _disconnect(self):
        if self.debug: print("Disconnected from MQTT Server.")
        return self.mqtt_client.disconnect()

    def _start_mqtt_thread(self):
        if self.debug: print("Listening for messages...")
        self.mqtt_client.loop_start()

    def _stop_mqtt_thread(self):
        if self.debug: print("Stopped listening for messages.")
        self.mqtt_client.loop_stop()

    def _forever_mqtt_thread(self):
        if self.debug: print("Listening for messages indefinitely...")
        self.mqtt_client.loop_forever()

    def is_connected(self):
        return self.mqtt_client.is_connected()

    # Splits a topic into a list
    def _parse_topic(self, topic):
        return topic.split("/")

    # Reassmbels topic back into a string
    def _construct_topic(self, topic_list):
        return "/".join(topic_list)

    def _authenticate_node_request(self):
        try:
            self.feedback_device_type
        except AttributeError:
            request_topic = "Authenticate/" + self.apikey + "/" + self.node_name + "/" + self.device_type + "/" + self.device_name
            receive_topic = "Authenticate_reply/" + self.apikey + "/" + self.node_name + "/" + self.device_type + "/" + self.device_name
        else:
            request_topic = "Authenticate/" + self.apikey + "/" + self.node_name + "/" + self.device_type + "/" + self.device_name + "/" + self.feedback_device_type
            receive_topic = "Authenticate_reply/" + self.apikey + "/" + self.node_name + "/" + self.device_type + "/" + self.device_name + "/" + self.feedback_device_type

        self._start_mqtt_thread()
        self._subscribe(receive_topic, 1)
        self._publish(request_topic, "connection_request", 1)

        timeout = time.time() + 5  # 5 sec from now

        while True:
            if self.node_ready:
                self._unsubscribe(receive_topic)
                self._stop_mqtt_thread()
                return True
            elif time.time() > timeout:
                if self.debug: print("ERROR: Device authentication request failed!")
                self._unsubscribe(receive_topic)
                self._stop_mqtt_thread()
                return False

    def start(self):
        if not self.device_started:
            self._start_mqtt_thread()
            self.device_started = True
            self.thread_running = True
            if self.device_type == "feedback":
                self._subscribe(self.receive_topic, 1)
                self.device_thread = threading.Thread(target=self.feedback_thread_function)
                self.device_thread.start()
            else:
                self._subscribe(self.receive_topic, 1)
                self.device_thread = threading.Thread(target=self.sensor_thread_function)
                self.device_thread.start()

    def feedback_thread_function(self):
        while True:
            if self.feedback_request_pending:
                self.feedback_request_pending = False
                if self.feedback_device_type == "switch":
                    self.device_function(self.feedback_value)
                elif self.feedback_device_type == "value":
                    self.device_function(int(self.feedback_value))

    def sensor_thread_function(self):
        while True:
            self._publish(self.send_topic, self.device_function(), 0)
            time.sleep(10)

    def stop(self):
        if self.device_started:
            self._start_mqtt_thread()
            self.device_started = False
            self._unsubscribe(self.receive_topic)
            self.thread_running = False
            self.device_thread.join()


if __name__ == "__main__":

    def func(value):
        print(value)

    test = IOSpace("luj3o4u3d814", "Node1", "192.168.1.15", True, "Light", func, "Switch",debug=True)
    test.start()
    time.sleep(1)
    test.stop()
