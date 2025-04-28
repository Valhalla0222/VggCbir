import os
import time
from PyQt5.QtWidgets import (
    QWidget, QLineEdit, QPushButton, QHBoxLayout, QFileDialog,
    QGridLayout, QLabel, QVBoxLayout, QGraphicsDropShadowEffect
)
from PyQt5.QtGui import QPixmap, QFont, QIcon, QColor
from PyQt5.QtCore import Qt, QSize, QThread, pyqtSignal
from search import searchByVgg, getScores  # 确保search.py存在且路径正确

class SearchThread(QThread):
    result_ready = pyqtSignal(list, list)

    def __init__(self, path):
        super().__init__()
        self.path = path

    def run(self):
        im_ls = searchByVgg(self.path)
        scores = getScores()
        self.result_ready.emit(im_ls, scores)

class SelectAndSearch(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # 用来保存所有打开的结果窗口，防止被回收
        self.result_windows = []

        self.bg_color = '#fafafa'
        self.setStyleSheet(f'background-color: {self.bg_color};')

        # 输入框 + 按钮布局
        self.input_layout = QHBoxLayout()
        self.input_layout.setSpacing(20)

        # 文本框
        self.img_path = QLineEdit(self)
        self.img_path.setPlaceholderText('请选择要检索的图片...')
        self.img_path.setFont(QFont('Arial', 14))
        self.img_path.setFixedSize(600, 50)
        self.img_path.setStyleSheet("""
            QLineEdit {
                border: 2px solid #ccc;
                border-radius: 10px;
                padding: 10px;
            }
            QLineEdit:focus {
                border: 2px solid #66afe9;
            }
        """)
        self.input_layout.addWidget(self.img_path)

        # 选择图片按钮
        self.upload_btn = QPushButton('选择图片', self)
        self.setup_button(self.upload_btn, '#4CAF50', 'icon/upload.png')
        self.upload_btn.clicked.connect(self.img_choose)
        self.input_layout.addWidget(self.upload_btn)

        # 搜索按钮
        self.search_btn = QPushButton('搜索', self)
        self.setup_button(self.search_btn, '#2196F3', 'icon/search.png')
        self.search_btn.clicked.connect(self.enter)
        self.input_layout.addWidget(self.search_btn)

        # 主布局
        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(30)
        self.main_layout.addLayout(self.input_layout)
        self.setLayout(self.main_layout)

    def setup_button(self, button, color, icon_path):
        button.setFont(QFont('Arial', 18, QFont.Bold))
        button.setFixedSize(150, 50)
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border: none;
                border-radius: 10px;
            }}
            QPushButton:hover {{
                background-color: {self.adjust_color(color, 20)};
            }}
            QPushButton:pressed {{
                background-color: {self.adjust_color(color, -20)};
            }}
        """)
        if os.path.exists(icon_path):
            button.setIcon(QIcon(icon_path))
            button.setIconSize(QSize(24, 24))
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setOffset(0, 3)
        shadow.setColor(QColor(0, 0, 0, 150))
        button.setGraphicsEffect(shadow)

    def adjust_color(self, hex_color, amount=20):
        col = QColor(hex_color)
        r = min(max(col.red() + amount, 0), 255)
        g = min(max(col.green() + amount, 0), 255)
        b = min(max(col.blue() + amount, 0), 255)
        return f'rgb({r}, {g}, {b})'

    def img_choose(self):
        options = QFileDialog.Options()
        file, _ = QFileDialog.getOpenFileName(
            self, '选择图片', os.getcwd(),
            'Image Files (*.png *.jpg *.bmp *.jpeg)', options=options
        )
        if file:
            self.img_path.setText(file)

    def enter(self):
        path = self.img_path.text()
        if not path:
            return

        # 启动搜索线程
        self.search_thread = SearchThread(path)
        self.search_thread.result_ready.connect(self.show_results)
        self.search_thread.start()

    def show_results(self, im_ls, scores):
        """在新窗口中显示检索结果，并保存窗口引用防止被回收"""
        win = QWidget()
        self.result_windows.append(win)

        win.setWindowTitle('检索结果')
        win.setGeometry(200, 150, 1280, 720)
        win.setStyleSheet('background-color: #f8f9fa;')

        grid = QGridLayout()
        grid.setSpacing(25)

        # 原始查询图
        query_path = self.img_path.text()
        pix_query = QPixmap(query_path).scaled(360, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        orig_label = QLabel('被检索的图片')
        orig_label.setFont(QFont('Arial', 20, QFont.Bold))
        orig_label.setAlignment(Qt.AlignCenter)
        grid.addWidget(orig_label, 0, 0, 1, 5)

        img_label = QLabel()
        img_label.setPixmap(pix_query)
        img_label.setAlignment(Qt.AlignCenter)
        grid.addWidget(img_label, 1, 0, 1, 5)

        # 检索结果图
        for idx, (raw_path, score) in enumerate(zip(im_ls, scores)):
            # 解码 bytes 路径
            if isinstance(raw_path, (bytes, bytearray)):
                path = raw_path.decode('utf-8')
            else:
                path = raw_path

            row = 2 + (idx // 5) * 2
            col = idx % 5

            lbl_score = QLabel(f'相似度: {score:.2f}')
            lbl_score.setFont(QFont('Arial', 16))
            lbl_score.setAlignment(Qt.AlignCenter)
            grid.addWidget(lbl_score, row, col)

            # 直接用 QPixmap 加载并缩放
            pix = QPixmap(path).scaled(240, 140, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            img_lbl = QLabel()
            img_lbl.setPixmap(pix)
            img_lbl.setAlignment(Qt.AlignCenter)
            grid.addWidget(img_lbl, row + 1, col)

        win.setLayout(grid)
        win.show()
