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