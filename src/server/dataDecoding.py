import cv2
import struct
import pickle
from src.algorithms import detection
from src.database import writeData
from omegaconf import OmegaConf

config = OmegaConf.load('config.yaml')
PAYLOAD_SIZE = struct.calcsize("Q")


def decode_video(conn, data, addr, model, model_names, ct, influx_client):
    while True:
        while len(data) < PAYLOAD_SIZE:
            packet = conn.recv(4 * config.SERVER.PKG_SIZE)  # 4K
            if not packet:
                break
            data += packet
        packed_msg_size = data[:PAYLOAD_SIZE]
        data = data[PAYLOAD_SIZE:]
        msg_size = struct.unpack("Q", packed_msg_size)[0]
        if msg_size < 100:
            data += conn.recv(4 * config.SERVER.PKG_SIZE)
            sensor_data = pickle.loads(data)
            writeData.write_sensor_data(influx_client, sensor_data)
            break

        while len(data) < msg_size:
            data += conn.recv(4 * config.SERVER.PKG_SIZE)
        frame_data = data[:msg_size]
        data = data[msg_size:]
        frame = pickle.loads(frame_data)

        frame = detection.detect(model, frame, model_names, ct, influx_client)

        cv2.imshow(f"RECEIVING VIDEO from {addr}", frame)
        key = cv2.waitKey(1) & 0xFF
        # key = cv2.waitKey(0)
        if key == ord('q'):
            break
