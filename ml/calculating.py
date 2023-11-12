from shapely.geometry import Polygon
from typing import List

'''Функция для определения находится ли каждый человек из списка в опасной зоне и площади пересечения
между ограничивающим прямоугольником и полигоном опасной зоны.'''
def object_in_danger(humans: List[List], danger_zone: List):
    results = []
    conf = []
    limit = 15
    for human in humans:
        result = False
        inter_area = calculate_intersection_area(human, danger_zone)
        if inter_area >= limit:
            result = True
        results.append(result)
        conf.append(inter_area)
    return results, conf

'''Функция для вычисления площади пересечения между ограничивающим прямоугольником и полигоном 
и процента площади пересечения.'''
def calculate_intersection_area(rectangle, polygon):
    rect_polygon = Polygon([(rectangle[0], rectangle[1]), (rectangle[2], rectangle[1]),
                            (rectangle[2], rectangle[3]), (rectangle[0], rectangle[3])])
    poly_polygon = Polygon(polygon)

    intersection_area = rect_polygon.intersection(poly_polygon).area
    rect_area = rect_polygon.area

    intersection_percentage = round(intersection_area / rect_area * 100)

    return intersection_percentage