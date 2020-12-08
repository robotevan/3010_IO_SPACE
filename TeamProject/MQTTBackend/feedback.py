# MQTT backend feedback device status update script
# Process feedback changes and change requests and relays updates to corresponding devices

import backendAPI as api  # API module to access and interface with our projects MQTT and MongoDB server

# Message format from website "apikey:Node_Name:Device_name:value type:Value"
# From device Feedback/Apikey/Node_name/Device_name/Value_type  "Value"

# Connection Fields
CONNECTION_STRING = "mongodb://192.168.1.48:27017"
BROKER_ADDRESS = "192.168.1.15"
SUB_TOPIC = "Feedback/#"
DEVICE_RECEIVE_TOPIC_HEADER = "Feedback_receive"


# Function call when a message is received
def on_message(client, userdata, message):
    print("\nMessage on Topic:", message.topic, " QoS:", message.qos)
    data_string = str(message.payload.decode("utf-8")).lower()
    print("Data:", data_string, "\n")
    topic_list = api.parse_topic(message.topic)
    msg_list = api.parse_msg(data_string)

    if topic_list[1].lower() == "website":  # Process feedback change request from website
        if update_db_feedback_device(db, msg_list[0], msg_list[1], msg_list[2], msg_list[3], msg_list[4]):
            api.publish(client, api.construct_topic(
                [DEVICE_RECEIVE_TOPIC_HEADER, msg_list[0], msg_list[1], msg_list[2], msg_list[3]]), msg_list[4], 1)
    elif len(topic_list) == 5:  # Process feedback change from device
        if not api.check_user_data(db, "user_data", topic_list[1]):
            print("Invalid API Key")
            topic_list[0] = DEVICE_RECEIVE_TOPIC_HEADER
            api.publish(client, api.construct_topic(topic_list), "ERROR: bad_api_key", 1)
        elif not update_db_feedback_device(db, topic_list[1], topic_list[2], topic_list[3], topic_list[4],
                                           data_string):
            topic_list[0] = DEVICE_RECEIVE_TOPIC_HEADER
            api.publish(client, api.construct_topic(topic_list), "Error: Failed to update feedback device!", 1)
    else:
        print("Invalid topic received, message ignored!")
        return 0


# Updates the database with feedback change requests
def update_db_feedback_device(database, api_key, node_name, device_name, data_type, data):
    collection_name = api_key + "_feedback"
    if collection_name not in database.list_collection_names():
        print("Database Error: User collection not found!")
        return False
    else:
        feedback_collection = database[collection_name]
        feedback_document = feedback_collection.find_one(
            {"node_name": node_name, "device_name": device_name, "data_type": data_type})
        if feedback_document is None:
            print("Error: Device does not exist in database!")
            return False

        if data_type.lower() == "switch" and (data.lower() == "on" or data.lower() == "off"):
            feedback_collection.update_one({"_id": feedback_document["_id"]}, {"$set": {"data": data.lower()}})
            return True
        elif data_type.lower() == "value":
            try:
                value = int(data)
                feedback_collection.update_one({"_id": feedback_document["_id"]}, {"$set": {"data": value}})
                return True
            except:
                print("Could not convert expected value type data to int!")
                return False
        else:
            print("Invalid data type or data!")
            return False


# Script Start #
db = api.connect_to_database(CONNECTION_STRING, "iospace")

mqtt_client = api.connect_to_broker(BROKER_ADDRESS, "feedback", on_message)
api.subscribe(mqtt_client, SUB_TOPIC, 1)

api.forever_mqtt_thread(mqtt_client)
