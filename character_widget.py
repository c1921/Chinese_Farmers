import random
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QScrollArea
from PyQt6.QtCore import QTimer, Qt
from datetime import datetime, timedelta
from character import Character, GAME_START_DATE, update_health, generate_child_character
from time_control import TimeControl
from character_list import CharacterList
from character_details import CharacterDetails
from event_logger import EventLogger
from config import TIMER_INTERVALS, MARRIAGE_PROBABILITY, MARRIAGE_ACCEPTANCE_PROBABILITY, PREGNANCY_PROBABILITY, PREGNANCY_DURATION, POST_BIRTH_PREGNANCY_DELAY, DEATH_PROBABILITY_COEFFICIENT
from keybindings import setup_shortcuts

class CharacterWidget(QWidget):
    def __init__(self, characters):
        super().__init__()
        self.characters = characters
        self.current_date = GAME_START_DATE
        self.timer_interval = TIMER_INTERVALS['1']
        self.timer_paused = False

        main_layout = QHBoxLayout()  # 使用 QHBoxLayout 代替 QVBoxLayout
        self.setLayout(main_layout)

        # 左侧布局
        left_layout = QVBoxLayout()
        main_layout.addLayout(left_layout)

        self.character_details = CharacterDetails()
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.character_details)
        scroll_area.setMaximumWidth(300)  # 设置最大宽度
        scroll_area.setStyleSheet("border: none;")  # 移除边框
        left_layout.addWidget(scroll_area)

        # 右侧布局
        right_layout = QVBoxLayout()
        main_layout.addLayout(right_layout)

        self.time_control = TimeControl(self)
        right_layout.addLayout(self.time_control.top_layout)

        self.character_list = CharacterList(self.characters, self.character_details.display_character_details)
        character_list_scroll_area = QScrollArea()
        character_list_scroll_area.setWidgetResizable(True)
        character_list_scroll_area.setWidget(self.character_list.tree)
        right_layout.addWidget(character_list_scroll_area)

        self.event_logger = EventLogger()
        right_layout.addWidget(self.event_logger.text_edit)

        setup_shortcuts(self)  # 设置快捷键
        self.populate_character_list()
        self.time_control.update_date_label(self.current_date)

        self.setWindowTitle("Chinese Farmers")  # 设置窗口标题

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(self.timer_interval)

    def log_event(self, content):
        log_entry = f"{self.current_date.strftime('%Y-%m-%d')}: {content}"
        self.event_logger.append_log(log_entry)

    def populate_character_list(self):
        self.character_list.populate()

    def update_time(self):
        self.current_date += timedelta(days=1)
        self.time_control.update_date_label(self.current_date)
        self.update_characters_age()
        self.handle_marriage_proposals()
        self.handle_pregnancy()
        self.handle_dying_characters()
        if self.character_details.current_character is not None:
            self.character_details.display_character_details(self.character_details.current_character)  # 自动更新角色栏

    def update_characters_age(self):
        for character in self.characters:
            if character.is_deceased:
                continue  # 跳过已死亡的角色
            if self.current_date.month == character.birth_date.month and self.current_date.day == character.birth_date.day:
                character.age += 1
                update_health(character)
                death_probability = (100 - character.health) * character.age * DEATH_PROBABILITY_COEFFICIENT
                if random.random() < death_probability / 100:
                    character.dying_days_left = random.randint(1, 365)
        self.populate_character_list()
        self.character_list.update_current_character(self.character_details)

    def handle_marriage_proposals(self):
        for character in self.characters:
            if character.is_deceased or character.spouse is not None or character.age < 16:
                continue  # 跳过已死亡、有配偶或年龄小于16岁的角色
            if random.random() < MARRIAGE_PROBABILITY:
                potential_spouses = [
                    c for c in self.characters 
                    if c.gender != character.gender and c.spouse is None and c.age >= 16 and not c.is_deceased
                ]
                if potential_spouses:
                    chosen_spouse = random.choice(potential_spouses)
                    if self.can_marry(character, chosen_spouse):
                        if random.random() < MARRIAGE_ACCEPTANCE_PROBABILITY:
                            character.spouse = chosen_spouse
                            chosen_spouse.spouse = character
                            if character.gender == "Female":
                                character.family = chosen_spouse.family
                                character.family.add_member(character)
                            else:
                                chosen_spouse.family = character.family
                                chosen_spouse.family.add_member(chosen_spouse)
                            self.log_event(f"{character.name} 和 {chosen_spouse.name} 结婚了。")
        self.populate_character_list()

    def can_marry(self, character, chosen_spouse):
        """
        检查角色是否可以结婚，避免近亲结婚：
        如果对方与自己在同一家庭，并且与对方的世代的差值小于5，则不允许。
        """
        if character.family == chosen_spouse.family:
            if abs(character.generation - chosen_spouse.generation) < 5:
                return False
        return True

    def handle_pregnancy(self):
        new_characters = []
        for character in self.characters:
            if character.is_deceased or character.spouse is None or character.gender != "Female" or character.age < 16 or character.age >= 40:
                continue  # 跳过已死亡、无配偶、非女性或不在生育年龄范围内的角色
            fertility_probability = (character.fertility + character.spouse.fertility) / 2 * PREGNANCY_PROBABILITY
            if character.pregnancy_days == 0 and (character.last_birth_date is None or (self.current_date - character.last_birth_date).days >= POST_BIRTH_PREGNANCY_DELAY) and random.random() < fertility_probability:
                character.pregnancy_days = 1
            elif character.pregnancy_days > 0:
                character.pregnancy_days += 1
                if character.pregnancy_days >= PREGNANCY_DURATION:
                    new_character = generate_child_character(character.spouse, character, self.current_date)
                    new_characters.append(new_character)
                    self.log_event(f"{character.name} 和 {character.spouse.name} 生育了一个孩子：{new_character.name}。")
                    character.pregnancy_days = 0

        for new_character in new_characters:
            self.characters.append(new_character)
        self.populate_character_list()

    def handle_dying_characters(self):
        for character in self.characters:
            if character.dying_days_left is not None:
                character.dying_days_left -= 1
                if character.dying_days_left <= 0:
                    self.log_event(f"{character.name} 在 {self.current_date.strftime('%Y-%m-%d')} 死亡，享年 {character.age} 岁。")
                    character.is_deceased = True  # 更新死亡属性
                    character.death_date = self.current_date  # 设置死亡日期
                    self.populate_character_list()  # 更新角色列表显示
                    self.character_list.update_current_character(self.character_details)  # 更新当前角色详情显示
                    character.dying_days_left = None  # 清除濒死天数

    def set_timer_interval(self, interval):
        self.timer_interval = interval
        self.timer.setInterval(self.timer_interval)

    def toggle_timer(self):
        if self.timer_paused:
            self.timer.start(self.timer_interval)
        else:
            self.timer.stop()
        self.timer_paused = not self.timer_paused
        self.time_control.update_pause_button(self.timer_paused)
