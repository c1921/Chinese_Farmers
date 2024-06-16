from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QButtonGroup
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from config import TIMER_INTERVALS  # 导入TIMER_INTERVALS

class TimeControl:
    def __init__(self, main_window):
        self.main_window = main_window

        # 日期和控制按钮布局
        self.top_layout = QHBoxLayout()

        # 顶部日期显示
        self.date_label = QLabel()
        self.date_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont("assets/fonts/LXGWFasmartGothic.ttf", 12)
        self.date_label.setFont(font)
        self.date_label.setFixedHeight(50)
        self.top_layout.addWidget(self.date_label)

        # 时间控制按钮
        self.speed_buttons = QButtonGroup(self.main_window)

        self.slow_button = QPushButton("1")
        self.slow_button.clicked.connect(lambda: self.main_window.set_timer_interval(TIMER_INTERVALS['1']))
        self.speed_buttons.addButton(self.slow_button)
        self.top_layout.addWidget(self.slow_button)

        self.medium_button = QPushButton("2")
        self.medium_button.clicked.connect(lambda: self.main_window.set_timer_interval(TIMER_INTERVALS['2']))
        self.speed_buttons.addButton(self.medium_button)
        self.top_layout.addWidget(self.medium_button)

        self.fast_button = QPushButton("3")
        self.fast_button.clicked.connect(lambda: self.main_window.set_timer_interval(TIMER_INTERVALS['3']))
        self.speed_buttons.addButton(self.fast_button)
        self.top_layout.addWidget(self.fast_button)

        self.very_fast_button = QPushButton("4")
        self.very_fast_button.clicked.connect(lambda: self.main_window.set_timer_interval(TIMER_INTERVALS['4']))
        self.speed_buttons.addButton(self.very_fast_button)
        self.top_layout.addWidget(self.very_fast_button)

        # 暂停/继续按钮
        self.pause_button = QPushButton("Pause")
        self.pause_button.clicked.connect(self.main_window.toggle_timer)
        self.top_layout.addWidget(self.pause_button)

    def update_date_label(self, date):
        self.date_label.setText(f"当前日期: {date.strftime('%Y-%m-%d')}")

    def update_pause_button(self, paused):
        if paused:
            self.pause_button.setText("Resume")
        else:
            self.pause_button.setText("Pause")
