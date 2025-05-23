def kmp_matcher(text: str, pattern: str) -> int:
    text_length = len(text)
    pattern_length = len(pattern)
    
    print("\nАЛГОРИТМ КМП ДЛЯ ПОИСКА ПАТТЕРНА:")
    print("-" * 60)
    print(f"Текст: '{text}' (длина: {text_length})")
    print(f"Паттерн: '{pattern}' (длина: {pattern_length})")
    print()
    
    pi = compute_prefix_function(pattern)
    print(f"Префикс-функция pi: {pi}")
    print()
    
    print("ПОИСК ПАТТЕРНА В ТЕКСТЕ:")
    print("-" * 60)
    
    match_len = 0
    
    for i in range(text_length):
        print(f"\nПозиция i={i}, символ text[{i}]='{text[i]}'")
        
        while match_len > 0 and pattern[match_len] != text[i]:
            old_match_len = match_len
            match_len = pi[match_len - 1]
            print(f"  Несовпадение: pattern[{old_match_len}]='{pattern[old_match_len]}' != text[{i}]='{text[i]}'")
            print(f"  Откат: match_len = pi[{old_match_len - 1}] = {match_len}")
        
        if pattern[match_len] == text[i]:
            print(f"  Совпадение: pattern[{match_len}]='{pattern[match_len]}' == text[{i}]='{text[i]}'")
            match_len += 1
            print(f"  Увеличиваем match_len до {match_len}")
        else:
            print(f"  Несовпадение: pattern[{match_len}]='{pattern[match_len]}' != text[{i}]='{text[i]}'")
            print(f"  match_len остается 0")
        
        if match_len == pattern_length:
            occurrence_pos = i - pattern_length + 1
            print(f"  *** НАЙДЕНО ПОЛНОЕ СОВПАДЕНИЕ на позиции {occurrence_pos} ***")
            print(f"  Текст:   {text}")
            print(f"  Паттерн: {' ' * occurrence_pos}{pattern}")
            return occurrence_pos
    
    print("\nПолное совпадение не найдено")
    return -1


def compute_prefix_function(pattern: str) -> list[int]:
    pattern_length = len(pattern)
    pi = [0 for _ in range(pattern_length)]
    border_len = 0
    
    print("\nВЫЧИСЛЕНИЕ ПРЕФИКС-ФУНКЦИИ:")
    print("-" * 40)
    print(f"Паттерн: '{pattern}'")
    print(f"Индексы: {' '.join(f'{i:2}' for i in range(pattern_length))}")
    print(f"Символы: {' '.join(f'{c:2}' for c in pattern)}")
    print()
    
    print("pi[0] = 0 (по определению)")
    
    for i in range(1, pattern_length):
        print(f"\nВычисляем pi[{i}] для символа '{pattern[i]}':")
        
        while border_len > 0 and pattern[border_len] != pattern[i]:
            print(f"  pattern[{border_len}]='{pattern[border_len]}' != pattern[{i}]='{pattern[i]}'")
            old_border = border_len
            border_len = pi[border_len - 1]
            print(f"  Откат: border_len = pi[{old_border - 1}] = {border_len}")
        
        if pattern[border_len] == pattern[i]:
            print(f"  pattern[{border_len}]='{pattern[border_len]}' == pattern[{i}]='{pattern[i]}'")
            border_len += 1
            print(f"  Увеличиваем border_len до {border_len}")
        else:
            print(f"  pattern[{border_len}]='{pattern[border_len]}' != pattern[{i}]='{pattern[i]}'")
            print(f"  border_len остается 0")
        
        pi[i] = border_len
        print(f"  pi[{i}] = {border_len}")
        
        print(f"  Текущий массив pi: {pi[:i+1]}")
    
    print(f"\nИтоговая префикс-функция: {pi}")
    return pi


def check_cyclic_shift(str1: str, str2: str) -> int:
    print("=" * 80)
    print("ПРОВЕРКА ЦИКЛИЧЕСКОГО СДВИГА")
    print("=" * 80)
    print(f"Строка 1 (str1): '{str1}'")
    print(f"Строка 2 (str2): '{str2}'")
    print()
    
    if len(str1) != len(str2):
        print("РЕЗУЛЬТАТ: Строки имеют разную длину!")
        print(f"Длина str1: {len(str1)}, длина str2: {len(str2)}")
        return -1
    
    print(f"Длины строк совпадают: {len(str1)}")
    
    if str1 == str2:
        print("РЕЗУЛЬТАТ: Строки идентичны! Сдвиг = 0")
        return 0
    
    print("\nСтроки не идентичны, проверяем циклический сдвиг...")
    print("\nМЕТОД: Удваиваем первую строку и ищем вторую строку в ней")
    
    doubled_str1 = str1 + str1
    print(f"Удвоенная str1: '{doubled_str1}'")
    print()
    
    print("Визуализация возможных циклических сдвигов str1:")
    for i in range(len(str1)):
        shifted = str1[i:] + str1[:i]
        print(f"  Сдвиг на {i:2}: '{shifted}'")
        if shifted == str2:
            print(f"             ^ Совпадает с str2!")
    
    print("\nЗапускаем поиск str2 в удвоенной str1...")
    result = kmp_matcher(doubled_str1, str2)
    
    print("\n" + "=" * 80)
    if result != -1:
        print(f"РЕЗУЛЬТАТ: str2 является циклическим сдвигом str1 на {result} позиций!")
        print(f"Проверка: str1[{result}:] + str1[:{result}] = '{str1[result:] + str1[:result]}' == str2")
    else:
        print("РЕЗУЛЬТАТ: str2 НЕ является циклическим сдвигом str1")
    
    return result


if __name__ == "__main__":
    str2 = input()
    str1 = input()
    
    result = check_cyclic_shift(str2, str1)
    print(f"\nИТОГОВЫЙ ОТВЕТ: {result}")
