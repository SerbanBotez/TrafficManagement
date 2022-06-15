from time import time
import torch
import numpy as np
import cv2
from src.utils import drawCircle
from omegaconf import OmegaConf

config = OmegaConf.load('config.yaml')


def check_device():
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    return device


def load_model():
    # model = torch.hub.load(YOLO_LOCAL_REPO_PATH, MODEL_NAME, source='local', pretrained=True)
    model = torch.hub.load(config.REPO.PATH, config.MODEL.NAME, source='github', pretrained=True)
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


def plot_boxes(current_results, current_frame, model_names, ct):
    labels, cord = current_results
    n = len(labels)
    x_shape, y_shape = current_frame.shape[1], current_frame.shape[0]

    rectangles = []
    if n == 0:
        ct.update([])
    else:
        for i in range(n):
            row = cord[i]
            # confidence = format(row[4], ".2f")
            # print("Row: ", confidence, " ", class_to_label(labels[i], model_names))
            if row[4] >= 0.3 and class_to_label(labels[i], model_names) == "car" or row[4] >= 0.7 and class_to_label(
                    labels[i], model_names) != "car":
                x1, y1, x2, y2 = int(row[0] * x_shape), int(row[1] * y_shape), int(row[2] * x_shape), int(
                    row[3] * y_shape)

                rectangle_coordinate = np.array([x1, y1, x2, y2], dtype=np.int32)
                rectangles.append(rectangle_coordinate)

                cv2.rectangle(current_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                # cv2.putText(current_frame, class_to_label(labels[i], model_names) + " " + confidence, (x1, y1),
                #             cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                #             bgr, 2)
    objects = ct.update(rectangles)
    drawCircle.draw(current_frame, objects)

    return current_frame


def detect(model, frame, model_names, ct):
    start_time = time()
    results = score_frame(model, frame)
    frame = plot_boxes(results, frame, model_names, ct)
    end_time = time()

    fps = 1 / np.round(end_time - start_time, 2)
    cv2.putText(frame, f'FPS: {int(fps)}', (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    return frame
