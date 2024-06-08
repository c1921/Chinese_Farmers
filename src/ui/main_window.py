from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea, QHBoxLayout, QGroupBox, QPushButton, QButtonGroup, QTextEdit
from datetime import datetime, timedelta

from src.family import Family

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # 创建家庭
        self.families = [Family() for _ in range(5)]
        self.characters_dict = {member.id: member for family in self.families for member in family.members}

        # 设置窗口
        self.setWindowTitle('Random Families Game')
        self.setGeometry(100, 100, 1200, 800)
        
        # 设置主布局
        main_layout = QVBoxLayout()

        # 日期和控制按钮布局
        top_layout = QHBoxLayout()

        # 顶部日期显示
        self.date_label = QLabel()
        self.date_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont("assets/fonts/LXGWFasmartGothic.ttf", 12)
        self.date_label.setFont(font)
        self.date_label.setFixedHeight(50)
        top_layout.addWidget(self.date_label)

        # 时间控制按钮
        self.speed_buttons = QButtonGroup(self)

        self.slow_button = QPushButton("1000 ms/day")
        self.slow_button.clicked.connect(lambda: self.set_timer_interval(1000))
        self.speed_buttons.addButton(self.slow_button)
        top_layout.addWidget(self.slow_button)

        self.medium_button = QPushButton("500 ms/day")
        self.medium_button.clicked.connect(lambda: self.set_timer_interval(500))
        self.speed_buttons.addButton(self.medium_button)
        top_layout.addWidget(self.medium_button)

        self.fast_button = QPushButton("100 ms/day")
        self.fast_button.clicked.connect(lambda: self.set_timer_interval(100))
        self.speed_buttons.addButton(self.fast_button)
        top_layout.addWidget(self.fast_button)

        self.very_fast_button = QPushButton("10 ms/day")
        self.very_fast_button.clicked.connect(lambda: self.set_timer_interval(10))
        self.speed_buttons.addButton(self.very_fast_button)
        top_layout.addWidget(self.very_fast_button)

        # 暂停/继续按钮
        self.pause_button = QPushButton("Pause")
        self.pause_button.clicked.connect(self.toggle_pause)
        top_layout.addWidget(self.pause_button)

        main_layout.addLayout(top_layout)

        # 左侧角色详细信息显示
        self.detail_widget = QWidget()
        self.detail_layout = QVBoxLayout(self.detail_widget)
        self.detail_label = QLabel()
        self.detail_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.detail_label.setFont(font)
        self.detail_layout.addWidget(self.detail_label)

        self.relation_label = QLabel("Relationships:")
        self.relation_label.setFont(font)
        self.detail_layout.addWidget(self.relation_label)

        self.relations_layout = QVBoxLayout()
        self.detail_layout.addLayout(self.relations_layout)

        detail_scroll_area = QScrollArea()
        detail_scroll_area.setWidgetResizable(True)
        detail_scroll_area.setWidget(self.detail_widget)
        detail_scroll_area.setFixedWidth(300)

        # 创建家庭显示区
        self.family_display_widget = QWidget()
        self.family_display_layout = QVBoxLayout(self.family_display_widget)
        self.family_display_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # 填充家庭信息
        self.update_family_display()

        # 创建滚动区域
        family_scroll_area = QScrollArea()
        family_scroll_area.setWidgetResizable(True)
        family_scroll_area.setWidget(self.family_display_widget)

        # 日志显示区
        self.log_text_edit = QTextEdit()
        self.log_text_edit.setReadOnly(True)
        self.log_text_edit.setFixedHeight(200)

        # 设置整体布局
        content_layout = QHBoxLayout()
        content_layout.addWidget(detail_scroll_area)
        content_layout.addWidget(family_scroll_area)
        
        main_layout.addLayout(content_layout)
        main_layout.addWidget(self.log_text_edit)

        self.setLayout(main_layout)

        # 设置起始日期
        self.current_date = datetime(1840, 1, 1)
        self.update_date_display()

        # 设置家庭成员的生日年份为当前日期年份减去年龄
        for family in self.families:
            for member in family.members:
                member.birth_date = datetime(self.current_date.year - member.age, member.birth_date.month, member.birth_date.day)

        # 设置定时器每天推进时间
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.advance_one_day)
        self.set_timer_interval(1000)
        self.timer.start()

        self.paused = False

        # 当前选中的角色
        self.selected_character = None
    
    def display_character_details(self, character):
        self.selected_character = character
        siblings = character.get_siblings(self.characters_dict)
        sibling_names = [sibling.name for sibling in siblings]

        father = character.get_father(self.characters_dict)
        mother = character.get_mother(self.characters_dict)
        children = character.get_children(self.characters_dict)

        details = (
            f"Name: {character.name}\n"
            f"Gender: {character.gender}\n"
            f"Age: {character.age}\n"
            f"Trait: {character.trait}\n"
            f"Player: {character.is_player}\n"
            f"Birthday: {character.birth_date.strftime('%Y-%m-%d')}\n"
            f"Fertility: {character.fertility:.2f}\n"
        )
        self.detail_label.setText(details)

        # 更新人物关系显示
        self.clear_layout(self.relations_layout)
        
        father_label = QLabel(f"Father: {father.name if father else 'Unknown'}")
        mother_label = QLabel(f"Mother: {mother.name if mother else 'Unknown'}")
        self.relations_layout.addWidget(father_label)
        self.relations_layout.addWidget(mother_label)

        if children:
            children_label = QLabel("Children:")
            self.relations_layout.addWidget(children_label)
            for child in children:
                child_label = QLabel(f"  {child.name}")
                self.relations_layout.addWidget(child_label)

        if sibling_names:
            siblings_label = QLabel("Siblings:")
            self.relations_layout.addWidget(siblings_label)
            for sibling_name in sibling_names:
                sibling_label = QLabel(f"  {sibling_name}")
                self.relations_layout.addWidget(sibling_label)

    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def advance_one_day(self):
        self.current_date += timedelta(days=1)
        self.update_date_display()

        log_messages = []
        for family in self.families:
            log_messages.extend(family.age_one_day(self.current_date, self.characters_dict))
            pregnancy_message = family.try_for_baby(self.current_date, self.characters_dict)
            if pregnancy_message:
                log_messages.append(pregnancy_message)

        self.update_family_display()
        self.update_selected_character_details()
        self.update_log_display(log_messages)

    def update_date_display(self):
        self.date_label.setText(self.current_date.strftime('%Y-%m-%d'))

    def update_family_display(self):
        # 清除当前家庭显示
        for i in reversed(range(self.family_display_layout.count())):
            widget = self.family_display_layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

        # 重新填充家庭信息
        for family in self.families:
            family_box = QGroupBox(f"Family {family.name}")
            family_layout = QVBoxLayout()
            
            for member in family.members:
                member_label = QLabel(f"{member.name} ({member.gender}, Age: {member.age})")
                member_label.mousePressEvent = lambda event, m=member: self.display_character_details(m)
                family_layout.addWidget(member_label)
            
            family_box.setLayout(family_layout)
            self.family_display_layout.addWidget(family_box)

    def update_selected_character_details(self):
        if self.selected_character:
            self.display_character_details(self.selected_character)

    def update_log_display(self, log_messages):
        for message in log_messages:
            self.log_text_edit.append(message)

    def set_timer_interval(self, interval):
        self.timer.setInterval(interval)

    def toggle_pause(self):
        if self.paused:
            self.timer.start()
            self.pause_button.setText("Pause")
        else:
            self.timer.stop()
            self.pause_button.setText("Resume")
        self.paused = not self.paused
