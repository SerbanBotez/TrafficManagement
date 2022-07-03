import pickle
import struct
import imutils
from vidgear.gears import CamGear
from omegaconf import OmegaConf

config = OmegaConf.load('../../../config.yaml')
OPTIONS = {
    "STREAM_RESOLUTION": config.APP.SOURCES.YOUTUBE_VIDEO.OPTIONS.RESOLUTION,
    "CAP_PROP_FRAME_WIDTH": config.APP.SOURCES.YOUTUBE_VIDEO.OPTIONS.WIDTH,
    "CAP_PROP_FRAME_HEIGHT": config.APP.SOURCES.YOUTUBE_VIDEO.OPTIONS.HEIGHT,
    "CAP_PROP_FPS": config.APP.SOURCES.YOUTUBE_VIDEO.OPTIONS.FPS,
}


def read_live_youtube_video(socket):
    stream = CamGear(
        source=config.APP.SOURCES.YOUTUBE_VIDEO.PATH,
        stream_mode=True,
        logging=True,
        **OPTIONS
    ).start()

    data = 'youtube'
    encoded_data = data.encode('utf-8')
    socket.send(struct.pack('Q', len(encoded_data)))
    socket.send(bytes(encoded_data))

    while True:
        frame = stream.read()
        if frame is None:
            break

        frame = imutils.resize(frame, width=config.APP.FRAME.WIDTH, height=config.APP.FRAME.HEIGHT)

        a = pickle.dumps(frame)
        message = struct.pack("Q", len(a)) + a
        socket.sendall(message)

    stream.stop()
