from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class CharacterDisplay:
    def __init__(self, characters_dict):
        self.characters_dict = characters_dict
        self.selected_character_label = None  # 初始化 selected_character_label 属性

        font = QFont("assets/fonts/LXGWFasmartGothic.ttf", 12)

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
            f"Married: {'Yes' if character.married else 'No'}\n"
        )
        self.detail_label.setText(details)

        # 更新人物关系显示
        self.clear_layout(self.relations_layout)
        
        if father or mother:
            parents_text = "Parents: "
            if father:
                parents_text += father.name
            if mother:
                parents_text += f" and {mother.name}" if father else mother.name
            parents_label = QLabel(parents_text)
            self.set_label_clickable(parents_label, father)
            self.set_label_clickable(parents_label, mother)
            self.relations_layout.addWidget(parents_label)

        if children:
            children_label = QLabel("Children:")
            self.relations_layout.addWidget(children_label)
            for child in children:
                child_label = QLabel(f"  {child.name}")
                self.set_label_clickable(child_label, child)
                self.relations_layout.addWidget(child_label)

        if sibling_names:
            siblings_label = QLabel("Siblings:")
            self.relations_layout.addWidget(siblings_label)
            for sibling in siblings:
                sibling_label = QLabel(f"  {sibling.name}")
                self.set_label_clickable(sibling_label, sibling)
                self.relations_layout.addWidget(sibling_label)

        if character.partner_id:
            partner = self.characters_dict.get(character.partner_id)
            if partner:
                partner_label = QLabel(f"Spouse: {partner.name}")
                self.set_label_clickable(partner_label, partner)
                self.relations_layout.addWidget(partner_label)

        self.highlight_selected_character()

    def highlight_selected_character(self):
        if self.selected_character_label:
            if self.selected_character_label in self.detail_widget.findChildren(QLabel):
                self.selected_character_label.setStyleSheet("")
            self.selected_character_label = None
        if self.selected_character:
            for family in self.characters_dict.values():
                if hasattr(family, 'members'):
                    for member in family.members:
                        if member == self.selected_character:
                            for i in range(self.relations_layout.count()):
                                family_box = self.relations_layout.itemAt(i).widget()
                                if family_box and family_box.text().startswith(member.name):
                                    family_box.setStyleSheet("background-color: yellow;")
                                    self.selected_character_label = family_box
                                    return

    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def update_selected_character_details(self, character):
        if character:
            self.display_character_details(character)

    def set_label_clickable(self, label, character):
        if character:
            label.mousePressEvent = lambda event, char=character: self.display_character_details(char)
            label.setCursor(Qt.CursorShape.PointingHandCursor)
            label.setStyleSheet("color: blue; text-decoration: underline;")
