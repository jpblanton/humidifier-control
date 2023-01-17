import argparse
import atexit

import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO

# need to pass client?
# double check method
def cleanup(client):
    GPIO.cleanup()
    client.loop_stop()
    print("Cleaned up")


def on_message(client, userdata, message):
    payload = message.payload
    # if payload True, turn it on
    # add arg to this function with pin number?
    if payload == b'True':
        GPIO.output(5, GPIO.LOW)
    elif payload == b'False':
        GPIO.output(5, GPIO.HIGH)

def mqtt_connect(topic, host):
    client = mqtt.Client()
    client.connect(host, 1883) #make opt arg
    client.subscribe(topic)
    return client

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    #TODO: this should be one integer
    parser.add_argument('--pin', type=int, required=True, help='Integer number of humidifier control pin')
    parser.add_argument('--topic', type=str, required=True, help='Topic for the script to subscribe to')
    parser.add_argument('--host', type=str, required=True, help='Hostname or IP of the MQTT broker')
    args = parser.parse_args()

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(args.pin, GPIO.OUT)

    client = mqtt_connect(args.topic, args.host)
    client.on_message = on_message
    atexit.register(cleanup, client)
    client.loop_forever()
