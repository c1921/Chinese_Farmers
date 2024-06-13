from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QButtonGroup
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

class TimeControl:
    """
    时间控制模块，包含日期显示和时间流速控制按钮。
    """
    def __init__(self, main_window):
        self.main_window = main_window

        # 日期和控制按钮布局
        self.top_layout = QHBoxLayout()

        # 顶部日期显示
        self.date_label = QLabel()
        self.date_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont("Arial", 12)
        self.date_label.setFont(font)
        self.date_label.setFixedHeight(50)
        self.top_layout.addWidget(self.date_label)

        # 时间控制按钮
        self.speed_buttons = QButtonGroup(self.main_window)

        self.slow_button = QPushButton("1000 ms/day")
        self.speed_buttons.addButton(self.slow_button)
        self.top_layout.addWidget(self.slow_button)

        self.medium_button = QPushButton("500 ms/day")
        self.speed_buttons.addButton(self.medium_button)
        self.top_layout.addWidget(self.medium_button)

        self.fast_button = QPushButton("100 ms/day")
        self.speed_buttons.addButton(self.fast_button)
        self.top_layout.addWidget(self.fast_button)

        self.very_fast_button = QPushButton("10 ms/day")
        self.speed_buttons.addButton(self.very_fast_button)
        self.top_layout.addWidget(self.very_fast_button)

        # 暂停/继续按钮
        self.pause_button = QPushButton("Pause")
        self.top_layout.addWidget(self.pause_button)

        # 连接按钮点击信号
        self.slow_button.clicked.connect(lambda: self.main_window.set_timer_interval(1000))
        self.medium_button.clicked.connect(lambda: self.main_window.set_timer_interval(500))
        self.fast_button.clicked.connect(lambda: self.main_window.set_timer_interval(100))
        self.very_fast_button.clicked.connect(lambda: self.main_window.set_timer_interval(10))
        self.pause_button.clicked.connect(self.main_window.toggle_timer)

    def update_date_label(self, date):
        """
        更新日期标签显示当前日期。
        
        参数：
        date (datetime): 当前日期。
        """
        self.date_label.setText(f"当前日期: {date.strftime('%Y-%m-%d')}")

    def update_pause_button(self, is_paused):
        """
        更新暂停按钮的文本。
        
        参数：
        is_paused (bool): 定时器是否暂停。
        """
        self.pause_button.setText("Resume" if is_paused else "Pause")
