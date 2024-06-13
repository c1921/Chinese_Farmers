from PyQt6.QtWidgets import QVBoxLayout, QLabel, QPushButton

class CharacterDetails:
    def __init__(self):
        self.layout = QVBoxLayout()
        self.detail_label = QLabel("选择一个角色查看详细信息")
        self.layout.addWidget(self.detail_label)
        self.spouse_button = QPushButton("跳转至配偶")
        self.spouse_button.setEnabled(False)
        self.layout.addWidget(self.spouse_button)

    def display_character_details(self, character):
        self.detail_label.setText(str(character))
        if character.spouse:
            self.spouse_button.setEnabled(True)
            self.spouse_button.clicked.connect(lambda: self.display_character_details(character.spouse))
        else:
            self.spouse_button.setEnabled(False)
