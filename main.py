import sys
from PyQt6.QtWidgets import QApplication
from character import generate_random_character
from character_widget import CharacterWidget

def main():
    """
    主函数，创建应用程序，生成随机角色并显示。
    """
    app = QApplication(sys.argv)  # 创建应用程序对象
    characters = [generate_random_character() for _ in range(20)]  # 生成二十个随机角色
    widget = CharacterWidget(characters)  # 创建角色窗口部件
    widget.show()  # 显示窗口
    sys.exit(app.exec())  # 运行应用程序主循环

if __name__ == "__main__":
    main()
