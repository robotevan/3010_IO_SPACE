from flask import Flask
app = Flask("__name__")
import pymongo
from flask import request

client = pymongo.MongoClient("mongodb://192.168.1.48:27017")
db = client['iospace']



def get_devices(api_key):
    collection = db['user_data']
    doc = collection.find_one({'api_key': api_key})
    device_list = []
    curr_node = 0
    for lst in doc['devices']:
        for item in lst:
            device_type, device_name = item.split(":")
            device_id = len(device_list)
            device_list.append({'nodeId': curr_node, 'deviceId': device_id, 'deviceType': device_type,
                                'deviceName': device_name})
        curr_node += 1
    return ({'devices': device_list})


@app.route('/test', methods=['GET'])
def fetch_devices():
    print(request.args.get('ap'))
    devices = get_devices('test')
    return devices


if __name__ == '__main__':
    app.run(debug=True)