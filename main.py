import sys
import time
import random
from Adafruit_IO import MQTTClient
from simple_ai import*

AIO_FEED_ID = ["nutnhan1", "nutnhan2"]
AIO_USERNAME = "thorfinn0330"
AIO_KEY = "aio_TXHm96YJ2aIQKvRjvyqOA4bbQD9L"

def connected(client):
    print("Connected successfully")
    for topic in AIO_FEED_ID:
        client.subscribe(topic)

def subcribe(client, userdata, mid, granted_qos):
    print("Subscribed successfully")

def disconnected(client):
    print("Disconnected...")
    sys.exit(1)

def message(client, feed_id, payload):
    print("Received: " + payload + " , feed id: " + feed_id)

client = MQTTClient(AIO_USERNAME, AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subcribe
client.connect()
client.loop_background()

counter = 10
detect_counter = 5
ai_result =""
pre_ai_result =""

while True:
    counter = counter - 1
    if counter <= 0:
        print("Data is publishing....")
        temp = random.randint(10, 30)
        client.publish("cambien1", temp)
        light = random.randint(100, 500)
        client.publish("cambien2", light)
        humi = random.randint(30, 60)
        client.publish("cambien3", humi)
        counter = 10
    detect_counter = detect_counter - 1
    if detect_counter <= 0:
        detect_counter = 5
        pre_ai_result = ai_result
        ai_result = image_detector()
        print("AI Result:", ai_result)
        if ai_result != pre_ai_result:
            client.publish("ai", ai_result)

    time.sleep(1)
    
