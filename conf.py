hostname = "localhost"
port = "1183"

device_id = "123456"

send_interval = 10

# Ideally a list for scalability, but this is fine for now
sensor1 = {
    "enabled": True,
    "id": "123123",
    "max_threshold": 600, # Equivalent to putting the sensor straight into water
    "fake": True,
    "fake_max_threshold": 0.6,
    "fake_min_threshold": 0,
    "fake_timerate": 60*3 # Time it should take for the fake sensor to go from the max value to the minimum.
    }

sensor2 = {
    "enabled": False,
    "id": "123321",
    "max_threshold": 600,  # Equivalent to putting the sensor straight into water
    "fake": True,
    "fake_max_threshold": 0.6,
    "fake_min_threshold": 0,
    "fake_timerate": 60*3 # Time it should take for the fake sensor to go from the max value to the minimum.
    }

sensors = [sensor1, sensor2]