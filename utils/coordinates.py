IMG_SIZE = 1024


def translate_bbox(bbox: tuple[float, float, float, float]) -> tuple[float, float, float, float]:
    """
    Translate the bbox from absolute left corner to relative centered coordinates
    :param bbox: tuple(x, y, w, h) (absolute; left corner)
    :return: tuple(x, y, w, h) (relative; centered)
    """
    top_left_x = bbox[0]
    top_left_y = bbox[1]
    absolute_w = bbox[2]
    absolute_h = bbox[3]

    relative_w = absolute_w / IMG_SIZE
    relative_h = absolute_h / IMG_SIZE

    relative_x = top_left_x / IMG_SIZE + relative_w / 2
    relative_y = top_left_y / IMG_SIZE + relative_h / 2

    return relative_x, relative_y, relative_w, relative_h


def revert_bbox(rx, ry, rw, rh) -> tuple[float, float, float, float]:
    """
    Revert the bbox from relative centered coordinates to absolute left corner
    """
    x = (rx - rw / 2) * IMG_SIZE
    y = (ry - rh / 2) * IMG_SIZE
    w = rw * IMG_SIZE
    h = rh * IMG_SIZE

    return x, y, w, h
