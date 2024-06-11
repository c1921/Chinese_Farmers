import random
import uuid

class Character:
    """
    表示一个角色的类，包含唯一ID、姓名、性别、年龄、能力值、配偶和怀孕天数。
    """
    def __init__(self, name, gender, age, abilities):
        self.id = str(uuid.uuid4())  # 生成唯一ID
        self.name = name  # 设置角色姓名
        self.gender = gender  # 设置角色性别
        self.age = age  # 设置角色年龄
        self.abilities = abilities  # 设置角色能力值
        self.spouse = None  # 初始化配偶为None
        self.pregnancy_days = 0  # 初始化怀孕天数为0
        self.family_id = str(uuid.uuid4())  # 初始化家庭ID

    def __str__(self):
        spouse_name = self.spouse.name if self.spouse else "无"  # 获取配偶姓名
        return f"ID: {self.id}\nName: {self.name}\nGender: {self.gender}\nAge: {self.age}\nAbilities: {self.abilities}\nSpouse: {spouse_name}\nPregnancy Days: {self.pregnancy_days}\n"  # 返回角色的字符串表示

def generate_random_character():
    """
    生成一个随机角色。
    
    返回：
    Character: 一个随机生成的角色对象。
    """
    names = ["Alice", "Bob", "Charlie", "Diana", "Eve"]  # 预定义姓名列表
    genders = ["Male", "Female"]  # 预定义性别列表
    name = random.choice(names)  # 随机选择姓名
    gender = random.choice(genders)  # 随机选择性别
    age = random.randint(18, 60)  # 随机生成年龄
    abilities = {
        "strength": random.randint(1, 100),  # 随机生成力量值
        "intelligence": random.randint(1, 100),  # 随机生成智力值
        "dexterity": random.randint(1, 100),  # 随机生成灵巧值
        "charisma": random.randint(1, 100)  # 随机生成魅力值
    }
    return Character(name, gender, age, abilities)  # 返回生成的角色对象

def generate_child_character(father, mother):
    """
    生成一个子角色。
    
    参数：
    father (Character): 父亲角色。
    mother (Character): 母亲角色。
    
    返回：
    Character: 一个子角色对象。
    """
    name = f"{father.name} Jr."  # 生成子角色的姓名
    gender = random.choice(["Male", "Female"])  # 随机生成性别
    age = 0  # 子角色的年龄为0
    abilities = {
        "strength": (father.abilities["strength"] + mother.abilities["strength"]) // 2,  # 计算力量值的平均数
        "intelligence": (father.abilities["intelligence"] + mother.abilities["intelligence"]) // 2,  # 计算智力值的平均数
        "dexterity": (father.abilities["dexterity"] + mother.abilities["dexterity"]) // 2,  # 计算灵巧值的平均数
        "charisma": (father.abilities["charisma"] + mother.abilities["charisma"]) // 2  # 计算魅力值的平均数
    }
    return Character(name, gender, age, abilities)  # 返回生成的子角色对象
