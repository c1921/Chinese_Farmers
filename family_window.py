from PyQt6.QtWidgets import QDialog, QVBoxLayout, QGraphicsView, QGraphicsScene, QGraphicsTextItem, QGraphicsLineItem, QGraphicsRectItem
from PyQt6.QtGui import QPen, QBrush, QColor, QFont
from PyQt6.QtCore import Qt

class FamilyWindow(QDialog):
    def __init__(self, family):
        super().__init__()
        self.setWindowTitle("家庭成员")
        self.setGeometry(100, 100, 800, 600)
        
        layout = QVBoxLayout(self)
        self.setLayout(layout)
        
        self.view = GenealogyTree(family)
        layout.addWidget(self.view)
        
class GenealogyTree(QGraphicsView):
    def __init__(self, family):
        super().__init__()
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.family = family
        self.positions = {}
        self.widths = {}
        self.all_members = self.get_all_family_members(family)  # 获取所有家庭成员
        self.initUI()

    def get_all_family_members(self, family):
        members = set(family.members)  # 包含当前家庭的所有成员
        to_check = list(family.members)

        # 获取所有的父母和孩子
        while to_check:
            member = to_check.pop()
            if member.father and member.father not in members:
                members.add(member.father)
                to_check.append(member.father)
            if member.mother and member.mother not in members:
                members.add(member.mother)
                to_check.append(member.mother)
            for child in member.children:
                if child not in members:
                    members.add(child)
                    to_check.append(child)

        return list(members)

    def initUI(self):
        # Calculate widths and node positions
        root_node = self.get_root_node()
        if root_node is None:
            return  # 如果没有符合条件的根节点，不显示树
        self.calculate_widths(root_node)
        self.calculate_positions(root_node, 400, 50)
        
        # Create nodes
        nodes = {}
        for member, pos in self.positions.items():
            node = QGraphicsRectItem(0, 0, 80, 40)
            if member.gender == "Male":
                node.setBrush(QBrush(QColor(173, 216, 230)))  # Set background color for male
            else:
                node.setBrush(QBrush(QColor(255, 182, 193)))  # Set background color for female
            node.setPos(*pos)
            self.scene.addItem(node)
            
            text = QGraphicsTextItem(f"{member.name} ( {'♂' if member.gender == 'Male' else '♀'} {member.age} )")
            if member.is_deceased:
                font = QFont()
                font.setItalic(True)
                text.setDefaultTextColor(Qt.GlobalColor.gray)
                text.setFont(font)
            else:
                text.setDefaultTextColor(Qt.GlobalColor.black)
            text.setPos(pos[0] + 10, pos[1] + 10)
            self.scene.addItem(text)
            nodes[member] = node

        # Create edges
        for member in self.all_members:
            for child in member.children:
                if member in nodes and child in nodes:
                    self.add_edge(nodes[member], nodes[child])

    def get_root_node(self):
        # 选择家族中世代第一的男性角色作为根节点
        try:
            root_node = next(member for member in self.all_members if member.generation == 1 and member.gender == "Male")
        except StopIteration:
            root_node = None  # 如果没有找到符合条件的根节点，返回None
        return root_node

    def calculate_widths(self, member):
        if not member.children:
            self.widths[member] = 80  # Width of one node
            return self.widths[member]

        if member in self.widths:
            return self.widths[member]

        # Width is the sum of the widths of its children
        width = 0
        for child in member.children:
            width += self.calculate_widths(child) + 20  # Add spacing between children
        width -= 20  # Remove extra space after the last child

        self.widths[member] = width
        return width

    def calculate_positions(self, member, x, y):
        if not member.children:
            self.positions[member] = (x, y)
            return

        # Calculate positions for all children
        current_x = x - self.widths[member] / 2
        for child in member.children:
            child_width = self.widths[child]
            self.calculate_positions(child, current_x + child_width / 2, y + 100)
            current_x += child_width + 20

        # Set parent's position to be the center of its children
        self.positions[member] = (x, y)

    def add_edge(self, parent, child):
        pen = QPen(QColor(105, 105, 105))  # Set line color
        pen.setWidth(2)
        parent_center_x = parent.x() + 40
        parent_center_y = parent.y() + 40
        child_center_x = child.x() + 40
        child_center_y = child.y()

        # Vertical line from parent to midpoint
        vertical_line = QGraphicsLineItem(parent_center_x, parent_center_y, parent_center_x, (parent_center_y + child_center_y) / 2)
        vertical_line.setPen(pen)
        self.scene.addItem(vertical_line)

        # Vertical line from midpoint to child
        vertical_line = QGraphicsLineItem(child_center_x, (parent_center_y + child_center_y) / 2, child_center_x, child_center_y)
        vertical_line.setPen(pen)
        self.scene.addItem(vertical_line)

        # Horizontal line from parent to child
        horizontal_line = QGraphicsLineItem(parent_center_x, (parent_center_y + child_center_y) / 2, child_center_x, (parent_center_y + child_center_y) / 2)
        horizontal_line.setPen(pen)
        self.scene.addItem(horizontal_line)
