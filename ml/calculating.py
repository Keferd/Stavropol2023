from shapely.geometry import Polygon
from typing import List
from utils import get_nested_level

def object_in_danger(humans: List[List], danger_zone: List):
    results = []
    conf = []
    limit = 15
    for human in humans:
        result = False
        if get_nested_level(danger_zone) > 2:
            for danger in danger_zone:
                inter_area = calculate_intersection_area(human, danger)
                if inter_area >= limit:
                    result = True
                results.append(result)
                conf.append(inter_area)
        else:
            inter_area = calculate_intersection_area(human, danger_zone)
            if inter_area >= limit:
                result = True
            results.append(result)
            conf.append(inter_area)

    return results, conf


def calculate_intersection_area(rectangle, polygon):
    rect_polygon = Polygon([(rectangle[0], rectangle[1]), (rectangle[2], rectangle[1]),
                            (rectangle[2], rectangle[3]), (rectangle[0], rectangle[3])])
    poly_polygon = Polygon(polygon)

    intersection_area = rect_polygon.intersection(poly_polygon).area
    rect_area = rect_polygon.area

    intersection_percentage = round(intersection_area / rect_area * 100)

    return intersection_percentage