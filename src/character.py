import random
import names
from datetime import datetime, timedelta

# 定义特质
traits = ['Brave', 'Smart', 'Cunning', 'Kind', 'Strong']

# 角色类
class Character:
    def __init__(self, is_player=False, gender=None, age_range=None, birth_date=None, surname=None):
        if gender is None:
            gender = random.choice(['male', 'female'])
        if surname is None:
            self.name = names.get_full_name(gender=gender)
        else:
            self.name = f"{names.get_first_name(gender=gender)} {surname}"
        self.gender = 'Male' if gender == 'male' else 'Female'
        if age_range is None:
            self.age = random.randint(18, 60)
        else:
            self.age = random.randint(*age_range)
        self.trait = random.choice(traits)
        self.is_player = is_player
        self.pregnant = False
        self.pregnancy_days = 0  # 怀孕天数
        self.postpartum_days = 90  # 产后恢复天数初始值为90以便开始可以立即尝试怀孕
        self.fertility = 1.0  # 生育能力默认为100%
        
        if birth_date is None:
            current_year = datetime.now().year  # 使用当前年份
            start_date = datetime(current_year - self.age, 1, 1)
            end_date = datetime(current_year - self.age, 12, 31)
            self.birth_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
        else:
            self.birth_date = birth_date
        
        self.update_fertility()

    def __str__(self):
        return f"Name: {self.name}, Gender: {self.gender}, Age: {self.age}, Trait: {self.trait}, Player: {self.is_player}, Birthday: {self.birth_date.strftime('%Y-%m-%d')}"

    def update_fertility(self):
        # 更新生育能力
        if self.age < 25:
            self.fertility = 1.0
        elif self.age < 40:
            self.fertility = 1.0 - (0.8 * (self.age - 25) / 15)  # 从25岁开始下降，到40岁下降至20%
        else:
            self.fertility = 0.2

    def age_one_day(self, current_date):
        # 每天更新年龄
        if current_date.month == self.birth_date.month and current_date.day == self.birth_date.day:
            self.age += 1
            self.update_fertility()
        
        if self.gender == 'Female':
            if self.pregnant:
                self.pregnancy_days += 1
                if self.pregnancy_days >= 270:  # 怀孕270天后生产
                    self.pregnant = False
                    self.pregnancy_days = 0
                    self.postpartum_days = 0
                    new_born = self.give_birth(current_date)
                    return f"{current_date.strftime('%Y-%m-%d')}: {self.name} gave birth to {new_born.name}."
            elif self.postpartum_days < 90:
                self.postpartum_days += 1
        return None

    def get_pregnant(self, partner_fertility, current_date):
        if (not self.pregnant and self.gender == 'Female' and 16 <= self.age < 40 and self.postpartum_days >= 90):
            pregnancy_chance = (self.fertility + partner_fertility) * 0.005  # 怀孕概率
            if random.random() < pregnancy_chance:
                self.pregnant = True
                return f"{current_date.strftime('%Y-%m-%d')}: {self.name} got pregnant."
        return None

    def give_birth(self, birth_date):
        surname = self.name.split()[-1]
        return Character(gender=random.choice(['male', 'female']), age_range=(0, 0), birth_date=birth_date, surname=surname)
