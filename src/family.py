from src.character import Character, generate_characters

class Family:
    def __init__(self, name, num_members):
        self.name = name
        self.members = generate_characters(num_members)

    def __str__(self):
        return f"Family {self.name} with members:\n" + "\n".join(str(member) for member in self.members)
