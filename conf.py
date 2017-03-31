server_ip = "localhost"
server_port = "11037"

# Ideally a list for scalability, but this is fine for now
sensor1_enabled = True
sensor1_gpio_pin = 2
sensor1_fake = True
sensor1_fake_max_threshold = 0.6
sensor1_fake_min_threshold = 0
sensor1_fake_timerate = 60*3 # Time it should take for the fake sensor to go from the max value to the minimum.

sensor2_enabled = True
sensor2_gpio_pin = 10
sensor2_fake = True
sensor2_fake_max_threshold = 0.6
sensor2_fake_min_threshold = 0
sensor2_fake_timerate = 60*3 # See above
