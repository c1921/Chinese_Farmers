import random
from datetime import datetime, timedelta
from id_generator import UniqueIDGenerator
import names
from utils import number_to_chinese

character_id_generator = UniqueIDGenerator()
family_id_generator = UniqueIDGenerator()

GAME_START_DATE = datetime(1840, 1, 1)

class Family:
    """
    表示一个家庭的类，包含唯一ID和家庭成员列表。
    """
    def __init__(self):
        self.id = family_id_generator.generate_id()  # 生成唯一ID
        self.members = []  # 初始化家庭成员列表

    def add_member(self, member):
        """
        添加家庭成员。
        
        参数：
        member (Character): 需要添加的家庭成员。
        """
        self.members.append(member)

    def __str__(self):
        member_names = ", ".join(member.name for member in self.members)
        return f"Family ID: {self.id}\nMembers: {member_names}"

class Character:
    """
    表示一个角色的类，包含唯一ID、姓名、性别、年龄、能力值、配偶和怀孕天数。
    """
    def __init__(self, name, gender, age, abilities, birth_date, generation, family=None):
        self.id = character_id_generator.generate_id()  # 生成唯一ID
        self.name = name  # 设置角色姓名
        self.gender = gender  # 设置角色性别
        self.age = age  # 设置角色年龄
        self.abilities = abilities  # 设置角色能力值
        self.spouse = None  # 初始化配偶为None
        self.pregnancy_days = 0  # 初始化怀孕天数为0
        self.last_birth_date = None  # 初始化最近一次生产日期为None
        self.generation = generation  # 设置角色的世代
        self.family = family if family else Family()  # 如果没有传入家庭则创建一个新家庭
        self.family.add_member(self)  # 将角色添加到家庭
        self.birth_date = birth_date  # 设置角色的生日
        self.health = 100.0  # 初始化健康值为100%
        self.dying_days_left = None  # 初始化濒死天数为None

    def __str__(self):
        spouse_name = self.spouse.name if self.spouse else "无"  # 获取配偶姓名
        generation_chinese = number_to_chinese(self.generation)  # 将世代转换为汉字表示
        return f"ID: {self.id}\nName: {self.name}\nGender: {self.gender}\nAge: {self.age}\nAbilities: {self.abilities}\nHealth: {self.health}%\nSpouse: {spouse_name}\nPregnancy Days: {self.pregnancy_days}\nLast Birth Date: {self.last_birth_date}\nGeneration: {generation_chinese}\nFamily ID: {self.family.id}\nBirth Date: {self.birth_date.strftime('%Y-%m-%d')}"  # 返回角色的字符串表示

def generate_random_character():
    """
    生成一个随机角色。
    
    返回：
    Character: 一个随机生成的角色对象。
    """
    gender = random.choice(["Male", "Female"])  # 随机选择性别
    first_name = names.get_first_name(gender.lower())  # 根据性别生成名字
    last_name = names.get_last_name()  # 生成姓氏
    name = f"{last_name} {first_name}"  # 合并姓名，姓在前，名在后
    age = random.randint(18, 60)  # 随机生成年龄
    birth_date = GAME_START_DATE - timedelta(days=age*365 + random.randint(0, 364))  # 随机生成出生日期
    abilities = {
        "strength": random.randint(1, 100),  # 随机生成力量值
        "intelligence": random.randint(1, 100),  # 随机生成智力值
        "dexterity": random.randint(1, 100),  # 随机生成灵巧值
        "charisma": random.randint(1, 100)  # 随机生成魅力值
    }
    generation = 1  # 初始角色的世代为1
    return Character(name, gender, age, abilities, birth_date, generation)  # 返回生成的角色对象

def generate_child_character(father, mother, current_date):
    """
    生成一个子角色。
    
    参数：
    father (Character): 父亲角色。
    mother (Character): 母亲角色。
    current_date (datetime): 当前日期，用于设置子角色的出生日期。
    
    返回：
    Character: 一个子角色对象。
    """
    gender = random.choice(["Male", "Female"])  # 随机生成性别
    first_name = names.get_first_name(gender.lower())  # 根据性别生成名字
    last_name = father.name.split()[0]  # 使用父亲的姓氏
    name = f"{last_name} {first_name}"  # 生成子角色的姓名，姓在前，名在后
    age = 0  # 子角色的年龄为0
    abilities = {
        "strength": (father.abilities["strength"] + mother.abilities["strength"]) // 2,  # 计算力量值的平均数
        "intelligence": (father.abilities["intelligence"] + mother.abilities["intelligence"]) // 2,  # 计算智力值的平均数
        "dexterity": (father.abilities["dexterity"] + mother.abilities["dexterity"]) // 2,  # 计算灵巧值的平均数
        "charisma": (father.abilities["charisma"] + mother.abilities["charisma"]) // 2  # 计算魅力值的平均数
    }
    family = mother.family  # 子角色加入母亲的家庭
    generation = father.generation + 1  # 子角色的世代比父亲的世代多1
    mother.last_birth_date = current_date  # 更新母亲的最近一次生产日期
    return Character(name, gender, age, abilities, current_date, generation, family)  # 返回生成的子角色对象

def update_health(character):
    """
    根据角色年龄更新健康值，年龄超过30岁健康值下降，使用二次函数。
    
    参数：
    character (Character): 需要更新健康值的角色。
    """
    if character.age > 30:
        age_diff = character.age - 30
        character.health -= age_diff ** 2 * 0.05  # 将0.05改为0.01以减缓健康值下降速度
        # 移除对健康值下限的限制

