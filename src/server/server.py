import socket
import threading
from src.server import dataDecoding
from src.algorithms import detection

IP = socket.gethostbyname(socket.gethostname())
PORT = 5566
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"


def handle_client(conn, addr):
    model, model_names = detection.load_model()
    connected = True

    while connected:
        data = conn.recv(SIZE)
        dataDecoding.decode_video(conn, data, addr, model, model_names)

    conn.close()


def start_server():
    print("[STARTING] Server is starting...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"[LISTENING] Server is listening on {IP}:{PORT}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
