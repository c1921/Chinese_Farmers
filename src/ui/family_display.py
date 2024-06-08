from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGroupBox
from PyQt6.QtCore import Qt

class FamilyDisplay:
    def __init__(self, families, display_character_details):
        self.families = families
        self.display_character_details = display_character_details
        self.family_display_widget = QWidget()
        self.family_display_layout = QVBoxLayout(self.family_display_widget)
        self.family_display_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.update_family_display(None)

    def update_family_display(self, selected_character):
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
                member_label.mousePressEvent = lambda event, m=member: self.on_member_click(event, m)
                family_layout.addWidget(member_label)
                if selected_character and selected_character == member:
                    member_label.setStyleSheet("background-color: yellow;")
            
            family_box.setLayout(family_layout)
            self.family_display_layout.addWidget(family_box)

    def on_member_click(self, event, member):
        self.display_character_details(member)
