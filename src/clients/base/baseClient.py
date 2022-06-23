import socket
from omegaconf import OmegaConf

config = OmegaConf.load('../../../config.yaml')

IP = socket.gethostbyname(socket.gethostname())
ADDR = (IP, config.SERVER.PORT)


def start_base_client(data_reading_callback):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    print(f"[CONNECTED] Client connected to server at {IP}:{config.SERVER.PORT}")

    connected = True
    while connected:
        while True:
            data_reading_callback(client)
