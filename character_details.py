from PyQt6.QtWidgets import QVBoxLayout, QLabel, QPushButton, QHBoxLayout

class CharacterDetails:
    def __init__(self):
        self.layout = QVBoxLayout()
        self.detail_label = QLabel("选择一个角色查看详细信息")
        self.layout.addWidget(self.detail_label)

        # 配偶跳转按钮
        self.spouse_button = QPushButton("跳转至配偶")
        self.spouse_button.setEnabled(False)
        self.layout.addWidget(self.spouse_button)

        # 子女列表标签和布局
        self.children_label = QLabel("子女:")
        self.layout.addWidget(self.children_label)
        self.children_buttons_layout = QVBoxLayout()
        self.layout.addLayout(self.children_buttons_layout)

    def display_character_details(self, character):
        self.detail_label.setText(str(character))
        
        # 配偶跳转按钮
        if character.spouse:
            self.spouse_button.setEnabled(True)
            self.spouse_button.clicked.connect(lambda: self.display_character_details(character.spouse))
        else:
            self.spouse_button.setEnabled(False)

        # 更新子女信息
        self.update_children_buttons(character)

    def update_children_buttons(self, character):
        # 清空子女按钮布局
        while self.children_buttons_layout.count():
            child = self.children_buttons_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # 创建并添加子女按钮
        for child in character.children:
            child_button = QPushButton(f"{child.name} ( {child.gender} {child.age} )")
            child_button.clicked.connect(self.create_child_button_lambda(child))
            self.children_buttons_layout.addWidget(child_button)

    def create_child_button_lambda(self, child):
        """
        创建子女按钮的 lambda 函数以避免捕获错误的变量。
        """
        return lambda: self.display_character_details(child)
