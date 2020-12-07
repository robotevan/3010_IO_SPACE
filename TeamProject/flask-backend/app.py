from flask import Flask
from flask import request
import pymongo
from email_services import send_email
import random
import string
import paho.mqtt.client as mqtt

APIKEY_LENGTH = 12
MQTT_CLIENT_NAME = "website_backend"
MQTT_ADDRESS = "192.168.1.15"
MQTT_TIMEOUT = 5
FEEDBACK_REQUEST_TOPIC = "Feedback/Website"

app = Flask("__name__")

mqtt_client = mqtt.Client(MQTT_CLIENT_NAME)
mqtt_client.CONNECTION_TIMEOUT_DEFAULT = MQTT_TIMEOUT
mqtt_client.connect(MQTT_ADDRESS)

client = pymongo.MongoClient("mongodb://192.168.1.48:27017")
db = client['iospace']

EMAIL_NOTIFICATION_SUBJECT = "IOSpace API Key"
EMAIL_NOTIFICATION_TEXT = "Below is your new IO Space API key, keep a copy of this on your local machine as you will " \
                          "need it to add new nodes! This key is what lets you connect to your IO Space!\n \n"


def get_user_nodes(api_key):
    device_lst = []
    # Get the user_data collection
    user_data_collection = db['user_data']
    doc = user_data_collection.find_one({'api_key': api_key})
    nodes = doc['nodes']
    # Iterate over devices to generate json text
    for node_id_num in range(len(nodes)):
        devices = doc['devices'][node_id_num]

        for device in devices:
            node_name = nodes[node_id_num]
            device_type, device_name = device.split(":")
            # Retrieve the appropriate collection
            if device_type == "sensor":
                device_collection_type = ""
            else:
                device_collection_type = "_feedback"
            device_collection = db[api_key+device_collection_type]
            device_info = device_collection.find_one({'device_name': device_name, 'node_name': node_name},
                                                     sort=[('_id', pymongo.DESCENDING)])

            device_data_type = None
            device_curr_time = None
            device_curr_val = None
            # Set the device fields
            if device_type == "feedback":
                device_data_type = device_info['data_type']
                device_curr_val = ['data']
                device_curr_time = None  # Feedback has no timestamp
            elif device_type == "sensor":
                device_data_type = None  # sensor has no data_type
                device_curr_val = ['data']
                device_curr_time = ['date']
            # Append device json description to list
            device_lst.append({'nodeId': node_name, 'deviceId': len(device_lst), 'deviceType': device_type,
                               'deviceName': device_name, 'deviceCurrVal': device_curr_val,
                               'data_type': device_data_type, 'timestamp': device_curr_time})

    return {'devices': device_lst}


@app.route('/login/user', methods=["GET"])
def verify_login():
    print("HERE")
    try:
        api_key = request.args.get('api_key')  # Fetch the api provided by the user
        if db['user_data'].find_one({"api_key": api_key}) is not None:
            return {"valid_user": True}
        else:
            return {"valid_user": False}
    except Exception:
        return {"valid_user": False}


@app.route('/newUser/user')
def create_user_apikey():
    email = request.args.get("email")  # Fetch provided email
    if db["user_data"].find_one({"email": email}) is not None:
        return {"success": False}  # This email is already in the database!
    # List containing 2 lambda functions, one to get rand int, one for rand char
    rand_char = [lambda: random.choice(string.ascii_lowercase), lambda: random.randint(0, 9)]
    while True:  # keeps on looping until finds a unique api key
        api_key = ""
        for i in range(APIKEY_LENGTH):  # generate random values
            api_key += str(random.choice(rand_char)())
        data_base_api_key = db["user_data"].find_one({"api_key": api_key})
        if data_base_api_key is None:
            new_data = {"email": email,
                        "api_key": api_key,
                        "nodes": [],
                        "devices": []}
            db["user_data"].insert_one(new_data)
            # Send an email to the user, containing the API key
            send_email(EMAIL_NOTIFICATION_SUBJECT, EMAIL_NOTIFICATION_TEXT + api_key, email)
            # we need to also create collections for the users devices
            db.create_collection(api_key + "_feedback")
            db.create_collection(api_key)
            db[api_key+"_feedback"].insert_one({"REQUIRED_PYMONGO_SHIT":"ABC"})
            db[api_key].insert_one({"REQUIRED_PYMONGO_SHIT": "ABC"})
            break


@app.route('/MyIOSpace', methods=['GET'])
def fetch_devices():
    api_key = request.args.get("api_key")
    print(api_key)
    try:
        devices = get_user_nodes(api_key)
        return devices
    except Exception:
        return {'devices': 'NoneFound'}


@app.route('/MyIOSpace/deviceOn')
def set_device_on():
    print("turning device on")
    api_key = str(request.args.get("api_key"))
    node_name = str(request.args.get("node_name"))
    device_name = str(request.args.get("device_name"))
    payload = api_key + ":" + node_name + ":" + device_name + ":switch:on"
    mqtt_client.publish(FEEDBACK_REQUEST_TOPIC, payload, 1)
    return {"deviceState": 1}


@app.route('/MyIOSpace/deviceOff')
def set_device_off():
    print("Turning device off")
    api_key = str(request.args.get("api_key"))
    node_name = str(request.args.get("node_name"))
    device_name = str(request.args.get("device_name"))
    payload = api_key + ":" + node_name + ":" + device_name + ":switch:off"
    mqtt_client.publish(FEEDBACK_REQUEST_TOPIC, payload, 1)
    return {"deviceState": 0}

@app.route('/MyIOSpace/currState')
def get_current_state():
    api_key = str(request.args.get("api_key"))
    node_name = str(request.args.get("node_name"))
    device_name = str(request.args.get("device_name"))
    doc = db[api_key + "_feedback"].find_one({"node_name": node_name, "device_name": device_name, "device_state" : "switch"})
    return {"deviceVal": doc["data"]}


@app.route('/MyIOSpace/sensorData')
def fetch_sensor_data():
    api_key = str(request.args.get("api_key"))
    node_name = str(request.args.get("node_name"))
    device_name = str(request.args.get("device_name"))
    query_size = db[api_key].count_documents({"node_name" : node_name, "device_name" : device_name})
    if query_size == 0:
        return {"deviceData": 'None'}
    else:
        documents = db["i3fy7j98zbqc"].find({"node_name" : node_name, "device_name" : device_name}).sort("_id", -1).limit(50)
        data_list = []
        i = 0
        for doc in documents:
            date = doc["date"]
            date_string = str(date.hour) + ":" + str(date.minute) + ":" + str(date.second)
            data_list.append({'y': doc["data"], 'x': i})
            i+=1
        print(data_list)
        return {"deviceData": data_list}


if __name__ == '__main__':
    app.run(debug=True)
