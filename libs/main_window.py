import os

from PyQt5.QtCore import Qt, QDateTime, QDir, QUrl, QThreadPool
from PyQt5.QtGui import QTextBlockFormat, QPixmap
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QLineEdit, QPushButton, QVBoxLayout, QWidget, QFileDialog, \
    QDesktopWidget, QSizePolicy, QSpacerItem, QLabel, QTextEdit, QMessageBox, QGraphicsView, QGraphicsScene

from datetime import datetime
from libs.swap_face import SwapFace
import sys

from utils import open_image


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
        self.face_entry.setDisabled(False)
        self.face_entry.setText("")
        self.face_button_select = QPushButton("选择")
        self.face_button_select.clicked.connect(lambda: self.select_image("face"))

        # 创建参考图片文件路径输入框和选择按钮
        self.check_entry = QLineEdit()
        self.check_entry.setDisabled(False)
        self.check_entry.setPlaceholderText("当目标图片或者视频中出现多张人脸时，请选择一张图片作为目标参考图。")
        self.check_button_select = QPushButton("选择")
        self.check_button_select.clicked.connect(lambda: self.select_image("check"))

        # 创建脸部选择输入框和选择按钮
        self.to_entry = QLineEdit()
        self.to_entry.setDisabled(False)
        self.to_entry.setText("")
        self.to_button_select = QPushButton("选择")
        self.to_button_select.clicked.connect(lambda: self.select_image("to"))

        # 创建脸部选择输入框和选择按钮
        self.save_entry = QLineEdit()
        self.save_entry.setDisabled(False)
        self.save_entry.setText("")
        self.save_button_select = QPushButton("选择")
        self.save_button_select.clicked.connect(self.save_path)

        self.start_button = QPushButton("开始转换")
        self.start_button.setFixedHeight(50)
        self.start_button.setCursor(Qt.PointingHandCursor)
        self.start_button.clicked.connect(lambda: self.execute("start"))

        self.stop_button = QPushButton("停止转换")
        self.stop_button.setFixedHeight(50)
        self.stop_button.setCursor(Qt.PointingHandCursor)
        self.stop_button.clicked.connect(lambda: self.execute("stop"))

        # 设置按钮的样式表
        self.start_button.setStyleSheet('''
            QPushButton {
                background-color: transparent;
                border: none;
                color: #007AFF;
                padding: 10px 20px;
                font-size: 16px;
            }

            QPushButton:hover {
                background-color: rgba(0, 122, 255, 0.1);
            }

            QPushButton:pressed {
                background-color: rgba(0, 122, 255, 0.2);
            }
        ''')

        self.stop_button.setStyleSheet('''
            QPushButton {
                background-color: transparent;
                border: none;
                color: #FF3B30;
                padding: 10px 20px;
                font-size: 16px;
            }

            QPushButton:hover {
                background-color: rgba(255, 59, 48, 0.1);
            }

            QPushButton:pressed {
                background-color: rgba(255, 59, 48, 0.2);
            }
        ''')



        layout = {
            'face': {'h': QHBoxLayout(), 'spacer': QSpacerItem(sSize, sSize, QSizePolicy.Fixed, QSizePolicy.Preferred)},
            'check': {'h': QHBoxLayout(), 'spacer': QSpacerItem(sSize, sSize, QSizePolicy.Fixed, QSizePolicy.Preferred)},
            'to': {'h': QHBoxLayout(), 'spacer': QSpacerItem(sSize, sSize, QSizePolicy.Fixed, QSizePolicy.Preferred)},
            'save': {'h': QHBoxLayout(), 'spacer': QSpacerItem(sSize, sSize, QSizePolicy.Fixed, QSizePolicy.Preferred)},
            'text': {'h': QHBoxLayout(), 'spacer': QSpacerItem(sSize, sSize, QSizePolicy.Fixed, QSizePolicy.Preferred)},
            'start': {'h': QHBoxLayout(), 'spacer': QSpacerItem(sSize, sSize, QSizePolicy.Fixed, QSizePolicy.Preferred)},
            'stop': {'h': QHBoxLayout(), 'spacer': QSpacerItem(sSize, sSize, QSizePolicy.Fixed, QSizePolicy.Preferred)},
            'image_view': {'h': QHBoxLayout(), 'spacer': QSpacerItem(sSize, sSize, QSizePolicy.Fixed, QSizePolicy.Preferred)}
        }

        # 创建水平布局并添加控件
        layout['face']['h'].addWidget(QLabel("1.人脸图片："))
        layout['face']['h'].addWidget(self.face_entry)
        layout['face']['h'].addSpacerItem(layout['face']['spacer'])
        layout['face']['h'].addWidget(self.face_button_select)


        # 创建水平布局并添加控件
        layout['to']['h'].addWidget(QLabel("2.原图/原视频："))
        layout['to']['h'].addWidget(self.to_entry)
        layout['to']['h'].addSpacerItem(layout['to']['spacer'])
        layout['to']['h'].addWidget(self.to_button_select)

        # 创建水平布局并添加控件
        layout['save']['h'].addWidget(QLabel("4.存储路径："))
        layout['save']['h'].addWidget(self.save_entry)
        layout['save']['h'].addSpacerItem(layout['save']['spacer'])
        layout['save']['h'].addWidget(self.save_button_select)

        # 创建水平布局并添加控件
        layout['check']['h'].addWidget(QLabel("3.目标人脸图片："))
        layout['check']['h'].addWidget(self.check_entry)
        layout['check']['h'].addSpacerItem(layout['check']['spacer'])
        layout['check']['h'].addWidget(self.check_button_select)


        # 创建水平布局并添加控件
        layout['start']['h'].addWidget(self.start_button)
        layout['start']['h'].addSpacerItem(layout['start']['spacer'])
        layout['start']['h'].addWidget(self.stop_button)

        # 创建四个 QGraphicsView 组件
        self.image_view_face = QGraphicsView()
        self.image_view_check = QGraphicsView()
        self.image_view_to = QGraphicsView()
        self.image_view_save = QGraphicsView()

        # 将点击事件处理函数与 QGraphicsView 组件关联
        self.image_view_save.mousePressEvent = self.createMousePressEvent(self.save_entry.text())


        # 创建水平布局并添加控件
        layout['image_view']['h'].addWidget(self.image_view_to)
        layout['image_view']['h'].addWidget(self.image_view_check)
        layout['image_view']['h'].addWidget(self.image_view_face)
        layout['image_view']['h'].addWidget(self.image_view_save)


        # 创建文本框组件
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(False)  # 设置为只读模式

        self.text_cursor = self.text_edit.textCursor()

        # 设置文本光标为结束位置，以便每次输出都在末尾
        # self.text_cursor.movePosition(QTextCursor.End)

        # 重定向标准输出到 text_edit
        sys.stdout = self

        # 创建水平布局并添加控件
        layout['text']['h'].addWidget(self.text_edit)



        # 创建垂直布局并添加水平布局
        v_layout = QVBoxLayout()

        v_layout.addLayout(layout['face']['h'])
        v_layout.setSpacing(1)
        v_layout.addLayout(layout['to']['h'])
        v_layout.setSpacing(1)
        v_layout.addLayout(layout['check']['h'])
        v_layout.setSpacing(1)
        v_layout.addLayout(layout['save']['h'])
        v_layout.setSpacing(1)

        v_layout.addLayout(layout['start']['h'])
        v_layout.setSpacing(1)
        v_layout.addLayout(layout['image_view']['h'])
        v_layout.setSpacing(1)
        v_layout.addLayout(layout['text']['h'], stretch=1)
        v_layout.setSpacing(1)

        v_layout.addStretch()  # 添加可伸展的空白部件





        # 创建主窗口的中心部件
        v_layout.addStretch()  # 添加可伸展的空白部件
        central_widget = QWidget()
        central_widget.setLayout(v_layout)
        self.setCentralWidget(central_widget)

        self.home_path = ""


    def execute(self, type):
        if type == 'start':
            face_path = self.face_entry.text()
            check_path = self.check_entry.text()
            to_path = self.to_entry.text()
            save_path = self.save_entry.text()
            err_msg = ""
            # 检查是否所有输入框都有值
            if not face_path:
                err_msg = "请选择要替换的脸[第一步]"
            # elif not check_path:
            #     err_msg = "请选择要被替换的脸"
            elif not to_path:
                err_msg = "请选择要被替换的图片或者视频路径[第二步]"
            elif not save_path:
                err_msg = "替换后存储路径[第四步]"
            else:
                self.start_button.setEnabled(False)
                swap = SwapFace()
                swap.run(face_path, to_path, check_path, save_path)
                self.start_button.setEnabled(True)
                self.image_view(self.save_entry.text(),"save")
            if err_msg != "":
                QMessageBox.warning(self, "提示", err_msg)

    def createMousePressEvent(self, image_path):
        def mousePressEvent(event):
            # 在自定义的 mousePressEvent 函数中访问 param 参数
            if event.button() == Qt.LeftButton and os.path.exists(image_path):
                print("打开 " + image_path)
                # 获取图片的本地路径
                local_path = os.path.abspath(image_path)
                # 打开默认的图片浏览器软件来查看图片
                # webbrowser.open(QUrl.fromLocalFile(local_path).toString())
                open_image(local_path)
            super(MainWindow, self).mousePressEvent(event)

        return mousePressEvent


    def image_view(self, image_path, image_viwe_name):
        scene = QGraphicsScene()
        pixmap = QPixmap(image_path)

        # 获取 QGraphicsView 的大小
        view_width = self.image_view_face.width()
        view_height = self.image_view_face.height()
        scaled_pixmap = pixmap.scaled(view_width - 10, view_height -10, Qt.AspectRatioMode.KeepAspectRatio)
        scene.addPixmap(scaled_pixmap)
        # 创建图形项并添加到场景中
        if image_viwe_name == "face":
            self.image_view_face.setScene(scene)
            self.image_view_face.setFixedSize(view_width, view_height)
            self.image_view_face.setSizeAdjustPolicy(QGraphicsView.AdjustToContents)
            self.image_view_face.mousePressEvent = self.createMousePressEvent(image_path)
        if image_viwe_name == "check":
            self.image_view_check.setScene(scene)
            self.image_view_check.setFixedSize(view_width, view_height)
            self.image_view_check.setSizeAdjustPolicy(QGraphicsView.AdjustToContents)
            self.image_view_check.mousePressEvent = self.createMousePressEvent(image_path)

        if image_viwe_name == "to":
            self.image_view_to.setScene(scene)
            self.image_view_to.setFixedSize(view_width, view_height)
            self.image_view_to.setSizeAdjustPolicy(QGraphicsView.AdjustToContents)
            self.image_view_to.mousePressEvent = self.createMousePressEvent(image_path)

        if image_viwe_name == "save":
            self.image_view_save.setScene(scene)
            self.image_view_save.setFixedSize(view_width, view_height)
            self.image_view_save.setSizeAdjustPolicy(QGraphicsView.AdjustToContents)
            self.image_view_save.mousePressEvent = self.createMousePressEvent(image_path)


    def select_image(self, type):
        if self.home_path == "":
            self.home_path = QDir.homePath()

        filepath, _ = QFileDialog.getOpenFileName(
            self,
            "选择图片",
            self.home_path,
            "图片文件 (*.jpg *.jpeg *.png);;视频文件 (*.mp4 *.avi *.mov)")
        if filepath:
            if type == 'face':
                self.face_entry.setText(filepath)
            elif type == 'check':
                self.check_entry.setText(filepath)
            elif type == 'to':
                self.to_entry.setText(filepath)
            self.home_path = os.path.dirname(filepath)
            self.image_view(filepath, type)

    def save_path(self):
        if self.home_path == "":
            self.home_path = QDir.homePath()

        save_pic = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath, _ = QFileDialog.getSaveFileName(
            self, "保存的文件", self.home_path + "/" + save_pic, "图片文件 (*.png *.jpg *.jpeg);"
        )
        if filepath:
                self.save_entry.setText(filepath)
                self.home_path =os.path.dirname(filepath)

    def write(self, text):
        # 获取当前日期和时间
        current_datetime = QDateTime.currentDateTime().toString("yyyy-MM-dd HH:mm:ss")

        # 设置文本块的格式
        block_format = QTextBlockFormat()
        block_format.setNonBreakableLines(False)
        self.text_cursor.setBlockFormat(block_format)
        if len(text) == 1 and (ord(text) != 10 and text != " "):
            self.text_cursor.insertText(f"[{current_datetime}] {text}\n")
        elif len(text) > 1:
            self.text_cursor.insertText(f"[{current_datetime}] {text}\n")
        self.text_edit.ensureCursorVisible()

    def flush(self):
        # 刷新文本编辑框
        pass

