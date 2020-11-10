from flask import Flask
import pymongo
app = Flask("__name__")
client = pymongo.MongoClient("mongodb://192.168.1.48:27017")
db = client['iospace']


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
            # Set the device fields
            try:
                device_curr_val = device_info['data']
                device_curr_time = device_info['date']
            except TypeError:
                device_curr_val = 0
                device_curr_time = 0
            # Append device json description to list
            device_lst.append({'nodeId': node_name, 'deviceId': len(device_lst), 'deviceType': device_type,
                               'deviceName': device_name, 'deviceCurrVal': device_curr_val, 'timestamp': device_curr_time})
    return {'devices': device_lst}


@app.route('/test', methods=['GET'])
def fetch_devices():
    devices = get_user_nodes('test')
    print(devices)
    return devices


if __name__ == '__main__':
    app.run(debug=True)