import random
import names

# 定义特质
traits = ['Brave', 'Smart', 'Cunning', 'Kind', 'Strong']

# 角色类
class Character:
    def __init__(self, is_player=False):
        self.name = names.get_full_name(gender=random.choice(['male', 'female']))
        self.gender = 'Male' if 'male' in self.name else 'Female'
        self.age = random.randint(18, 60)
        self.trait = random.choice(traits)
        self.is_player = is_player

    def __str__(self):
        return f"Name: {self.name}, Gender: {self.gender}, Age: {self.age}, Trait: {self.trait}, Player: {self.is_player}"

# 生成角色
def generate_characters(num):
    characters = []
    for _ in range(num):
        characters.append(Character())
    return characters
