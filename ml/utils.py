import cv2
import numpy as np
from typing import List

def convert_from_normal(objects, width, height):
    objects = np.array(objects)
    converted_objects = np.round(objects * [width, height, width, height]).astype(int)
    return converted_objects.tolist()

def visualize_boxes(image_path, person_boxes, danger_zones):
    # Загрузить изображение
    image = cv2.imread(image_path)

    # Отобразить каждый бокс человека
    for person_box in person_boxes:
        cv2.rectangle(image, (person_box[0], person_box[1]), (person_box[2], person_box[3]), (0, 0, 255), 2)

    # Отобразить каждую опасную зону
    for danger_zone in danger_zones:
        danger_zone_np = np.array([danger_zone], dtype=np.int32)
        cv2.polylines(image, [danger_zone_np], isClosed=True, color=(0, 255, 0), thickness=2)


    # Отобразить изображение
    # cv2.imshow('Danger Zone Visualization', image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    output_path = 'output.jpg'
    cv2.imwrite(output_path, image)

    return output_path

