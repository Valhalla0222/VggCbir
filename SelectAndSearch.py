import os
import time
from PyQt5.QtWidgets import (
    QWidget, QLineEdit, QPushButton, QHBoxLayout, QFileDialog,
    QGridLayout, QLabel, QVBoxLayout, QGraphicsDropShadowEffect
)
from PyQt5.QtGui import QPixmap, QFont, QIcon, QColor
from PyQt5.QtCore import Qt, QSize
from PIL import Image, ImageQt
from search import searchByVgg, getScores  # 确保search.py存在

class SelectAndSearch(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.bg_color = '#fafafa'
        self.setStyleSheet(f'background-color: {self.bg_color};')

        # 输入框 + 按钮布局
        self.input_layout = QHBoxLayout()
        self.input_layout.setSpacing(20)

        # 文本框
        self.img_path = QLineEdit(self)
        self.img_path.setPlaceholderText('请选择要检索的图片...')
        self.img_path.setFont(QFont('Arial', 14))
        self.img_path.setFixedWidth(600)
        self.img_path.setFixedHeight(50)
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
        # 添加阴影效果
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setOffset(0, 3)
        shadow.setColor(QColor(0, 0, 0, 150))
        button.setGraphicsEffect(shadow)

    def adjust_color(self, hex_color, amount=20):
        # 调整颜色亮度
        col = QColor(hex_color)
        r = min(max(col.red() + amount, 0), 255)
        g = min(max(col.green() + amount, 0), 255)
        b = min(max(col.blue() + amount, 0), 255)
        return f'rgb({r}, {g}, {b})'

    def img_choose(self):
        options = QFileDialog.Options()
        file, _ = QFileDialog.getOpenFileName(
            self, '选择图片', os.getcwd(), 'Image Files (*.png *.jpg *.bmp *.jpeg)', options=options)
        if file:
            self.img_path.setText(file)

    def enter(self):
        path = self.img_path.text()
        if not path:
            return
        start = time.perf_counter()
        im_ls = searchByVgg(path)
        duration = time.perf_counter() - start
        print(f'检索时长: {duration:.3f}s')

        scores = getScores()
        self.show_results(path, im_ls, scores)

    def show_results(self, query_path, im_ls, scores):
        # 结果窗口
        result = QWidget()
        result.setWindowTitle('检索结果')
        result.setGeometry(200, 150, 1280, 720)
        result.setStyleSheet('background-color: #f8f9fa;')

        grid = QGridLayout()
        grid.setSpacing(25)

        # 原始查询图
        original = Image.open(query_path)
        original = original.resize((360, 200), Image.ANTIALIAS)
        op_qimage = ImageQt.ImageQt(original)
        op_pix = QPixmap.fromImage(op_qimage)

        orig_label = QLabel('被检索的图片')
        orig_label.setFont(QFont('Arial', 20, QFont.Bold))
        orig_label.setAlignment(Qt.AlignCenter)
        grid.addWidget(orig_label, 0, 0, 1, 5)

        img_label = QLabel()
        img_label.setPixmap(op_pix)
        img_label.setAlignment(Qt.AlignCenter)
        grid.addWidget(img_label, 1, 0, 1, 5)

        # 检索结果
        for idx, (img_path, score) in enumerate(zip(im_ls, scores)):
            row = 2 + idx // 5 * 2
            col = idx % 5

            lbl_score = QLabel(f'相似度: {score:.2f}')
            lbl_score.setFont(QFont('Arial', 16))
            lbl_score.setAlignment(Qt.AlignCenter)
            grid.addWidget(lbl_score, row, col)

            img = Image.open(img_path)
            img = img.resize((240, 140), Image.ANTIALIAS)
            qimg = ImageQt.ImageQt(img)
            pix = QPixmap.fromImage(qimg)
            img_lbl = QLabel()
            img_lbl.setPixmap(pix)
            img_lbl.setAlignment(Qt.AlignCenter)
            grid.addWidget(img_lbl, row + 1, col)

        result.setLayout(grid)
        result.show()
