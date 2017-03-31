import conf
from sensors.sensor import Sensor
#rom sensors.fakesensor import FakeSensor

def main():
    assert(conf.sensor1_enabled or conf.sensor2_enabled)
    if conf.sensor1_enabled:
        #if conf.sensor1_fake:

        #else:"
        sens1 = Sensor(conf.sensor1_gpio_pin)

    # if conf.sensor2_enabled:
    #     #if conf.sensor1_fake:
    #
    #     #else:"
    #     sens1 = Sensor(conf.sensor1_gpio_pin)

    while True:
        i = input("Read sensor data?")
        if int(i) == 1:
            print(sens1.read())
        elif int(i) == 0:
            break


if __name__ == "__main__":
    main()