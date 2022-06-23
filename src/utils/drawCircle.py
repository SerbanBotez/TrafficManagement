import cv2


def draw(frame, objects):
    objects_number = 0
    for (objectID, centroid) in objects.items():
        # draw both the ID of the object and the centroid of the object on the output frame
        objects_number += 1
        text = "ID {}".format(objectID)
        cv2.putText(frame, text, (centroid[0] - 10, centroid[1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        cv2.circle(frame, (centroid[0], centroid[1]), 4, (0, 255, 0), -1)

    return objects_number
