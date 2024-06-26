from PyQt6.QtWidgets import QVBoxLayout, QLabel, QPushButton, QScrollArea, QWidget
from family_window import FamilyWindow  # 导入家庭成员窗口

def format_date(date):
    """格式化日期，仅保留年月日"""
    return date.strftime('%Y-%m-%d') if date else "N/A"

class CharacterDetails(QWidget):
    def __init__(self):
        super().__init__()

        # 创建主布局和滚动区域
        self.layout = QVBoxLayout(self)
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.layout.addWidget(self.scroll_area)

        # 创建容器小部件和布局
        self.container_widget = QWidget()
        self.container_layout = QVBoxLayout(self.container_widget)

        # 设置滚动区域的窗口小部件
        self.scroll_area.setWidget(self.container_widget)

        # 详细信息标签
        self.detail_label = QLabel("选择一个角色查看详细信息")
        self.container_layout.addWidget(self.detail_label)

        # 能力标签
        self.strength_label = QLabel()
        self.intelligence_label = QLabel()
        self.dexterity_label = QLabel()
        self.charisma_label = QLabel()

        # 设置固定高度和间距
        for label in [self.strength_label, self.intelligence_label, self.dexterity_label, self.charisma_label]:
            label.setFixedHeight(10)
            self.container_layout.addWidget(label)
            self.container_layout.addSpacing(0)

        # 添加一个固定的空间隔开能力值和人物关系
        self.container_layout.addSpacing(15)

        # 父母列表标签和布局
        self.parents_label = QLabel("父母:")
        self.container_layout.addWidget(self.parents_label)
        self.container_layout.addSpacing(10)
        self.parents_buttons_layout = QVBoxLayout()
        self.container_layout.addLayout(self.parents_buttons_layout)

        # 配偶列表标签和布局
        self.spouse_label = QLabel("配偶:")
        self.container_layout.addWidget(self.spouse_label)
        self.container_layout.addSpacing(10)
        self.spouse_buttons_layout = QVBoxLayout()
        self.container_layout.addLayout(self.spouse_buttons_layout)

        # 子女列表标签和布局
        self.children_label = QLabel("子女:")
        self.container_layout.addWidget(self.children_label)
        self.container_layout.addSpacing(10)
        self.children_buttons_layout = QVBoxLayout()
        self.container_layout.addLayout(self.children_buttons_layout)

        # 兄弟姐妹列表标签和布局
        self.siblings_label = QLabel("兄弟姐妹:")
        self.container_layout.addWidget(self.siblings_label)
        self.container_layout.addSpacing(10)
        self.siblings_buttons_layout = QVBoxLayout()
        self.container_layout.addLayout(self.siblings_buttons_layout)

        # 家庭成员按钮
        self.family_button = QPushButton("查看家庭成员")
        self.family_button.clicked.connect(self.show_family_members)
        self.container_layout.addWidget(self.family_button)

        self.current_character = None  # 用于存储当前角色

    def display_character_details(self, character):
        self.current_character = character  # 更新当前角色
        birth_date = format_date(character.birth_date)
        last_birth_date = format_date(character.last_birth_date)

        detail_text = (f"ID: {character.id}\n"
                       f"Name: {character.name}\n"
                       f"Gender: {character.gender}\n"
                       f"Age: {character.age}\n"
                       f"Health: {character.health}%\n"
                       f"Generation: {character.generation}\n"
                       f"Family ID: {character.family.id}\n"
                       f"Birth Date: {birth_date}\n")

        if character.gender == "Female":
            detail_text += (f"Pregnancy Days: {character.pregnancy_days}\n"
                            f"Last Birth Date: {last_birth_date}\n")

        if character.is_deceased:
            death_date = format_date(character.death_date)
            detail_text += f"Death Date: {death_date}\n"
        
        self.detail_label.setText(detail_text)
        
        # 更新能力值标签
        self.strength_label.setText(f"Strength: {character.abilities['strength']}")
        self.intelligence_label.setText(f"Intelligence: {character.abilities['intelligence']}")
        self.dexterity_label.setText(f"Dexterity: {character.abilities['dexterity']}")
        self.charisma_label.setText(f"Charisma: {character.abilities['charisma']}")

        # 更新父母信息
        self.update_parents_buttons(character)

        # 更新配偶信息
        self.update_spouse_buttons(character)

        # 更新子女信息
        self.update_children_buttons(character)

        # 更新兄弟姐妹信息
        self.update_siblings_buttons(character)

    def show_family_members(self):
        if self.current_character:
            family_window = FamilyWindow(self.current_character.family)
            family_window.exec()

    def update_parents_buttons(self, character):
        # 清空父母按钮布局
        while self.parents_buttons_layout.count():
            parent = self.parents_buttons_layout.takeAt(0)
            if parent.widget():
                parent.widget().deleteLater()

        # 创建并添加父母按钮
        for parent in [character.father, character.mother]:
            if parent:
                gender_symbol = "♂" if parent.gender == "Male" else "♀"
                parent_button = QPushButton(f"{parent.name} ( {gender_symbol} {parent.age} )")
                parent_button.clicked.connect(self.create_parent_button_lambda(parent))
                self.parents_buttons_layout.addWidget(parent_button)

    def create_parent_button_lambda(self, parent):
        """
        创建父母按钮的 lambda 函数以避免捕获错误的变量。
        """
        return lambda: self.display_character_details(parent)

    def update_spouse_buttons(self, character):
        # 清空配偶按钮布局
        while self.spouse_buttons_layout.count():
            spouse = self.spouse_buttons_layout.takeAt(0)
            if spouse.widget():
                spouse.widget().deleteLater()

        # 创建并添加配偶按钮
        if character.spouse:
            gender_symbol = "♂" if character.spouse.gender == "Male" else "♀"
            spouse_button = QPushButton(f"{character.spouse.name} ( {gender_symbol} {character.spouse.age} )")
            spouse_button.clicked.connect(self.create_spouse_button_lambda(character.spouse))
            self.spouse_buttons_layout.addWidget(spouse_button)

    def create_spouse_button_lambda(self, spouse):
        """
        创建配偶按钮的 lambda 函数以避免捕获错误的变量。
        """
        return lambda: self.display_character_details(spouse)

    def update_children_buttons(self, character):
        # 清空子女按钮布局
        while self.children_buttons_layout.count():
            child = self.children_buttons_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # 创建并添加子女按钮
        for child in character.children:
            gender_symbol = "♂" if child.gender == "Male" else "♀"
            child_button = QPushButton(f"{child.name} ( {gender_symbol} {child.age} )")
            child_button.clicked.connect(self.create_child_button_lambda(child))
            self.children_buttons_layout.addWidget(child_button)

    def create_child_button_lambda(self, child):
        """
        创建子女按钮的 lambda 函数以避免捕获错误的变量。
        """
        return lambda: self.display_character_details(child)

    def update_siblings_buttons(self, character):
        # 清空兄弟姐妹按钮布局
        while self.siblings_buttons_layout.count():
            sibling = self.siblings_buttons_layout.takeAt(0)
            if sibling.widget():
                sibling.widget().deleteLater()

        # 创建并添加兄弟姐妹按钮
        if character.father:
            for sibling in character.father.children:
                if sibling != character:
                    gender_symbol = "♂" if sibling.gender == "Male" else "♀"
                    sibling_button = QPushButton(f"{sibling.name} ( {gender_symbol} {sibling.age} )")
                    sibling_button.clicked.connect(self.create_sibling_button_lambda(sibling))
                    self.siblings_buttons_layout.addWidget(sibling_button)

    def create_sibling_button_lambda(self, sibling):
        """
        创建兄弟姐妹按钮的 lambda 函数以避免捕获错误的变量。
        """
        return lambda: self.display_character_details(sibling)
