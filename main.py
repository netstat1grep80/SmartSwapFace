import insightface
import os
import sys
from libs import gol

import argparse
import numpy as np
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon

from libs.main_window import MainWindow
from datetime import datetime
from insightface.app import FaceAnalysis
assert insightface.__version__>='0.7'

__ROOT__ = os.path.split(os.path.realpath(__file__))[0]
__ICON_PATH__ = __ROOT__ +  os.sep + 'resource' + os.sep + 'w.ico'


gol.__init()
gol.set_value('__ROOT__', __ROOT__)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(__ICON_PATH__))
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

    """
    start = time.time()

    # os.environ['CUDA_VISIBLE_DEVICES'] = '2, 3'
    parser = argparse.ArgumentParser()


    parser.add_argument(
        '--swap_from',
        type=str,
        default='/Users/laozhang/Pictures/aitest/明星/wangbaoqiang.png',
        help="从这张图片中提取脸部"
    )

    parser.add_argument(
        '--swap_to',
        type=str,
        default='/Users/laozhang/Downloads/maxresdefault.jpeg',
        help="将此图片的脸替换掉"
    )

    parser.add_argument(
        '--swap_dst',
        type=str,
        default='/Users/laozhang/Pictures/aitest/明星/zhourunfa.jpeg',
        help="将此图片的脸替换掉"
    )

    #python /Users/laozhang/projects/python/src/insightface/examples/in_swapper/single.py --swap_from=/Users/laozhang/Pictures/aitest/明星/wangbaoqiang.png  --swap_to=/Users/laozhang/Pictures/aitest/明星/zhourunfa.jpeg
    # getting the current date and time
    current_datetime = datetime.now()
    parser.add_argument(
        '--output',
        type=str,
        default='./' +  current_datetime.strftime("%Y%m%d_%H%M%S") + '.png',
        help="最终成片"
    )
    args = parser.parse_args()

    if args.swap_from == "":
        raise "--swap_from参数不能为空"

    if args.swap_to == "":
        raise "--swap_to参数不能为空"

    app = FaceAnalysis(name='buffalo_l')
    app.prepare(ctx_id=0, det_size=(353, 512))

    swapper = insightface.model_zoo.get_model('inswapper_128.onnx', download=True, download_zip=True)

    img1 = get_my_image(args.swap_to)
    faces1 = app.get(img1)


    img2 = get_my_image(args.swap_from)
    faces2 = app.get(img2)

    img_dst = get_my_image(args.swap_dst)
    faces_dst = app.get(img_dst)

    res = img1.copy()

    faces = []
    for face1 in faces1:
        feat1 = face1.embedding
        feat2 = faces_dst[0].embedding
        sim = np.linalg.norm(feat1 - feat2)
        faces.append(sim)


    if len(faces) >0 :
        min_index = faces.index(min(faces))
        res = swapper.get(res, faces1[min_index], faces2[0], paste_back=True)
    cv2.imwrite(args.output, res)
    end = time.time()
    print('CPU执行时间: ', end - start)
    """
