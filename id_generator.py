class UniqueIDGenerator:
    def __init__(self):
        self.current_id = 0

    def _to_base36(self, number):
        chars = '0123456789abcdefghijklmnopqrstuvwxyz'
        base36 = ''
        while number:
            number, i = divmod(number, 36)
            base36 = chars[i] + base36
        return base36.zfill(6)  # 确保ID长度为6位

    def generate_id(self):
        self.current_id += 1
        return self._to_base36(self.current_id)
