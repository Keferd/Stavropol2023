import cv2
import numpy as np
from typing import List
from shapely.geometry import Polygon
from shapely.ops import nearest_points


def get_nested_level(lst):
    if isinstance(lst, list):
        return 1 + max(get_nested_level(item) for item in lst)
    else:
        return 0


def convert_from_normal(objects, width, height):
    objects = np.array(objects)
    converted_objects = np.round(objects * [width, height, width, height]).astype(int)
    return converted_objects.tolist()


def visualize_boxes(image_path, person_boxes, danger_zones, result):
    # Загрузить изображение
    image = cv2.imread(image_path)

    ids = result[0]
    conf = result[2]

    if get_nested_level(danger_zones) <= 2:
        danger_zones = [danger_zones]

    polygons_zone = []
    polygons_person = []
    # Отобразить каждую опасную зону
    for danger_zone in danger_zones:
        danger_zone_np = np.array([danger_zone], dtype=np.int32)
        cv2.polylines(image, [danger_zone_np], isClosed=True, color=(0, 255, 0), thickness=2)
        polygons_zone.append(Polygon(danger_zone))

    # Отобразить каждый бокс человека
    for i in range(len(person_boxes)):
        x1 = person_boxes[i][0]
        y1 = person_boxes[i][1]
        x2 = person_boxes[i][2]
        y2 = person_boxes[i][3]
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 255), 2)
        polygons_person.append(Polygon([[x1, y1], [x2, y1], [x2, y2], [x1, y2]]))
        cv2.putText(image, "ID:" + str(i) + " DZ:" + str(conf[i]) + "%", (x1 - 35, y1), cv2.FONT_HERSHEY_SIMPLEX,
                    0.7, (255, 255, 0), 2, cv2.LINE_4)

    for person in polygons_person:
        min_distance = float('inf')
        closest_zone = None

        for zone in polygons_zone:
            distance = person.distance(zone)
            if distance < min_distance:
                min_distance = distance
                closest_zone = zone

        if closest_zone is not None and min_distance != 0:
            person_point, zone_point = nearest_points(person, closest_zone)
            x1 = int(person_point.coords[0][0])
            y1 = int(person_point.coords[0][1])
            x2 = int(zone_point.coords[0][0])
            y2 = int(zone_point.coords[0][1])

            cv2.line(image, (x1, y1), (x2, y2), (255, 50, 50), 2)
            cv2.putText(image, str(round(min_distance)), (((x1 + x2) // 2) + 5, ((y1 + y2) // 2) + 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2, cv2.LINE_4)

    if any(c > 0.15 for c in conf):
        border_color = (0, 0, 255)  # Red
    elif any(0.1 <= c <= 0.15 for c in conf):
        border_color = (0, 255, 255)  # Yellow
    else:
        border_color = None

    if border_color is not None:
        border_thickness = 10
        image = cv2.copyMakeBorder(image, border_thickness, border_thickness, border_thickness,
                                   border_thickness,
                                   cv2.BORDER_CONSTANT, value=border_color)
            # Отобразить изображение
    # cv2.imshow('Danger Zone Visualization', image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    output_path = 'output.jpg'
    cv2.imwrite(output_path, image)

    return output_path
