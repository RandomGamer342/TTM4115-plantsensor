import conf
from sensors.sensor import Sensor
#rom sensors.fakesensor import FakeSensor
import paho.mqtt.client as mqtt
import json
import time
import threading
from sys import exit

# No pretty way to make a wrapper for this in a separate file
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected!")
        userdata.set()
    else:
        print("Cannot connect to server due to a configuration issue. ({})".format(mqtt.connack_string(rc)))
        print("Change the config and try again.")
        exit(1)

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Connection lost. Trying to connect again...")
        userdata.clear()
        # Handled by loop_start()
        #client.reconnect()
    else:
        print("Disconnected.")
        exit(0)

def sensor_reader(con, preparing, client, sensors):
    while True:
        con.wait()
        preparing.set()
        print("Preparing data...")
        for s in sensors:
            hum = s.read()
            payload = {"humidity": hum, "timestamp": time.time()}
            print("{}: {}".format(s.id, hum))
            client.publish("plantlife/sensors/{}/humidity".format(s.id), json.JSONEncoder().encode(payload), retain=True)
        preparing.clear()
        time.sleep(conf.send_interval)

def main():
    assert(0 < len(conf.sensors) <= 8)
    sensors = list()
    print("Welcome to the Plant-Life sensor system!")
    print("Initialising sensors...")
    for i in range(len(conf.sensors)):
        if conf.sensors[i].get("enabled"):
            sensors.append(Sensor(conf.sensors[i].get("id"), i, conf.sensors[i].get("max_threshold")))
    print("Sensors initialised!")
    print("Connecting to server...")
    mc = mqtt.Client(client_id=conf.device_id, clean_session=False)
    mc.on_connect = on_connect
    mc.on_disconnect = on_disconnect
    mc.connect(conf.hostname, conf.port, 3 * conf.send_interval)
    mc.loop_start()

    connected = threading.Event()
    mc.user_data_set(connected)

    preparing_message = threading.Event()

    sender = threading.Thread(target=sensor_reader, args=(connected, preparing_message, mc, sensors), daemon=True)
    sender.start()

    while True:
        inp = input("> ").strip().lower().split()

        if not inp:
            print("Please enter a command.")
        elif inp[0] == "exit":
            if connected.is_set():
                if preparing_message.is_set():
                    preparing_message.wait()
                #TODO: Wait for messages to actually be published
                mc.disconnect()
            else:
                exit(0)
        elif inp[0] == "help":
            print("Available commands:")
            print("help\t-\tShow this help text again.")
            print("exit\t-\tStop the sensor system and quit this program.")


if __name__ == "__main__":
    main()
