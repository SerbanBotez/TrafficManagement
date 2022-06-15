# algorithm based on the tutorial found at https://pyimagesearch.com/2018/07/23/simple-object-tracking-with-opencv/
import numpy as np
from scipy.spatial import distance as dist
from collections import OrderedDict


class CentroidTracker:
    def __init__(self, max_disappeared):
        self.x = 0
        self.nextObjectID = 0
        self.objects = OrderedDict()
        self.disappeared = OrderedDict()
        self.maxDisappeared = max_disappeared

    def register(self, centroid):
        self.objects[self.nextObjectID] = centroid
        self.disappeared[self.nextObjectID] = 0
        self.nextObjectID += 1

    def deregister(self, object_id):
        del self.objects[object_id]
        del self.disappeared[object_id]

    def update(self, rectangles):
        self.x = 0
        if len(rectangles) == 0:
            for object_id in list(self.disappeared.keys()):
                self.disappeared[object_id] += 1

                if self.disappeared[object_id] > self.maxDisappeared:
                    self.deregister(object_id)

            return self.objects

        input_centroids = np.zeros((len(rectangles), 2), dtype="int")

        for (i, (startX, startY, endX, endY)) in enumerate(rectangles):
            cx = int((startX + endX) / 2.0)
            cy = int((startY + endY) / 2.0)
            input_centroids[i] = (cx, cy)

        if len(self.objects) == 0:
            for i in range(0, len(input_centroids)):
                self.register(input_centroids[i])
        else:
            object_ids = list(self.objects.keys())
            object_centroids = list(self.objects.values())

            distances_matrix = dist.cdist(np.array(object_centroids), input_centroids, 'euclidean')
            rows = distances_matrix.min(axis=1, initial=None).argsort()

            cols = distances_matrix.argmin(axis=1)[rows]

            used_rows = set()
            used_cols = set()

            for (row, col) in zip(rows, cols):
                if row in used_rows or col in used_cols:
                    continue
                object_id = object_ids[row]
                self.objects[object_id] = input_centroids[col]
                self.disappeared[object_id] = 0

                used_rows.add(row)
                used_cols.add(col)

            unused_rows = set(range(0, distances_matrix.shape[0])).difference(used_rows)
            unused_cols = set(range(0, distances_matrix.shape[1])).difference(used_cols)

            if distances_matrix.shape[0] >= distances_matrix.shape[1]:
                for row in unused_rows:
                    object_id = object_ids[row]
                    self.disappeared[object_id] += 1

                    if self.disappeared[object_id] > self.maxDisappeared:
                        self.deregister(object_id)
            else:
                for col in unused_cols:
                    self.register(input_centroids[col])
        return self.objects
