import random
import iospaceAPI as api
from Lidar import Lidar
ADDRESS = "198.91.181.118"
NODE_NAME = "EvanNode"
DEVICE_NAME = "Lidar"
API_KEY = ""

lidar = Lidar()

def read_lidar():
    return lidar.read_distance();


random_device = api.IOSpace(API_KEY,NODE_NAME,ADDRESS,False,DEVICE_NAME, read_lidar, debug=True)
random_device.start()
