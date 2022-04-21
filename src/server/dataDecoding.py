import cv2
import struct
import pickle
from src.algorithms import detection

PAYLOAD_SIZE = struct.calcsize("Q")
SIZE = 1024


def decode_video(conn, data, addr, model, model_names):
    while True:
        while len(data) < PAYLOAD_SIZE:
            packet = conn.recv(4 * SIZE)  # 4K
            if not packet:
                break
            data += packet
        packed_msg_size = data[:PAYLOAD_SIZE]
        data = data[PAYLOAD_SIZE:]
        msg_size = struct.unpack("Q", packed_msg_size)[0]

        while len(data) < msg_size:
            data += conn.recv(4 * SIZE)
        frame_data = data[:msg_size]
        data = data[msg_size:]
        frame = pickle.loads(frame_data)

        frame = detection.detect(model, frame, model_names)

        cv2.imshow(f"RECEIVING VIDEO from {addr}", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
