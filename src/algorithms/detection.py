from time import time
import torch
import numpy as np
import cv2

YOLO_REPO_PATH = 'ultralytics/yolov5'
YOLO_LOCAL_REPO_PATH = '../models'
MODEL_NAME = 'yolov5x6'


def check_device():
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    return device


def load_model():
    # model = torch.hub.load(YOLO_LOCAL_REPO_PATH, MODEL_NAME, source='local', pretrained=True)
    model = torch.hub.load(YOLO_REPO_PATH, MODEL_NAME, source='github', pretrained=True)
    model_names = model.names
    return model, model_names


def score_frame(loaded_model, loaded_frame):
    loaded_model.to(check_device())
    loaded_frame = [loaded_frame]

    results = loaded_model(loaded_frame)
    labels, cord = results.xyxyn[0][:, -1], results.xyxyn[0][:, :-1]

    return labels, cord


def class_to_label(x, model_names):
    classes = model_names
    return classes[int(x)]


def plot_boxes(current_results, current_frame, model_names):
    labels, cord = current_results
    n = len(labels)
    x_shape, y_shape = current_frame.shape[1], current_frame.shape[0]
    for i in range(n):
        row = cord[i]
        if row[4] >= 0.3:
            x1, y1, x2, y2 = int(row[0] * x_shape), int(row[1] * y_shape), int(row[2] * x_shape), int(
                row[3] * y_shape)
            bgr = (0, 255, 0)
            cv2.rectangle(current_frame, (x1, y1), (x2, y2), bgr, 2)
            cv2.putText(current_frame, class_to_label(labels[i], model_names), (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                        bgr, 2)

    return current_frame


def detect(model, frame, model_names):
    start_time = time()
    results = score_frame(model, frame)
    frame = plot_boxes(results, frame, model_names)
    end_time = time()

    fps = 1 / np.round(end_time - start_time, 2)
    cv2.putText(frame, f'FPS: {int(fps)}', (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    return frame
