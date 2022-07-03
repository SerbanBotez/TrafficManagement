import cv2
import imutils
import pickle
import struct
from omegaconf import OmegaConf

config = OmegaConf.load('../../../config.yaml')


def read_local_video(socket):
    vid = cv2.VideoCapture(config.APP.SOURCES.LOCAL_VIDEO.PATH)

    data = 'local'
    encoded_data = data.encode('utf-8')
    socket.send(struct.pack('Q', len(encoded_data)))
    socket.send(bytes(encoded_data))

    while vid.isOpened():
        img, frame = vid.read()
        frame = imutils.resize(frame, width=config.APP.FRAME.WIDTH, height=config.APP.FRAME.HEIGHT)
        a = pickle.dumps(frame)
        message = struct.pack("Q", len(a)) + a
        socket.sendall(message)
