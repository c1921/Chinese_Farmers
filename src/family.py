from src.character import Character

class Family:
    def __init__(self):
        self.head = Character(is_player=True, gender='male')
        self.wife = Character(is_player=False, gender='female', age_range=(self.head.age - 5, self.head.age + 5), surname=self.head.name.split()[-1])
        self.head.partner_id = self.wife.id
        self.wife.partner_id = self.head.id
        self.head.married = True
        self.wife.married = True
        self.name = self.head.name.split()[-1]  # 使用姓氏作为家庭名
        self.members = [self.head, self.wife]

    def __str__(self):
        return f"Family {self.name} with members:\n" + "\n".join(str(member) for member in self.members)

    def age_one_day(self, current_date, characters_dict):
        new_members = []
        log_messages = []
        for member in self.members:
            log_message = member.age_one_day(current_date, characters_dict)
            if log_message:
                log_messages.append(log_message)
                new_members.append(characters_dict[member.children_ids[-1]])  # 添加新生儿到家庭成员
        self.members.extend(new_members)
        return log_messages

    def try_for_baby(self, current_date, characters_dict):
        log_message = self.wife.get_pregnant(self.head, current_date)
        if log_message:
            return log_message
        return None

    def add_member(self, member):
        self.members.append(member)

    def remove_member(self, member):
        self.members.remove(member)
