import socket
import threading
from src.server import dataDecoding
from src.algorithms import detection, centroidTracker
from src.server import modelConfiguration
from omegaconf import OmegaConf

config = OmegaConf.load('config.yaml')
IP = socket.gethostbyname(socket.gethostname())
ADDR = (IP, config.SERVER.PORT)


def handle_client(conn, addr):
    model, model_names = detection.load_model()
    model = modelConfiguration.configure_model(model)
    ct = centroidTracker.CentroidTracker(max_disappeared=20)
    connected = True

    while connected:
        data = conn.recv(config.SERVER.PKG_SIZE)
        dataDecoding.decode_video(conn, data, addr, model, model_names, ct)

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
