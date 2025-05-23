def kmp_matcher(text: str, pattern: str) -> list[int]:
    text_length = len(text)
    pattern_length = len(pattern)
    occurrences = []
    
    print("=" * 60)
    print("АЛГОРИТМ КНУТА-МОРРИСА-ПРАТТА")
    print("=" * 60)
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
            occurrences.append(occurrence_pos)
            print(f"  *** НАЙДЕНО ВХОЖДЕНИЕ на позиции {occurrence_pos} ***")
            print(f"  Текст:   {text}")
            print(f"  Паттерн: {' ' * occurrence_pos}{pattern}")
            match_len = pi[pattern_length - 1]
            print(f"  Продолжаем поиск: match_len = pi[{pattern_length - 1}] = {match_len}")
    
    print("\n" + "=" * 60)
    if not occurrences:
        print("Вхождений не найдено")
        return [-1]
    else:
        print(f"Найдено вхождений: {len(occurrences)}")
        print(f"Позиции: {occurrences}")
    
    return occurrences


def compute_prefix_function(pattern: str) -> list[int]:
    pattern_length = len(pattern)
    pi = [0 for _ in range(pattern_length)]
    border_len = 0
    
    print("\nВЫЧИСЛЕНИЕ ПРЕФИКС-ФУНКЦИИ:")
    print("-" * 60)
    print(f"Паттерн: '{pattern}'")
    print(f"Индексы: {' '.join(str(i) for i in range(pattern_length))}")
    print(f"Символы: {' '.join(pattern)}")
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


if __name__ == "__main__":
    print("Введите паттерн:")
    pattern = input()
    print("Введите текст:")
    text = input()
    
    if len(text) < len(pattern):
        print(-1)
    else:
        result = kmp_matcher(text, pattern)
        print("\nРЕЗУЛЬТАТ:")
        print(*result, sep=',')
