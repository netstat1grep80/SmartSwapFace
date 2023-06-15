import os.path as osp
import subprocess
import sys

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

def open_image(image_path):
    try:
        # 根据操作系统的不同，使用不同的命令打开图片
        if sys.platform.startswith('darwin'):  # macOS
            subprocess.call(['open', image_path])
        elif sys.platform.startswith('win32'):  # Windows
            subprocess.call(['start', image_path], shell=True)
        else:  # Linux or other platforms
            subprocess.call(['xdg-open', image_path])
    except OSError as e:
        print(f"Failed to open image: {e}")
