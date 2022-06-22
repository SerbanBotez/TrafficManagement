from omegaconf import OmegaConf

config = OmegaConf.load('../../../config.yaml')


def read_sensor_data(socket):
    while True:
        sensor_data = {'weather': 'sunny', 'temperature': 30}
        data = {"source": 'sensor', 'data': sensor_data}
        socket.sendall(data)
