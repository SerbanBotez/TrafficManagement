import urllib
from urllib import request
import pickle
import struct
import cv2
import numpy as np
import imutils

WIDTH = 520
HEIGHT = 520
CAMERA = "https://live.freecam.ro/live/iasi-hotel-unirea?d=1608366225652"


def read_live_cam(socket):
    while True:
        resp = urllib.request.urlopen(CAMERA)
        frame = np.asarray(bytearray(resp.read()), dtype="uint8")
        frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
        frame = imutils.resize(frame, width=WIDTH, height=HEIGHT)

        a = pickle.dumps(frame)
        message = struct.pack("Q", len(a)) + a
        socket.sendall(message)
