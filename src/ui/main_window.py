import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QScrollArea, QHBoxLayout, QTextEdit
from PyQt6.QtCore import QTimer, Qt
from datetime import datetime, timedelta
import random
from src.family import Family
from src.ui.character_display import CharacterDisplay
from src.ui.family_display import FamilyDisplay
from src.ui.time_control import TimeControl

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
        self.time_control = TimeControl(self)
        self.time_control.slow_button.clicked.connect(lambda: self.set_timer_interval(1000))
        self.time_control.medium_button.clicked.connect(lambda: self.set_timer_interval(500))
        self.time_control.fast_button.clicked.connect(lambda: self.set_timer_interval(100))
        self.time_control.very_fast_button.clicked.connect(lambda: self.set_timer_interval(10))
        self.time_control.pause_button.clicked.connect(self.toggle_pause)

        main_layout.addLayout(self.time_control.top_layout)

        # 左侧角色详细信息显示
        self.character_display = CharacterDisplay(self.characters_dict)
        detail_scroll_area = QScrollArea()
        detail_scroll_area.setWidgetResizable(True)
        detail_scroll_area.setWidget(self.character_display.detail_widget)
        detail_scroll_area.setFixedWidth(300)

        # 创建家庭显示区
        self.family_display = FamilyDisplay(self.families, self.character_display.display_character_details)
        family_scroll_area = QScrollArea()
        family_scroll_area.setWidgetResizable(True)
        family_scroll_area.setWidget(self.family_display.family_display_widget)

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
        self.selected_character_label = None
    
    def advance_one_day(self):
        self.current_date += timedelta(days=1)
        self.update_date_display()

        log_messages = []
        for family in self.families:
            log_messages.extend(family.age_one_day(self.current_date, self.characters_dict))
            pregnancy_message = family.try_for_baby(self.current_date, self.characters_dict)
            if pregnancy_message:
                log_messages.append(pregnancy_message)
        
        # 进行婚姻匹配
        log_messages.extend(self.match_marriages())

        self.family_display.update_family_display(self.selected_character)
        self.character_display.update_selected_character_details(self.selected_character)
        self.update_log_display(log_messages)

    def match_marriages(self):
        log_messages = []
        unmarried_males = [char for char in self.characters_dict.values() if char.gender == 'Male' and not char.married and char.age >= 16]
        unmarried_females = [char for char in self.characters_dict.values() if char.gender == 'Female' and not char.married and char.age >= 16]

        for male in unmarried_males:
            if unmarried_females:
                female = random.choice(unmarried_females)
                if male.marry(female):
                    log_messages.append(f"{self.current_date.strftime('%Y-%m-%d')}: {male.name} married {female.name}.")
                    unmarried_females.remove(female)

                    # 将女性角色从原有家庭分组移到男性角色的家庭分组
                    for family in self.families:
                        if female in family.members:
                            family.remove_member(female)
                    male_family = next(fam for fam in self.families if male in fam.members)
                    male_family.add_member(female)
        
        return log_messages

    def update_date_display(self):
        self.time_control.date_label.setText(self.current_date.strftime('%Y-%m-%d'))

    def update_log_display(self, log_messages):
        for message in log_messages:
            self.log_text_edit.append(message)

    def set_timer_interval(self, interval):
        self.timer.setInterval(interval)

    def toggle_pause(self):
        if self.paused:
            self.timer.start()
            self.time_control.pause_button.setText("Pause")
        else:
            self.timer.stop()
            self.time_control.pause_button.setText("Resume")
        self.paused = not self.paused

def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
