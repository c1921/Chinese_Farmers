import random
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QListWidget, QListWidgetItem, QPushButton, QTreeWidget, QTreeWidgetItem
from PyQt6.QtCore import QTimer
from character import generate_random_character, generate_child_character
from time_control import TimeControl

class CharacterWidget(QWidget):
    def __init__(self, characters):
        super().__init__()
        self.characters = characters  # 存储角色列表
        self.days = 0  # 初始化天数
        self.timer_interval = 10  # 初始化时间间隔
        self.timer_paused = False  # 初始化定时器暂停状态

        # 设置布局
        main_layout = QVBoxLayout()  # 创建主布局
        self.setLayout(main_layout)  # 设置窗口布局

        # 时间控制模块
        self.time_control = TimeControl(self)
        main_layout.addLayout(self.time_control.top_layout)  # 将时间控制布局添加到主布局

        # 主界面布局
        content_layout = QHBoxLayout()  # 创建内容布局
        main_layout.addLayout(content_layout)  # 将内容布局添加到主布局

        # 左侧布局
        left_layout = QVBoxLayout()  # 创建左侧布局
        content_layout.addLayout(left_layout)  # 将左侧布局添加到内容布局

        # 显示角色详细信息
        self.detail_label = QLabel("选择一个角色查看详细信息")  # 初始化详细信息标签
        left_layout.addWidget(self.detail_label)  # 将详细信息标签添加到左侧布局

        # 跳转配偶按钮
        self.spouse_button = QPushButton("跳转至配偶")  # 创建跳转配偶按钮
        self.spouse_button.clicked.connect(self.jump_to_spouse)  # 连接按钮点击信号
        self.spouse_button.setEnabled(False)  # 初始状态下禁用按钮
        left_layout.addWidget(self.spouse_button)  # 将按钮添加到左侧布局

        # 右侧家庭树
        self.family_tree = QTreeWidget()  # 创建家庭树部件
        self.family_tree.setHeaderLabels(["角色", "家庭ID"])  # 设置标题
        self.family_tree.itemClicked.connect(self.display_character_details_from_tree)  # 连接点击信号
        content_layout.addWidget(self.family_tree)  # 将家庭树添加到内容布局

        self.populate_family_tree()  # 填充家庭树

        self.setWindowTitle("随机角色")  # 设置窗口标题

        # 设置定时器
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)  # 连接定时器的超时信号到时间更新方法
        self.timer.start(self.timer_interval)  # 根据初始时间间隔启动定时器

        self.current_character = None  # 当前选中的角色

    def populate_family_tree(self):
        """
        填充家庭树。
        """
        family_dict = {}
        for character in self.characters:
            if character.family_id not in family_dict:
                family_dict[character.family_id] = QTreeWidgetItem([character.family_id])
                self.family_tree.addTopLevelItem(family_dict[character.family_id])
            family_item = QTreeWidgetItem([character.name, character.family_id])
            family_item.setData(0, 1, character)  # 将角色对象存储在列表项的数据中
            family_dict[character.family_id].addChild(family_item)

    def display_character_details_from_tree(self, item, column):
        """
        从家庭树中显示选中的角色的详细信息。
        
        参数：
        item (QTreeWidgetItem): 被选中的树项。
        column (int): 被选中的列。
        """
        character = item.data(0, 1)  # 获取选中的角色对象
        if character:
            self.display_character_details(character)

    def display_character_details(self, character):
        """
        显示选中的角色的详细信息。
        
        参数：
        character (Character): 被选中的角色对象。
        """
        self.current_character = character  # 获取选中的角色对象
        self.detail_label.setText(str(self.current_character))  # 显示角色详细信息
        if self.current_character.spouse:  # 如果角色有配偶
            self.spouse_button.setEnabled(True)  # 启用跳转配偶按钮
        else:
            self.spouse_button.setEnabled(False)  # 禁用跳转配偶按钮

    def jump_to_spouse(self):
        """
        跳转至选中角色的配偶。
        """
        if self.current_character and self.current_character.spouse:
            spouse = self.current_character.spouse  # 获取配偶对象
            for i in range(self.family_tree.topLevelItemCount()):
                family_item = self.family_tree.topLevelItem(i)
                for j in range(family_item.childCount()):
                    child_item = family_item.child(j)
                    if child_item.data(0, 1) == spouse:
                        self.family_tree.setCurrentItem(child_item)  # 设置配偶为当前选中项
                        self.display_character_details(spouse)  # 显示配偶的详细信息
                        break

    def update_time(self):
        """
        更新当前天数并处理角色的婚姻申请和生育。
        """
        self.days += 1  # 天数加1
        self.time_control.update_date_label(self.days)  # 更新日期标签
        self.handle_marriage_proposals()  # 处理角色的婚姻申请
        self.handle_pregnancy()  # 处理角色的怀孕和生育

    def handle_marriage_proposals(self):
        """
        处理角色之间的婚姻申请。
        """
        for character in self.characters:
            if character.spouse is None:  # 如果角色没有配偶
                if random.random() < 0.05:  # 5%的概率发出婚姻申请
                    potential_spouses = [c for c in self.characters if c.gender != character.gender and c.spouse is None]
                    if potential_spouses:
                        chosen_spouse = random.choice(potential_spouses)
                        if random.random() < 0.5:  # 50%的概率同意婚姻申请
                            character.spouse = chosen_spouse
                            chosen_spouse.spouse = character
                            if character.gender == "Female":
                                character.family_id = chosen_spouse.family_id  # 女性角色进入男性的家庭
                            self.populate_family_tree()  # 更新家庭树

    def handle_pregnancy(self):
        """
        处理已婚角色的怀孕和生育。
        """
        new_characters = []
        for character in self.characters:
            if character.spouse and character.gender == "Female" and 16 <= character.age < 40:
                if character.pregnancy_days == 0 and random.random() < 0.1:  # 10%的概率怀孕
                    character.pregnancy_days = 1
                elif character.pregnancy_days > 0:
                    character.pregnancy_days += 1
                    if character.pregnancy_days >= 270:  # 怀孕270天后生育
                        new_character = generate_child_character(character.spouse, character)
                        new_character.family_id = character.family_id  # 新生育的角色进入其母亲的家庭
                        new_characters.append(new_character)
                        character.pregnancy_days = 0

        for new_character in new_characters:
            self.characters.append(new_character)
            item = QTreeWidgetItem([new_character.name, new_character.family_id])
            item.setData(0, 1, new_character)
            for i in range(self.family_tree.topLevelItemCount()):
                family_item = self.family_tree.topLevelItem(i)
                if family_item.text(0) == new_character.family_id:
                    family_item.addChild(item)
                    break
            else:
                new_family_item = QTreeWidgetItem([new_character.family_id])
                new_family_item.addChild(item)
                self.family_tree.addTopLevelItem(new_family_item)

    def set_timer_interval(self, interval):
        """
        设置定时器的时间间隔。
        
        参数：
        interval (int): 新的时间间隔（毫秒）。
        """
        self.timer_interval = interval
        self.timer.setInterval(self.timer_interval)

    def toggle_timer(self):
        """
        切换定时器的暂停/继续状态。
        """
        if self.timer_paused:
            self.timer.start(self.timer_interval)  # 继续定时器
        else:
            self.timer.stop()  # 暂停定时器
        self.timer_paused = not self.timer_paused
        self.time_control.update_pause_button(self.timer_paused)
