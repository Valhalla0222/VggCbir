import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QHBoxLayout
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from SelectAndSearch import SelectAndSearch

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('基于内容的图像检索（CBIR）')
        self.setGeometry(100, 100, 1280, 720)
        self.setStyleSheet('background-color: #f5f5f5;')

        # 主容器和布局
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)

        # 标题
        title = QLabel('基于内容的图像检索（CBIR）')
        title_font = QFont('Arial', 28, QFont.Bold)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet('color: #333333;')
        main_layout.addWidget(title)

        # 介绍文字
        intro = QLabel(
            '点击“选择图片”→选择图片→点击“搜索”\n'
            '即可检索出10张最相关图片。'
        )
        intro_font = QFont('Arial', 20)
        intro.setFont(intro_font)
        intro.setAlignment(Qt.AlignCenter)
        intro.setStyleSheet('color: #555555;')
        main_layout.addWidget(intro)

        # 搜索组件
        search_layout = QHBoxLayout()
        search_layout.addStretch(1)
        search_widget = SelectAndSearch(self)
        search_layout.addWidget(search_widget)
        search_layout.addStretch(1)
        main_layout.addLayout(search_layout)

        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())