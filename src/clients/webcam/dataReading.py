import urllib
from urllib import request
import pickle
import struct
import cv2
import numpy as np
import imutils
from omegaconf import OmegaConf

config = OmegaConf.load('../../../config.yaml')


def read_live_cam(socket):
    while True:
        resp = urllib.request.urlopen(config.APP.SOURCES.WEB_CAMERA.PATH)
        frame = np.asarray(bytearray(resp.read()), dtype="uint8")
        frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
        frame = imutils.resize(frame, width=config.APP.FRAME.WIDTH, height=config.APP.FRAME.HEIGHT)

        a = pickle.dumps(frame)
        message = struct.pack("Q", len(a)) + a
        socket.sendall(message)
