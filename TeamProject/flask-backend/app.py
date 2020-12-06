from flask import Flask
from flask import  request
import pymongo
from TeamProject.email_services import send_email
import random
import string
APIKEY_LENGTH = 12
app = Flask("__name__")
client = pymongo.MongoClient("mongodb://192.168.1.48:27017")
db = client['iospace']
EMAIL_NOTIFICATION_SUBJECT = "IOSpace API Key"
EMAIL_NOTIFICATION_TEXT = "Below is your new IO Space API key, keep a copy of this on your local machine. This key" \
                          "will be the way you connect to your IO Space!\n \n"


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
                                                     sort=[('_id', pymongo.ASCENDING)])
            # TODO: Revert to DESCENTING ^^^^
            # Set the device fields
            try:
                device_curr_val = device_info['data']
                device_curr_time = device_info['date']
            except TypeError:
                device_curr_val = 0
                device_curr_time = 0
            # Append device json description to list
            device_lst.append({'nodeId': node_name, 'deviceId': len(device_lst), 'deviceType': device_type,
                               'deviceName': device_name, 'deviceCurrVal': device_curr_val,
                               'timestamp': device_curr_time})
    return {'devices': device_lst}


@app.route('/login/user', methods= ["GET"])
def verify_login():
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
    # List containing 2 lambda functions, one to get rand int, one for rand char
    rand_char = [lambda: random.choice(string.ascii_lowercase), lambda: random.randint(0, 9)]
    while True:  # keeps on looping until finds a unique api key
        api_key = ""
        for i in range(APIKEY_LENGTH):  # generate random values
            api_key += str(random.choice(rand_char)())
        data_base_api_key = db["user_data"].find_one({"api_key":api_key,"email":email})
        if data_base_api_key is None:
            new_data={"email": email,
                      "api_key": api_key,
                      "nodes": [],
                      "devices": []}
            db["user_data"].insert_one(new_data)
            # Send an email to the user, containing the API key
            send_email(EMAIL_NOTIFICATION_SUBJECT, EMAIL_NOTIFICATION_TEXT + api_key, email)
            break


@app.route('/api/<api_key>', methods=['GET'])
def fetch_devices(api_key):
    print("imhere")
    try:
        devices = get_user_nodes(api_key)
        print(devices)
        return devices
    except Exception:
        return {'devices': 'NoneFound'}




if __name__ == '__main__':
    app.run(debug=True)
