import pickle
import struct
import imutils
from vidgear.gears import CamGear

# TODO add constants to a config file
WIDTH = 520
HEIGHT = 520
YOUTUBE_VIDEO = "https://www.youtube.com/watch?v=RQA5RcIZlAM"
OPTIONS = {
    "STREAM_RESOLUTION": "best",
    "CAP_PROP_FRAME_WIDTH": WIDTH,
    "CAP_PROP_FRAME_HEIGHT": HEIGHT,
    "CAP_PROP_FPS": 60,
}


def read_live_youtube_video(socket):
    stream = CamGear(
        source=YOUTUBE_VIDEO,
        stream_mode=True,
        logging=True,
        **OPTIONS
    ).start()

    while True:
        frame = stream.read()
        if frame is None:
            break

        frame = imutils.resize(frame, width=WIDTH, height=HEIGHT)

        a = pickle.dumps(frame)
        message = struct.pack("Q", len(a)) + a
        socket.sendall(message)

    stream.stop()
