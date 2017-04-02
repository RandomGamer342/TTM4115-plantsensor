server_ip = "localhost"
server_port = "11037"

# Ideally a list for scalability, but this is fine for now
sensor1 = {
    "enabled": True,
    "max_threshold": 600, # Equivalent to putting the sensor straight into water
    "fake": True,
    "fake_max_threshold": 0.6,
    "fake_min_threshold": 0,
    "fake_timerate": 60*3 # Time it should take for the fake sensor to go from the max value to the minimum.
    }

sensor2 = {
    "enabled": False,
    "max_threshold": 600,  # Equivalent to putting the sensor straight into water
    "fake": True,
    "fake_max_threshold": 0.6,
    "fake_min_threshold": 0,
    "fake_timerate": 60*3 # Time it should take for the fake sensor to go from the max value to the minimum.
    }

sensors = [sensor1, sensor2]