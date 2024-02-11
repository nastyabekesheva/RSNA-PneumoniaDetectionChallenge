def box_areas_utils(box1, box2):  # corner coords
    _, left_x1, left_y1, w1, h1 = box1
    _, left_x2, left_y2, w2, h2 = box2

    assert w1 * h1 * w2 * h2 > 0, 'w or h is 0'

    right_x1, right_x2 = left_x1 + w1, left_x2 + w2
    top_y1, top_y2 = left_y1 + h1, left_y2 + h2

    area1, area2 = w1 * h1, w2 * h2
    right_xi = min(right_x1, right_x2)
    left_xi = max(left_x1, left_x2)
    top_yi = min(top_y1, top_y2)
    bottom_yi = max(left_y1, left_y2)

    if right_xi <= left_xi or top_yi <= bottom_yi:
        intersection = 0
    else:
        intersection = (right_xi - left_xi) * (top_yi - bottom_yi)

    union = area1 + area2 - intersection
    return area1, area2, intersection, union


def iou(box1, box2):
    area1, area2, intersection, union = box_areas_utils(box1, box2)
    return intersection / union