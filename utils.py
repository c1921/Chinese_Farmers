chinese_numerals = {
    0: "零", 1: "一", 2: "二", 3: "三", 4: "四", 5: "五",
    6: "六", 7: "七", 8: "八", 9: "九", 10: "十", 100: "百", 1000: "千"
}

def number_to_chinese(num):
    if num <= 10:
        return chinese_numerals[num]
    elif num < 20:
        return chinese_numerals[10] + chinese_numerals[num - 10]
    elif num < 100:
        tens, units = divmod(num, 10)
        return chinese_numerals[tens] + chinese_numerals[10] + (chinese_numerals[units] if units > 0 else "")
    elif num < 1000:
        hundreds, remainder = divmod(num, 100)
        tens, units = divmod(remainder, 10)
        return chinese_numerals[hundreds] + chinese_numerals[100] + (chinese_numerals[tens] + chinese_numerals[10] if tens > 0 else "") + (chinese_numerals[units] if units > 0 else "")
    else:
        raise ValueError("Number too large")
