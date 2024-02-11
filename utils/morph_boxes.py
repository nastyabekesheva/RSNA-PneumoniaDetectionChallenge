import pandas as pd

from utils.iou_utils import iou, box_areas_utils


def empty_preds(s: str) -> bool:
    return pd.isna(s) or len(s) == 0


def str_to_boxes(s: str) -> list:  # return c,x,y,w,h
    if empty_preds(s):
        return []

    boxes = []
    n = len(s.split()) // 5
    for i in range(n):
        box = s.split()[i * 5:i * 5 + 5]
        boxes.append(list(map(float, box)))

    return boxes


def remove_empty_boxes(s: str) -> str:
    if empty_preds(s):
        return s

    n = len(s.split()) // 5
    data = s.split()
    for i in range(n):
        box = data[i * 5:i * 5 + 5]
        if float(box[2]) * float(box[3]) == 0:
            s = s.replace(' '.join(map(str, box)), '').strip()

    return s


def two_boxes_overlap(box1, box2) -> bool:
    return iou(box1, box2) > 0.3


def one_box_inside_another(box1, box2) -> bool:
    area1, area2, intersection, union = box_areas_utils(box1, box2)
    return intersection / area1 > 0.7 or intersection / area2 > 0.7


def merge_boxes(box1, box2) -> (float, float, float, float, float):  # c,x,y,w,h - bottom left corner (0,0)
    c1, x1, y1, w1, h1 = box1
    c2, x2, y2, w2, h2 = box2

    # average boxes coords
    return (c1 + c2) / 2, (x1 + x2) / 2, (y1 + y2) / 2, (w1 + w2) / 2, (h1 + h2) / 2


def detect_overlapping(s: str, type='both') -> bool:
    if empty_preds(s):
        return False

    n = len(s.split()) // 5
    for i in range(n):
        box1 = list(map(float, s.split()[i * 5:i * 5 + 5]))
        for j in range(n):
            if i == j:
                continue
            box2 = list(map(float, s.split()[j * 5:j * 5 + 5]))

            if type == 'both':
                if two_boxes_overlap(box1, box2) or one_box_inside_another(box1, box2):
                    return True
            elif type == 'overlap':
                if two_boxes_overlap(box1, box2) and not one_box_inside_another(box1, box2):
                    return True
            elif type == 'inside':
                if one_box_inside_another(box1, box2):
                    return True

    return False


def merge_overlapping(s: str) -> str:
    if empty_preds(s):
        return s

    boxes = str_to_boxes(s)

    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            if boxes[i] is None or boxes[j] is None:
                continue
            if two_boxes_overlap(boxes[i], boxes[j]) or \
                    one_box_inside_another(boxes[i], boxes[j]):
                boxes[i] = merge_boxes(boxes[i], boxes[j])
                boxes[j] = None

    return ' '.join([' '.join(map(str, c)) for c in boxes if c is not None]).strip()


def clean_predictions(predictionStrings: pd.Series) -> pd.Series:
    predictionStrings = predictionStrings.apply(remove_empty_boxes).apply(merge_overlapping)
    return predictionStrings
