import pickle
import struct
import time
import random

from omegaconf import OmegaConf

config = OmegaConf.load('../../../config.yaml')


def read_sensor_data(socket):
    weather_list = ['sunny', 'rainy', 'cloudy', 'thunderstorm', 'heavy_rain', 'snowy']

    while True:
        current_weather = random.choice(weather_list)
        current_temperature = random.randint(20, 22)
        if current_weather == 'snowy':
            current_temperature = '-10'
        sensor_data = {'weather': current_weather, 'temperature': current_temperature}
        data = {"source": 'sensor', 'data': sensor_data}
        a = pickle.dumps(data)
        message = struct.pack("q", len(a)) + a
        socket.sendall(message)
        time.sleep(1)
