import conf
from sensors.sensor import Sensor
#rom sensors.fakesensor import FakeSensor

def main():
    assert(0 < len(conf.sensors) <= 8)
    sensors = list()
    for i in range(len(conf.sensors)):
        if conf.sensors[i].get("enabled"):
            sensors.append(Sensor(i))

    while True:
        i = input("Read sensor data?")
        if i == "1":
            for s in sensors:
                print(s.read())
        elif i == "0":
            break


if __name__ == "__main__":
    main()