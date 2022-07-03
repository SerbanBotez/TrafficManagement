import socket
import struct
import threading
from src.server import dataDecoding
from src.algorithms import detection, centroidTracker
from src.server import modelConfiguration
from src.database import setup
from omegaconf import OmegaConf

config = OmegaConf.load('config.yaml')
IP = socket.gethostbyname(socket.gethostname())
ADDR = (IP, config.SERVER.PORT)


def handle_client(conn, addr):
    model, model_names = detection.load_model()
    model = modelConfiguration.configure_model(model)
    ct = centroidTracker.CentroidTracker(max_disappeared=config.APP.DISSAPEARED_FRAMES_NR)
    connected = True

    influx_client = setup.get_database_connection()

    length_left = struct.unpack('Q', conn.recv(struct.calcsize('Q')))[0]
    client_type = conn.recv(length_left).decode('utf-8')
    # print(client_type)

    while connected:
        data = conn.recv(config.SERVER.PKG_SIZE)
        dataDecoding.decode_video(conn, data, addr, model, model_names, ct, influx_client, client_type)

    conn.close()


def start_server():
    print("[STARTING] Server is starting...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"[LISTENING] Server is listening on {IP}:{config.SERVER.PORT}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
