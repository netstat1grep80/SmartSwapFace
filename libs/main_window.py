from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QLineEdit, QPushButton, QVBoxLayout, QWidget, QFileDialog, \
    QDesktopWidget, QSizePolicy, QSpacerItem, QLabel
from PyQt5.QtGui import QIcon
from libs import gol

from datetime import datetime
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        #占位符宽度
        sSize = 20
        self.setWindowTitle("Swap Face")


        # 获取屏幕尺寸
        screen_geometry = QDesktopWidget().screenGeometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()

        # 计算窗口尺寸
        window_width = screen_width // 3
        window_height = screen_height // 2

        # 计算窗口位置
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        # 设置窗口尺寸和位置
        self.setGeometry(x, y, window_width, window_height)

        # 创建脸部选择输入框和选择按钮
        self.face_entry = QLineEdit()
        self.face_entry.setDisabled(True)
        self.face_entry.setText("")
        self.face_button_select = QPushButton("选择")
        self.face_button_select.clicked.connect(lambda: self.select_image("face"))

        # 创建参考图片文件路径输入框和选择按钮
        self.check_entry = QLineEdit()
        self.check_entry.setDisabled(True)
        self.check_entry.setText("")
        self.check_button_select = QPushButton("选择")
        self.check_button_select.clicked.connect(lambda: self.select_image("check"))

        # 创建脸部选择输入框和选择按钮
        self.to_entry = QLineEdit()
        self.to_entry.setDisabled(True)
        self.to_entry.setText("")
        self.to_button_select = QPushButton("选择")
        self.to_button_select.clicked.connect(self.save_path)

        layout = {
            'face': {'h': QHBoxLayout(), 'spacer': QSpacerItem(sSize, sSize, QSizePolicy.Fixed, QSizePolicy.Preferred)},
            'check': {'h': QHBoxLayout(), 'spacer': QSpacerItem(sSize, sSize, QSizePolicy.Fixed, QSizePolicy.Preferred)},
            'to': {'h': QHBoxLayout(), 'spacer': QSpacerItem(sSize, sSize, QSizePolicy.Fixed, QSizePolicy.Preferred)},
        }

        # 创建水平布局并添加控件
        layout['face']['h'].addWidget(QLabel("进入的脸:"))
        layout['face']['h'].addWidget(self.face_entry)
        layout['face']['h'].addSpacerItem(layout['face']['spacer'])
        layout['face']['h'].addWidget(self.face_button_select)

        # 创建水平布局并添加控件
        layout['check']['h'].addWidget(QLabel("移出的脸:"))
        layout['check']['h'].addWidget(self.check_entry)
        layout['check']['h'].addSpacerItem(layout['check']['spacer'])
        layout['check']['h'].addWidget(self.check_button_select)

        # 创建水平布局并添加控件
        layout['to']['h'].addWidget(QLabel("存储路径:"))
        layout['to']['h'].addWidget(self.to_entry)
        layout['to']['h'].addSpacerItem(layout['to']['spacer'])
        layout['to']['h'].addWidget(self.to_button_select)

        # 创建垂直布局并添加水平布局
        v_layout = QVBoxLayout()
        v_layout.addLayout(layout['face']['h'])
        v_layout.setSpacing(1)
        v_layout.addLayout(layout['check']['h'])
        v_layout.setSpacing(1)
        v_layout.addLayout(layout['to']['h'])
        v_layout.setSpacing(1)



        # 创建主窗口的中心部件
        v_layout.addStretch()  # 添加可伸展的空白部件
        central_widget = QWidget()
        central_widget.setLayout(v_layout)
        self.setCentralWidget(central_widget)

    def select_image(self, type):
        filepath, _ = QFileDialog.getOpenFileName(
            self,
            "选择图片",
            "/",
            "图片文件 (*.jpg *.jpeg *.png)")
        if filepath:
            if type == 'face':
                self.face_entry.setText(filepath)
            elif type == 'check':
                self.check_entry.setText(filepath)


    def save_path(self):
        save_pic = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath, _ = QFileDialog.getSaveFileName(
            self, "保存的文件", "./" + save_pic, "图片文件 (*.png *.jpg *.jpeg);"
        )
        if filepath:
                self.to_entry.setText(filepath)