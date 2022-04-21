import cv2
import imutils
import pickle
import struct

WIDTH = 520
HEIGHT = 520
LOCAL_VIDEO_PATH = '../../assets/traffic.mp4'


def read_local_video(socket):
    vid = cv2.VideoCapture(LOCAL_VIDEO_PATH)

    while vid.isOpened():
        img, frame = vid.read()
        frame = imutils.resize(frame, width=WIDTH, height=HEIGHT)

        a = pickle.dumps(frame)
        message = struct.pack("Q", len(a)) + a
        socket.sendall(message)
