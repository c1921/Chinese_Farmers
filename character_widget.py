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

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        self.time_control = TimeControl(self)
        main_layout.addLayout(self.time_control.top_layout)

        content_layout = QHBoxLayout()
        main_layout.addLayout(content_layout)

        # 创建并添加角色详细信息区域
        self.character_details = CharacterDetails()
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.character_details)
        scroll_area.setMaximumWidth(300)  # 设置最大宽度
        scroll_area.setStyleSheet("border: none;")  # 移除边框
        content_layout.addWidget(scroll_area)

        # 创建并添加角色列表
        self.character_list = CharacterList(self.characters, self.character_details.display_character_details)
        character_list_scroll_area = QScrollArea()
        character_list_scroll_area.setWidgetResizable(True)
        character_list_scroll_area.setWidget(self.character_list.tree)
        content_layout.addWidget(character_list_scroll_area)

        self.event_logger = EventLogger()
        main_layout.addWidget(self.event_logger.text_edit)

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

    def update_characters_age(self):
        for character in self.characters:
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
            if character.spouse is None and character.age >= 16:
                if random.random() < MARRIAGE_PROBABILITY:
                    potential_spouses = [c for c in self.characters if c.gender != character.gender and c.spouse is None and c.age >= 16]
                    if potential_spouses:
                        chosen_spouse = random.choice(potential_spouses)
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

    def handle_pregnancy(self):
        new_characters = []
        for character in self.characters:
            if character.spouse and character.gender == "Female" and 16 <= character.age < 40:
                if character.pregnancy_days == 0 and (character.last_birth_date is None or (self.current_date - character.last_birth_date).days >= POST_BIRTH_PREGNANCY_DELAY) and random.random() < PREGNANCY_PROBABILITY:
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
                    self.characters.remove(character)
                    character.family.members.remove(character)
                    self.populate_character_list()
                    self.character_list.update_current_character(self.character_details)

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
