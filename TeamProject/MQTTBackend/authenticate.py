#MQTT backend authentication script
#Checks if newly connected nodes or devices are in the system, if not it adds them

import backendAPI as api #API module to access and interface with our projects MQTT and MongoDB server

#Connection Fields
CONNECTION_STRING = "mongodb://192.168.1.48:27017"
BROKER_ADDRESS = "192.168.1.15"
SUB_TOPIC = "Authenticate/#"

#Function call when a message is received
def on_message(client, userdata, message):
    topic_list = parse_topic(message.topic)
    message_data = message.payload.decode("utf-8")
    print("Message on Topic: ", message.topic, " QoS: ", message.qos)
    print("Data: " ,message_data, "\n")

    if len(topic_list) != 3 and len(topic_list) != 5 and len(topic_list) != 6:
        print("Message ignored, incorrect topic format!\n")
        return 0

    topic_list[0] = "Authenticate_reply"

    if check_API_key(database, "user_data",topic_list[1]) == False: #Check the API Key
        print("Invalid API Key")
        api.publish(client, construct_topic(topic_list), "ERROR: bad_api_key", 1) #Return error message back to node
        return 0
    elif message_data == "connection_request":
        if len(topic_list) == 3: #Topic of 3 elements is a node trying to connect
            if node_check(database, "user_data", topic_list[1], topic_list[2]):
                api.publish(client, construct_topic(topic_list), "connection_accepted", 1)
            else:
                api.publish(client, construct_topic(topic_list), "connection_denied", 1)
        elif len(topic_list) == 5: #Topic of 5 elements is a device trying to connect
            if node_check(database, "user_data", topic_list[1], topic_list[2]) and device_check(database, "user_data", topic_list[1], topic_list[2], topic_list[3], topic_list[4]):
                api.publish(client, construct_topic(topic_list), "connection_accepted", 1)
            else:
                api.publish(client, construct_topic(topic_list), "connection_denied", 1)
        elif len(topic_list) == 6:  # Topic of 5 elements is a device trying to connect
            if node_check(database, "user_data", topic_list[1], topic_list[2]) and device_check(database, "user_data", topic_list[1], topic_list[2], topic_list[3], topic_list[4], topic_list[5]):
                api.publish(client, construct_topic(topic_list), "connection_accepted", 1)
            else:
                api.publish(client, construct_topic(topic_list), "connection_denied", 1)

#Splits a topic into a list
def parse_topic(topic: str) -> list:
    return topic.split("/")

#Reassmbels topic back into a string
def construct_topic(topic_list: list) -> str:
    return "/".join(topic_list)

def check_API_key(database, collection_name, api_key):
    user_doc = database[collection_name].find_one( {"api_key" : api_key} )
    if user_doc is None:
        return False
    return True if (user_doc["api_key"]) == api_key else False

#Checks if given node exists with in the system
def node_check(database, collection_name, api_key, node_name):
    node_name = node_name.lower()
    user_doc = database[collection_name].find_one( {"api_key" : api_key} ) #pull user data using api key

    if type(user_doc["nodes"]) == list: #verify database nodes entry is a list
        if node_name in user_doc["nodes"]: #checks if the node is in the users nodes entry
            print(node_name, "found in database.")
            return True
        else: #If node doesn't exist, add it
            if len(user_doc["nodes"]) == len(user_doc["devices"]) and type(user_doc["devices"]) == list:
                user_doc["nodes"].append(node_name)
                user_doc["devices"].append([])
                database[collection_name].update_one({"_id" : user_doc ["_id"]}, { "$set" : {"nodes" : user_doc["nodes"], "devices": user_doc["devices"]}})
                print(node_name, " added to database")
                return True
            else:
                print("Node and Device arrays are mismatched in size! \n")
                return False
    else:
        print("Incorrect data type for device entry inside of document! \n")
        return False

#Checks if given device exists with in the system
def device_check(database, collection_name,api_key, node_name, device_type, device_name, feedback_type=None):
    node_name = node_name.lower()
    device_name = device_name.lower()
    device_type = device_type.lower()
    device_name = device_name.lower()
    user_doc = database[collection_name].find_one({"api_key": api_key}) #pull user data using api key
    device = ":".join([device_type, device_name]) #creates a string following "device_type:device_name: format

    if type(user_doc["devices"]) == list:
        try: #fetch the nodes index and use it to get the device index
            index = user_doc["nodes"].index(node_name)
            device_list = user_doc["devices"][index]
        except Exception as error:
            print(error)
            print("Unable to fetch index of node from database document! \n")
            return False

        if device in device_list: #check if the device is in the users device entry
            print(device_name, "found in database.")
            return True
        else: #If device doesn't exist, add it
            if device_type == "feedback":
                feedback_doc = database[api_key + "_feedback"].find_one({"node_name": node_name, "device_name" : device_name})
                if feedback_doc is None and feedback_type is not None:
                    feedback_type = feedback_type.lower()
                    if feedback_type == "switch":
                        database[api_key + "_feedback"].insert_one({"node_name": node_name, "device_name": device_name, "data_type": feedback_type, "data": "off"})
                    elif feedback_type == "value":
                        database[api_key + "_feedback"].insert_one({"node_name": node_name, "device_name": device_name, "data_type": feedback_type, "data" : "0"})
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

#Script Start#
#Connecting to database
database = api.connect_to_database(CONNECTION_STRING, "iospace")

#Connecting to broker and subscribe to SUB_TOPIC
client = api.connect_to_broker(BROKER_ADDRESS, "authenticate", on_message)
api.subscribe(client, SUB_TOPIC, 1)

#Starting MQTT thread to listen for incoming messages
api.forever_mqtt_thread(client)
