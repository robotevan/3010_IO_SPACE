#MQTT backend data insertion script
import datetime
import backendAPI as api #API module to access and interface with our projects MQTT and MongoDB server

#Connection Fields
CONNECTION_STRING = "mongodb://192.168.1.48:27017"
BROKER_ADDRESS = "192.168.1.15"
SUB_TOPIC = "Data/#"

#Function call when a message is received
def on_message(client, userdata, message):
    print("Message on Topic:", message.topic, " QoS:", message.qos)
    data_string = str(message.payload.decode("utf-8"))
    print("Data:" ,data_string, "\n")
    topic_list = parse_topic(message.topic)

    if check_user_data(database, "user_data",topic_list[1]) == False: #Check the API Key
        print("Invalid API Key")
        topic_list[0] = "Data_reply/"
        api.publish(client, construct_topic(topic_list), "ERROR: bad_api_key", 1) #Return error message back to node
        return 0
    try:
        converted_message = float(data_string)
        if len(topic_list) == 4: # Verify topic format
            if not insert_data(database, topic_list[1], topic_list[2], topic_list[3], converted_message):
                topic_list[0] = "Data_reply/"
                api.publish(client, construct_topic(topic_list), "Internal Error: failed_data_insertion", 1)
        else: #Any other topic setup is invalid
            print("Invalid topic format message ignored!")
            return 0
    except Exception as e:
        print(e)
        print("Could not convert data, only floats and ints are allowed!")

#Splits a topic into a list
def parse_topic(topic: str) -> list:
    return topic.split("/")

#Reassmbels topic back into a string
def construct_topic(topic_list: list) -> str:
    return "/".join(topic_list)

def check_user_data(database, collection_name, api_key):
    user_doc = database[collection_name].find_one( {"api_key" : api_key} )
    if user_doc is None:
        return False
    return True if (user_doc["api_key"]) == api_key else False

#Checks if given node exists with in the system
def insert_data(database, api_key, node_name, device_name, data):
    if api_key not in database.list_collection_names():
        print("Database Error: User collection not found!")
        return False
    else:
        user_data = database[api_key] #pull user data using api key
        data_entry = {"node_name" : node_name, "device_name" : device_name, "data" : data, "date" : datetime.datetime.now()}
        user_data.insert_one(data_entry)
        return True


#Script Start#
#Connecting to database
database = api.connect_to_database(CONNECTION_STRING, "iospace")

#Connecting to broker and subscribe to SUB_TOPIC
client = api.connect_to_broker(BROKER_ADDRESS, "data", on_message)
api.subscribe(client, SUB_TOPIC, 1)

#Starting MQTT thread to listen for incoming messages
api.forever_mqtt_thread(client)