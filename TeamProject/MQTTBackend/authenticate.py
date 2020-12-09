# MQTT backend authentication script
# Checks if newly connected nodes or devices are in the system, if not it adds them

import backendAPI as api  # API module to access and interface with our projects MQTT and MongoDB server

# Connection Fields
CONNECTION_STRING = "mongodb://192.168.1.48:27017"
BROKER_ADDRESS = "192.168.1.15"
SUB_TOPIC = "Authenticate/#"


# Function call when a message is received
def on_message(client, userdata, message):
    topic_list = api.parse_topic(message.topic)
    message_data = message.payload.decode("utf-8")
    print("Message on Topic: ", message.topic, " QoS: ", message.qos)
    print("Data: ", message_data, "\n")

    if len(topic_list) != 3 and len(topic_list) != 5 and len(topic_list) != 6:
        print("Message ignored, incorrect topic format!\n")
        return 0

    topic_list[0] = "Authenticate_reply"

    if api.check_API_key(db, "user_data", topic_list[1]) == False:
        print("Invalid API Key")
        api.publish(client, api.construct_topic(topic_list), "ERROR: bad_api_key", 1)
        return 0
    elif message_data == "connection_request":
        if len(topic_list) == 3:  # Topic of 3 elements is a node trying to connect
            if node_check(db, "user_data", topic_list[1], topic_list[2]):
                api.publish(client, api.construct_topic(topic_list), "connection_accepted", 1)
            else:
                api.publish(client, api.construct_topic(topic_list), "connection_denied", 1)
        elif len(topic_list) == 5:  # Topic of 5 elements is a device trying to connect
            if node_check(db, "user_data", topic_list[1], topic_list[2]) and device_check(db, "user_data",
                                                                                                topic_list[1],
                                                                                                topic_list[2],
                                                                                                topic_list[3],
                                                                                                topic_list[4]):
                api.publish(client, api.construct_topic(topic_list), "connection_accepted", 1)
            else:
                api.publish(client, api.construct_topic(topic_list), "connection_denied", 1)
        elif len(topic_list) == 6:  # Topic of 5 elements is a device trying to connect
            if node_check(db, "user_data", topic_list[1], topic_list[2]) and device_check(db, "user_data",
                                                                                                topic_list[1],
                                                                                                topic_list[2],
                                                                                                topic_list[3],
                                                                                                topic_list[4],
                                                                                                topic_list[5]):
                api.publish(client, api.construct_topic(topic_list), "connection_accepted", 1)
            else:
                api.publish(client, api.construct_topic(topic_list), "connection_denied", 1)


# Checks if given node exists with in the system
def node_check(database, collection_name, api_key, node_name):
    node_name = node_name.lower()
    user_doc = database[collection_name].find_one({"api_key": api_key})  # pull user data using api key

    if type(user_doc["nodes"]) == list:  # verify database nodes entry is a list
        if node_name in user_doc["nodes"]:
            print(node_name, "found in database.")
            return True
        else:  # If node doesn't exist, add it
            if len(user_doc["nodes"]) == len(user_doc["devices"]) and type(user_doc["devices"]) == list:
                user_doc["nodes"].append(node_name)
                user_doc["devices"].append([])
                database[collection_name].update_one({"_id": user_doc["_id"]}, {
                    "$set": {"nodes": user_doc["nodes"], "devices": user_doc["devices"]}})
                print(node_name, " added to database")
                return True
            else:
                print("Node and Device arrays are mismatched in size! \n")
                return False
    else:
        print("Incorrect data type for device entry inside of document! \n")
        return False


# Checks if given device exists with in the system
def device_check(database, collection_name, api_key, node_name, device_type, device_name, feedback_type=None):
    node_name = node_name.lower()
    device_name = device_name.lower()
    device_type = device_type.lower()
    device_name = device_name.lower()
    user_doc = database[collection_name].find_one({"api_key": api_key})  # pull user data using api key
    device = ":".join([device_type, device_name])

    if type(user_doc["devices"]) == list:
        try:  # fetch the nodes index and use it to get the device index
            index = user_doc["nodes"].index(node_name)
            device_list = user_doc["devices"][index]
        except Exception as error:
            print(error)
            print("Unable to fetch index of node from database document! \n")
            return False

        if device in device_list:  # check if the device is in the users device entry
            print(device_name, "found in database.")
            return True
        else:  # If device doesn't exist, add it
            if device_type == "feedback":
                feedback_doc = database[api_key + "_feedback"].find_one(
                    {"node_name": node_name, "device_name": device_name})
                if feedback_doc is None and feedback_type is not None:
                    feedback_type = feedback_type.lower()
                    if feedback_type == "switch":
                        database[api_key + "_feedback"].insert_one(
                            {"node_name": node_name, "device_name": device_name, "data_type": feedback_type,
                             "data": "off"})
                    elif feedback_type == "value":
                        database[api_key + "_feedback"].insert_one(
                            {"node_name": node_name, "device_name": device_name, "data_type": feedback_type, "data": 0})
                elif feedback_type is None:
                    print("Unable to add feedback device to user_feedback collection!")
                    return False

            device_list.append(device)
            user_doc["devices"][index] = device_list
            database[collection_name].update_one({"_id": user_doc["_id"]}, {"$set": {"devices": user_doc["devices"]}})
            print(device_name, " added to database.")
            return True
    else:
        print("Incorrect data type for device entry inside of document! \n")
        return False


# Script Start#
db = api.connect_to_database(CONNECTION_STRING, "iospace")

client = api.connect_to_broker(BROKER_ADDRESS, "authenticate1", on_message)
api.subscribe(client, SUB_TOPIC, 1)

api.forever_mqtt_thread(client)
