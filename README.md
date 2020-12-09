# 3010_L2_M4    -----    IO SPACE

This repository contains all the code created for our SYSC 3010 Projet. Code used can be found in TeamProject Directory.

TeamProject/ClientAPI - The API clients will use
TeamProject/flask-backend - Web App backend, used to serve our web app
TeamProject/MQTTBackend - MQTT scripts, used by API and web app backend 
TeamProject/react-frontend - React web application

#Using IO Space
NOTE: IO Space web app is currently NOT deployed on a webserver. Although the front end works, back end is not currently
working!

Step 1: Visit http://198.91.181.118/  (Sorry didn't want to buy domain name)

Step 2: Scroll down to create a new user, enter your email and you should receieve an API key via email

Step 3: Navigate back to the main page then log in. You will be brought to the MyIOSpace page, containing 0 devices

Step 4: Clone This repository, it contains the client API

Step 5: create a new directory to hold your code

Step 6: Copy the TeamProject/ClientAPI directory to the newly created directory from step 5

Step 7: In CMD, navigate to your directory, and enter the following: `pip install -r ClientApi/requirements.txt`

##H1You are now ready to start making IoT devices!
From within the directory created in step 5 you can create as many python files as you want. And in order to use
our API, all you need to do is import it and enter your credentials. To make it easier, here's a template to follow
for sensors!

```
import iospaceAPI as api   # Import our API
ADDRESS = "198.91.181.118"  # This is OUR MQTT server address, don't change it unless we tell you to!

# Enter your credentials below, you will need an API key from our website before doing this!
NODE_NAME = "EnterYourNodeNameHere"
DEVICE_NAME = "EnterYourDeviceNameHere"

def sensor_function():
    # Write the code to read from your desired sensor here
    
    # ...
    return some_sensor_data  # Return the data so our API can use it  

sensor_dev = api.IOSpace(API_KEY, NODE_NAME, ADDRESS, DEVICE_NAME, sensor_function, debug=True)
random_device.start()
```

Here's a template for a controllable feedback device:
```
import iospaceAPI as api   # Import our API
ADDRESS = "198.91.181.118"  # This is OUR MQTT server address, don't change it unless we tell you to!

# Enter your credentials below, you will need an API key from our website before doing this!
NODE_NAME = "EnterYourNodeNameHere"
DEVICE_NAME = "EnterYourDeviceNameHere"

def feedback_function(api_key):
    # Write the code to control your sensor. api_key is a bool value that can be used to set your devices state
    
    # ...

# Now, in the line below we pass it feedback=True, meaining our API expects a feedback function (1 param)
sensor_dev = api.IOSpace(API_KEY, NODE_NAME, ADDRESS, DEVICE_NAME, feedback_function, feedback=True debug=True)
random_device.start()
```