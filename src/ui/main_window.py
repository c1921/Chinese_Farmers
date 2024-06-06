import random
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea, QHBoxLayout, QListWidget, QListWidgetItem, QGroupBox, QGridLayout

from src.family import Family

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # 创建家庭
        self.families = [Family(f"Family {i+1}", random.randint(3, 6)) for i in range(5)]

        # 设置窗口
        self.setWindowTitle('Random Families Game')
        self.setGeometry(100, 100, 1200, 800)
        
        # 设置主布局
        main_layout = QHBoxLayout()

        # 左侧角色详细信息显示
        self.detail_label = QLabel()
        self.detail_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        font = QFont("assets/fonts/LXGWFasmartGothic.ttf", 12)
        self.detail_label.setFont(font)
        self.detail_label.setFixedWidth(300)

        # 创建家庭显示区
        self.family_display_widget = QWidget()
        self.family_display_layout = QVBoxLayout(self.family_display_widget)
        self.family_display_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # 填充家庭信息
        for family in self.families:
            family_box = QGroupBox(family.name)
            family_layout = QVBoxLayout()
            
            for member in family.members:
                member_label = QLabel(f"{member.name}")
                member_label.mousePressEvent = lambda event, m=member: self.display_character_details(m)
                family_layout.addWidget(member_label)
            
            family_box.setLayout(family_layout)
            self.family_display_layout.addWidget(family_box)

        # 创建滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.family_display_widget)
        
        # 添加到主布局
        main_layout.addWidget(self.detail_label)
        main_layout.addWidget(scroll_area)

        self.setLayout(main_layout)
    
    def display_character_details(self, character):
        details = (
            f"Name: {character.name}\n"
            f"Gender: {character.gender}\n"
            f"Age: {character.age}\n"
            f"Trait: {character.trait}\n"
            f"Player: {character.is_player}"
        )
        self.detail_label.setText(details)
