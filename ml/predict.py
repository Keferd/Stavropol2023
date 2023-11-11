from typing import List, Optional, Dict
import os

from ultralytics import YOLO
from ensemble_boxes import *

from dangers_dict import ALL_DANGERS_COORDS
from calculating import object_in_danger
from utils import convert_from_normal, visualize_boxes


def restructure_preds(yolo_pred):
    """
    Формирует предскзаания моделей в необходимом формате:
    [координаты bbox, уверенность в предсказаниях, предсказанные лейблы]
    :param yolo_pred: возвращаемое значение функции predict_one_model, содержит всю информацию о предсказании моделью
    :return:
    """
    boxes_list, scores_list, labels_list = list(), list(), list()

    for object_ in yolo_pred[0].boxes:
        boxes_list.extend(object_.xyxyn.tolist())
        scores_list.extend(object_.conf.tolist())
        labels_list.extend(object_.cls.tolist())

    return boxes_list, scores_list, labels_list


def ensemble_boxes(
        models: List[YOLO],
        path_to_image: str,
        weights: Optional[List[float]] = None,
        run_type: str = 'wbf',
        iou_thr: float = 0.5,
        skip_box_thr: float = 0.0001,
        sigma: float = 0.1
):
    """
    Данная функция усредняет предсказания модели по боксам, исходя из ряда параметров
    param models: массив моделей, которые будут делать предсказание
    param path_to_image: путь до изображения для предсказания
    param weights: значимость каждой модели в ансамбле
    param run_type: тип усреднения
    param iou_thr: значение iou в совпадении полей
    param skip_box_thr: минимальная уверенность модели в предсказании
    param sigma:
    """
    if weights is None:
        weights = [1 for _ in range(len(models))]

    boxes_, scores_, labels_ = [], [], []
    for model in models:
        yolo_model_predict = model.predict(path_to_image, save_conf=True, seed=42)
        boxes_list, scores_list, labels_list = restructure_preds(yolo_model_predict)

        boxes_.append(boxes_list)
        scores_.append(scores_list)
        labels_.append(labels_list)

    if run_type == 'wbf':
        boxes, scores, labels = weighted_boxes_fusion(
            boxes_,
            scores_,
            labels_,
            weights=weights,
            iou_thr=iou_thr,
            skip_box_thr=skip_box_thr
        )

    elif run_type == 'soft_nms':
        boxes, scores, labels = soft_nms(
            boxes_,
            scores_,
            labels_,
            weights=weights,
            iou_thr=iou_thr,
            sigma=sigma,
            thresh=skip_box_thr
        )

    elif run_type == 'nms':
        boxes, scores, labels = nms(
            boxes_,
            scores_,
            labels_,
            weights=weights,
            iou_thr=iou_thr
        )

    elif run_type == 'non_maximum_weighted':
        boxes, scores, labels = non_maximum_weighted(
            boxes_,
            scores_,
            labels_,
            weights=weights,
            iou_thr=iou_thr,
            skip_box_thr=skip_box_thr
        )

    else:
        raise NotImplementedError(f"{run_type} type method for ensembling boxes is not implemented. Available "
                                  f"methods: ['nms', 'soft_nms', 'non_maximum_weighted', 'wbf']")

    return boxes, scores, labels


def predict(danger_zone_name, path_to_image):
    directory = 'cameras/' + danger_zone_name
    danger_zone = ALL_DANGERS_COORDS[danger_zone_name]
    image_extensions = ['.jpg', '.jpeg', '.png']
    # image_list = [os.path.join(directory, file) for file in os.listdir(directory) if
    #               os.path.splitext(file)[1].lower() in image_extensions]
    # path_to_image = image_list[0]
    model = YOLO('runs/detect/yolov8n_custom8/weights/best.pt')
    models = [model]
    weights = [1]
    humans, scores, labels = ensemble_boxes(
        models=models,
        path_to_image=path_to_image,
        weights=weights
    )

    humans = convert_from_normal(humans, width=1280, height=720)
    print(object_in_danger(humans, danger_zone[0]))

    visualize_boxes(path_to_image, humans, [danger_zone[0]])

if __name__ == '__main__':
    danger_zone_name = 'Spp-K1-1-2-6'
    directory = 'cameras/' + danger_zone_name
    danger_zone = ALL_DANGERS_COORDS[danger_zone_name]
    image_extensions = ['.jpg', '.jpeg', '.png']
    image_list = [os.path.join(directory, file) for file in os.listdir(directory) if
                  os.path.splitext(file)[1].lower() in image_extensions]
    path_to_image = image_list[0]
    model = YOLO('runs/detect/yolov8n_custom8/weights/best.pt')
    models = [model]
    weights = [1]
    humans, scores, labels = ensemble_boxes(
        models=models,
        path_to_image=path_to_image,
        weights=weights
    )


    humans = convert_from_normal(humans, width=1280, height=720)
    print(object_in_danger(humans, danger_zone[0]))

    visualize_boxes(path_to_image, humans,[danger_zone[0]])