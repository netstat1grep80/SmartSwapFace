import os.path as osp
import cv2

def load_fit_image(img):
    w, h, _ = img.shape
    if w > h:
        rate = 512 / w
    else:
        rate = 512 / h

    w = int(w * rate)
    h = int(h * rate)

    img = cv2.resize(img, (h, w), interpolation=cv2.INTER_CUBIC)

    return img


def get_my_image(image_file, resize=True):
    if osp.exists(image_file):
        image_file = image_file
    else:
        assert image_file is not None, '%s not found'%image_file
    img = cv2.imread(image_file)
    if resize is True:
        return load_fit_image(img)
    return img
