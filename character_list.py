from PyQt6.QtWidgets import QTreeWidget, QTreeWidgetItem
from character import Character
from utils import number_to_chinese

class CharacterList:
    def __init__(self, characters, display_character_details_callback):
        self.characters = characters
        self.display_character_details_callback = display_character_details_callback
        self.tree = QTreeWidget()
        self.tree.setHeaderLabel("家庭与角色")
        self.tree.itemClicked.connect(self.display_character_details)

    def populate(self):
        self.tree.clear()
        families = {}
        for character in self.characters:
            if character.is_deceased:  # 跳过已死亡角色
                continue
            if character.family.id not in families:
                families[character.family.id] = []
            families[character.family.id].append(character)

        for family_id, members in families.items():
            family_item = QTreeWidgetItem(self.tree)
            family_item.setText(0, f"Family {family_id} (人数: {len(members)})")
            family_item.setExpanded(True)
            for character in members:
                character_item = QTreeWidgetItem(family_item)
                gender_symbol = "♂" if character.gender == "Male" else "♀"
                generation_chinese = number_to_chinese(character.generation)
                character_item.setText(0, f"{character.name} ( {gender_symbol} {character.age} {generation_chinese} )")
                character_item.setData(0, 1, character)

        self.tree.setHeaderLabel(f"家庭与角色 (总人数: {len(self.characters)})")

    def display_character_details(self, item):
        character = item.data(0, 1)
        if isinstance(character, Character):
            self.display_character_details_callback(character)

    def update_current_character(self, character_details):
        current_item = self.tree.currentItem()
        if current_item:
            character = current_item.data(0, 1)
            if isinstance(character, Character):
                character_details.display_character_details(character)
