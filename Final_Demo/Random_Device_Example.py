import random
import iospaceAPI as api

ADDRESS = "198.91.181.118"
NODE_NAME = "o_aa"
DEVICE_NAME = "random_device"
API_KEY = "658i685q44g1"


def random_number():
    return random.randint(0,10)


random_device = api.IOSpace(API_KEY,NODE_NAME,ADDRESS,False,DEVICE_NAME,random_number,debug=True)
random_device.start()

