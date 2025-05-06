def levenshteinDistance(sourceString, targetString, debug=False):
    m, n = len(sourceString), len(targetString)
    dpTable = [[0] * (n + 1) for _ in range(m + 1)]
    
    if debug:
        print("\n=== РАССТОЯНИЕ ЛЕВЕНШТЕЙНА ===")
        print("Исходная строка:", sourceString)
        print("Целевая строка:", targetString)
        print("Все операции имеют стоимость 1")
    
    for i in range(1, m + 1):
        dpTable[i][0] = i
        if debug:
            print(f"Инициализация: dpTable[{i}][0] = {i} (удаление {i} символов)")
    
    for j in range(1, n + 1):
        dpTable[0][j] = j
        if debug:
            print(f"Инициализация: dpTable[0][{j}] = {j} (вставка {j} символов)")
    
    if debug:
        print("\n=== ЗАПОЛНЕНИЕ ТАБЛИЦЫ DP ===")
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if sourceString[i-1] == targetString[j-1]:
                dpTable[i][j] = dpTable[i-1][j-1]
                if debug:
                    print(f"Символы '{sourceString[i-1]}' и '{targetString[j-1]}' совпадают: dpTable[{i}][{j}] = {dpTable[i][j]}")
            else:
                replaceOption = dpTable[i-1][j-1] + 1
                deleteOption = dpTable[i-1][j] + 1
                insertOption = dpTable[i][j-1] + 1
                
                dpTable[i][j] = min(replaceOption, deleteOption, insertOption)
                
                if debug:
                    print(f"Символы '{sourceString[i-1]}' и '{targetString[j-1]}' не совпадают:")
                    print(f"  Вариант замены: {dpTable[i-1][j-1]} + 1 = {replaceOption}")
                    print(f"  Вариант удаления: {dpTable[i-1][j]} + 1 = {deleteOption}")
                    print(f"  Вариант вставки: {dpTable[i][j-1]} + 1 = {insertOption}")
                    operation = ""
                    if dpTable[i][j] == replaceOption:
                        operation = "замена"
                    elif dpTable[i][j] == deleteOption:
                        operation = "удаление"
                    else:
                        operation = "вставка"
                    print(f"  Выбран минимальный вариант ({operation}): dpTable[{i}][{j}] = {dpTable[i][j]}")
    
    if debug:
        print("\n=== ВОССТАНОВЛЕНИЕ ПОСЛЕДОВАТЕЛЬНОСТИ ОПЕРАЦИЙ ===")
        operations = []
        i, j = m, n
        
        while i > 0 or j > 0:
            if i > 0 and j > 0 and sourceString[i-1] == targetString[j-1]:
                operations.append(('M', i-1, j-1))
                print(f"Символы '{sourceString[i-1]}' и '{targetString[j-1]}' совпадают - нет операции")
                i -= 1
                j -= 1
            elif i > 0 and j > 0 and dpTable[i][j] == dpTable[i-1][j-1] + 1:
                operations.append(('R', i-1, j-1))
                print(f"Заменяем символ '{sourceString[i-1]}' на '{targetString[j-1]}'")
                i -= 1
                j -= 1
            elif j > 0 and dpTable[i][j] == dpTable[i][j-1] + 1:
                operations.append(('I', i, j-1))
                print(f"Вставляем символ '{targetString[j-1]}'")
                j -= 1
            elif i > 0 and dpTable[i][j] == dpTable[i-1][j] + 1:
                operations.append(('D', i-1, j))
                print(f"Удаляем символ '{sourceString[i-1]}'")
                i -= 1
            else:
                print("Что-то пошло не так, выходим из цикла")
                break
        
        operations.reverse()
        
        print("\n=== ВИЗУАЛИЗАЦИЯ ПРОЦЕССА ТРАНСФОРМАЦИИ ===")
        currentString = ""
        
        for op, i, j in operations:
            if op == 'M':
                currentString += sourceString[i]
                print(f"Сохраняем символ '{sourceString[i]}': {currentString}")
            elif op == 'R':
                currentString += targetString[j]
                print(f"Заменяем '{sourceString[i]}' на '{targetString[j]}': {currentString}")
            elif op == 'I':
                currentString += targetString[j]
                print(f"Вставляем символ '{targetString[j]}': {currentString}")
            elif op == 'D':
                print(f"Удаляем символ '{sourceString[i]}': {currentString}")
        
        print(f"\nИтоговая строка: {currentString}")
        print(f"Целевая строка:  {targetString}")
        print(f"\nРасстояние Левенштейна: {dpTable[m][n]}")
    
    return dpTable[m][n]


def findLcsLength(sourceString, targetString, debug=False):
    """Функция для нахождения длины наибольшей общей подпоследовательности"""
    m, n = len(sourceString), len(targetString)
    lcsTable = [[0] * (n + 1) for _ in range(m + 1)]
    
    if debug:
        print("\n=== АЛГОРИТМ НАХОЖДЕНИЯ НАИБОЛЬШЕЙ ОБЩЕЙ ПОДПОСЛЕДОВАТЕЛЬНОСТИ ===")
        print("Строка A:", sourceString)
        print("Строка B:", targetString)
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if sourceString[i-1] == targetString[j-1]:
                lcsTable[i][j] = lcsTable[i-1][j-1] + 1
                if debug:
                    print(f"Символы '{sourceString[i-1]}' и '{targetString[j-1]}' совпадают: lcsTable[{i}][{j}] = {lcsTable[i][j]}")
            else:
                lcsTable[i][j] = max(lcsTable[i-1][j], lcsTable[i][j-1])
                if debug:
                    print(f"Символы '{sourceString[i-1]}' и '{targetString[j-1]}' не совпадают:")
                    print(f"  Макс. из: lcsTable[{i-1}][{j}]={lcsTable[i-1][j]} и lcsTable[{i}][{j-1}]={lcsTable[i][j-1]}")
                    print(f"  Результат: lcsTable[{i}][{j}] = {lcsTable[i][j]}")
    
    if debug:
        
        i, j = m, n
        lcs = []
        
        print("\n=== ВОССТАНОВЛЕНИЕ НОП ===")
        while i > 0 and j > 0:
            if sourceString[i-1] == targetString[j-1]:
                lcs.append(sourceString[i-1])
                print(f"Символы совпадают: '{sourceString[i-1]}' добавляем в НОП")
                i -= 1
                j -= 1
            elif lcsTable[i-1][j] >= lcsTable[i][j-1]:
                print(f"Пропускаем символ '{sourceString[i-1]}' в строке A")
                i -= 1
            else:
                print(f"Пропускаем символ '{targetString[j-1]}' в строке B")
                j -= 1
                
        lcs.reverse()
        print(f"\nНайденная НОП: {''.join(lcs)}")
        print(f"Длина НОП: {lcsTable[m][n]}")
    
    return lcsTable[m][n]


def main():
    sourceString = input().strip()
    targetString = input().strip()
    
    debug = True
    
    result = levenshteinDistance(sourceString, targetString, debug)
    
    print("\n=== ИТОГОВЫЙ РЕЗУЛЬТАТ ===")
    print(result)
    
    lcsLength = findLcsLength(sourceString, targetString, debug)
    print(f"Длина наибольшей общей подпоследовательности: {lcsLength}")


if __name__ == "__main__":
    main()
