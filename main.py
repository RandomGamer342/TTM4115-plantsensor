import conf
from sensors.sensor import Sensor
from sensors.fakesensor import FakeSensor
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

def on_publish(client, userdata, mid):
    client.user_data_set([userdata[0], userdata[1], userdata[2] - 1])
    if userdata[2] - 1 == 0:  # assume userdata does not get updated by above
        userdata[1].set() # naively assume that 0 readied messages equals all messages being published

def sensor_reader(con, ready, sent, client, sensors):
    timer = threading.Timer(0, ready.set)
    timer.start()
    while True:
        con.wait()
        sent.wait()
        ready.wait()
        if timer.is_alive():
            timer.cancel()
        print("Preparing data...")
        sent.clear()
        client.user_data_set([con, sent, len(sensors)])
        for s in sensors:
            hum = s.read()
            tim = time.time()
            payload = {"humidity": hum, "timestamp": tim}
            print("{}: {} - {}".format(tim, s.id, hum))
            client.publish("plantlife/sensors/{}/humidity".format(s.id), json.JSONEncoder().encode(payload), retain=True)
        ready.clear()
        timer = threading.Timer(conf.send_interval, ready.set)
        timer.start()

def main():
    assert(0 < len(conf.sensors) <= 8)
    sensors = list()
    print("Welcome to the Plant-Life sensor system!")
    print("Initialising sensors...")
    for i in range(len(conf.sensors)):
        s = conf.sensors[i]
        if s.get("enabled"):
            if s.get("fake"):
                sensors.append(FakeSensor(s.get("id"), s.get("fake_good_threshold"), s.get("fake_timerate")))
            else:
                sensors.append(Sensor(s.get("id"), i, s.get("max_threshold")))
    print("Sensors initialised!")
    print("Connecting to server...")
    mc = mqtt.Client(client_id=conf.device_id, clean_session=False)
    mc.on_connect = on_connect
    mc.on_disconnect = on_disconnect
    mc.connect(conf.hostname, conf.port, 3 * conf.send_interval)
    mc.loop_start()

    connected = threading.Event()

    ready = threading.Event()

    sent = threading.Event()
    sent.set()

    mc.user_data_set([connected, sent, 0])

    sender = threading.Thread(target=sensor_reader, args=(connected, ready, sent, mc, sensors), daemon=True)
    sender.start()

    while True:
        inp = input("> ").strip().lower().split()

        if not inp:
            print("Please enter a command.")
        elif inp[0] == "exit":
            if connected.is_set():
                sent.wait()
                mc.disconnect()
            else:
                exit(0)
        elif inp[0] == "update":
            ready.set()
        elif inp[0] == "sensors":
            for i in range(len(sensors)):
                s = sensors[i]
                print("{}[{}]Sensor {}: {}".format(
                    "[FAKE]" if s is FakeSensor else "",
                    i,
                    s.id,
                    s.read()
                ))
        elif inp[0] == "water":  # Huge mess
            if len(inp) < 2:
                print("Please enter a sensor number!\t(water <sensor number> <humidity>)")
            try:
                id = int(inp[1])
                if id < 0 or id >= len(sensors):
                    print("Please enter a valid sensor number, between 0 and {}. Hint: Use the sensors command.".format(
                        len(sensors) - 1
                    ))
                elif not sensors[id]["fake"]:
                    print("Sensor", id, "is not fake. You will have to water this plant yourself!")
                else:
                    fraction = None
                    if len(inp) > 2:
                        fraction = float(inp[2])
                    if fraction is not None and (fraction < 0 or fraction > 1):
                        print("Please enter a valid fraction for humidity between 0 and 1")
                    else:
                        print("Watered plant to humidity {}.".format(sensors[id].water(fraction)))

            except ValueError:
                print("Please enter valid numbers for sensor/fraction!\t(water <sensor number> <humidity>)")
        elif inp[0] == "help":
            print("Available commands:")
            print("help\t-\tShow this help text again.")
            print("update\t-\tSend a sensor update right now, skipping the usual delay.")
            print("sensors\t-\tPrint information about existing sensors.")
            print("water <sensor number> <humidity>\t-\tWater the plant to specified fraction of humidity.",
                  "If humidity is unspecified, default to the good threshold. Only relevant for fake sensors.")
            print("exit\t-\tStop the sensor system and quit this program.")
        else:
            print("Invalid command. Hint: Use the help command.")


if __name__ == "__main__":
    main()
