#MQTT backend feedback device status update script
import datetime
import backendAPI as api #API module to access and interface with our projects MQTT and MongoDB server

#Message format from website "apikey:Node_Name:Device_name:value type:Value"
#From device Feedback/Apikey/Node_name/Devce_name/Value_type  "Value"

#Connection Fields
CONNECTION_STRING = "mongodb://192.168.1.48:27017"
BROKER_ADDRESS = "192.168.1.15"
SUB_TOPIC = "Feedback_s/#"
DEVICE_RECEIVE_TOPIC_HEADER = "Feedback_r"

#Function call when a message is received
def on_message(client, userdata, message):
    print("\nMessage on Topic:", message.topic, " QoS:", message.qos)
    data_string = str(message.payload.decode("utf-8"))
    print("Data:" ,data_string, "\n")
    topic_list = api.parse_topic(message.topic)
    msg_list = api.parse_msg(data_string)

    if (topic_list[1].lower() == "website"):
        if update_db_feedback_device(database, msg_list[0], msg_list[1], msg_list[2], msg_list[3], msg_list[4]):
            api.publish(client, api.construct_topic([DEVICE_RECEIVE_TOPIC_HEADER, msg_list[0], msg_list[1], msg_list[2], msg_list[3]]), msg_list[4], 0)
    elif len(topic_list) == 5:
        if check_user_data(database, "user_data",topic_list[1]) == False: #Check the API Key
            print("Invalid API Key")
            topic_list[0] = DEVICE_RECEIVE_TOPIC_HEADER
            api.publish(client, api.construct_topic(topic_list), "ERROR: bad_api_key", 1) #Return error message back to node
        elif update_db_feedback_device(database, topic_list[1], topic_list[2], topic_list[3], topic_list[4], data_string) == False:
            topic_list[0] = DEVICE_RECEIVE_TOPIC_HEADER
            api.publish(client, api.construct_topic(topic_list), "Error: Failed to update feedback device!", 1)
    else:
        print("Invalid topic received!")

def check_user_data(database, collection_name, api_key):
    user_doc = database[collection_name].find_one( {"api_key" : api_key} )
    if user_doc is None:
        return False
    return True if (user_doc["api_key"]) == api_key else False

#Checks if given node exists with in the system
def update_db_feedback_device(database, api_key, node_name, device_name, data_type, data):
    collection_name = api_key + "_feedback"
    if collection_name not in database.list_collection_names():
        print("Database Error: User collection not found!")
        return False
    else:
        feedback_collection = database[collection_name]
        feedback_document = feedback_collection.find_one( {"node_name" : node_name, "device_name" : device_name, "data_type": data_type})
        if feedback_document == None:
            print("Device does not exist in database!")
            return False

        if data_type.lower() == "switch" and (data.lower() == "on" or data.lower() == "off"):
            feedback_collection.update_one({"_id": feedback_document["_id"]}, {"$set": {"data" : data.lower()}})
            return True
        elif data_type.lower() == "value":
            try:
                value = int(data)
                return True
            except:
                print("Could not convert expected value type data to int!")
                return False
        else:
            print("Invalid data type or data!")
            return False

#Script Start#
#Connecting to database
database = api.connect_to_database(CONNECTION_STRING, "iospace")

#Connecting to broker and subscribe to SUB_TOPIC
client = api.connect_to_broker(BROKER_ADDRESS, "data", on_message)
api.subscribe(client, SUB_TOPIC, 1)

#Starting MQTT thread to listen for incoming messages
api.forever_mqtt_thread(client)