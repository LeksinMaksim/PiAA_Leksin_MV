def minCostTransform(StringA, StringB, replaceCost, insertCost, deleteCost, debug=False):
    m, n = len(StringA), len(StringB)
    
    dpTable = [[0] * (n + 1) for _ in range(m + 1)]
    
    if debug:
        print("\n=== ИНИЦИАЛИЗАЦИЯ ТАБЛИЦЫ DP ===")
        print("Исходная строка:", StringA)
        print("Целевая строка:", StringB)
        print("Стоимость операций: Замена={}, Вставка={}, Удаление={}".format(
            replaceCost, insertCost, deleteCost))
    
    for i in range(1, m + 1):
        dpTable[i][0] = dpTable[i-1][0] + deleteCost
        if debug:
            print(f"Инициализация: dpTable[{i}][0] = {dpTable[i][0]} (удаление символа '{StringA[i-1]}')")
    
    for j in range(1, n + 1):
        dpTable[0][j] = dpTable[0][j-1] + insertCost
        if debug:
            print(f"Инициализация: dpTable[0][{j}] = {dpTable[0][j]} (вставка символа '{StringB[j-1]}')")
    
    if debug:
        print("\n=== ЗАПОЛНЕНИЕ ТАБЛИЦЫ DP ===")
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if StringA[i-1] == StringB[j-1]:
                dpTable[i][j] = dpTable[i-1][j-1]
                if debug:
                    print(f"Символы '{StringA[i-1]}' и '{StringB[j-1]}' совпадают: dpTable[{i}][{j}] = {dpTable[i][j]}")
            else:
                replaceOption = dpTable[i-1][j-1] + replaceCost
                deleteOption = dpTable[i-1][j] + deleteCost
                insertOption = dpTable[i][j-1] + insertCost
                
                dpTable[i][j] = min(replaceOption, deleteOption, insertOption)
                
                if debug:
                    print(f"Символы '{StringA[i-1]}' и '{StringB[j-1]}' не совпадают:")
                    print(f"  Вариант замены: {dpTable[i-1][j-1]} + {replaceCost} = {replaceOption}")
                    print(f"  Вариант удаления: {dpTable[i-1][j]} + {deleteCost} = {deleteOption}")
                    print(f"  Вариант вставки: {dpTable[i][j-1]} + {insertCost} = {insertOption}")
                    print(f"  Выбран минимальный вариант: dpTable[{i}][{j}] = {dpTable[i][j]}")
    
    operations = []
    i, j = m, n
    
    if debug:
        print("\n=== ОБРАТНЫЙ ПРОХОД ДЛЯ НАХОЖДЕНИЯ ПОСЛЕДОВАТЕЛЬНОСТИ ОПЕРАЦИЙ ===")
        print(f"Начинаем с позиции ({i}, {j})")
    
    while i > 0 or j > 0:
        if i > 0 and j > 0 and StringA[i-1] == StringB[j-1]:
            operations.append('M')
            if debug:
                print(f"Символы '{StringA[i-1]}' и '{StringB[j-1]}' совпадают: операция 'M' (совпадение)")
                print(f"Переходим к позиции ({i-1}, {j-1})")
            i -= 1
            j -= 1
        elif i > 0 and j > 0 and dpTable[i][j] == dpTable[i-1][j-1] + replaceCost:
            operations.append('R')
            if debug:
                print(f"Заменяем символ '{StringA[i-1]}' на '{StringB[j-1]}': операция 'R' (замена)")
                print(f"Переходим к позиции ({i-1}, {j-1})")
            i -= 1
            j -= 1
        elif j > 0 and dpTable[i][j] == dpTable[i][j-1] + insertCost:
            operations.append('I')
            if debug:
                print(f"Вставляем символ '{StringB[j-1]}': операция 'I' (вставка)")
                print(f"Переходим к позиции ({i}, {j-1})")
            j -= 1
        elif i > 0 and dpTable[i][j] == dpTable[i-1][j] + deleteCost:
            operations.append('D')
            if debug:
                print(f"Удаляем символ '{StringA[i-1]}': операция 'D' (удаление)")
                print(f"Переходим к позиции ({i-1}, {j})")
            i -= 1
        else:
            if debug:
                print("Что-то пошло не так, выходим из цикла")
            break
    
    operations.reverse()
    operationsString = ''.join(operations)
    
    if debug:
        print("\n=== РЕЗУЛЬТАТ ===")
        print(f"Последовательность операций: {operationsString}")
        print(f"Исходная строка: {StringA}")
        print(f"Целевая строка: {StringB}")
        
        print("\n=== ВИЗУАЛИЗАЦИЯ ПРОЦЕССА ПРЕОБРАЗОВАНИЯ ===")
        currentString = ""
        posA = 0
        posB = 0
        
        for op in operationsString:
            if op == 'M':
                currentString += StringA[posA]
                print(f"Совпадение: '{StringA[posA]}' остаётся без изменений")
                posA += 1
                posB += 1
            elif op == 'R':
                currentString += StringB[posB]
                print(f"Замена: '{StringA[posA]}' -> '{StringB[posB]}'")
                posA += 1
                posB += 1
            elif op == 'I':
                currentString += StringB[posB]
                print(f"Вставка: добавляем '{StringB[posB]}'")
                posB += 1
            elif op == 'D':
                print(f"Удаление: удаляем '{StringA[posA]}'")
                posA += 1
            
            print(f"Текущая строка: {currentString}")
        
        print(f"\nИтоговая строка: {currentString}")
        print(f"Целевая строка:  {StringB}")
        assert currentString == StringB, "Ошибка в преобразовании!"
    
    return operationsString


def findLcsLength(StringA, StringB, debug=False):
    """Функция для нахождения длины наибольшей общей подпоследовательности"""
    m, n = len(StringA), len(StringB)
    lcsTable = [[0] * (n + 1) for _ in range(m + 1)]
    
    if debug:
        print("\n=== АЛГОРИТМ НАХОЖДЕНИЯ НАИБОЛЬШЕЙ ОБЩЕЙ ПОДПОСЛЕДОВАТЕЛЬНОСТИ ===")
        print("Строка A:", StringA)
        print("Строка B:", StringB)
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if StringA[i-1] == StringB[j-1]:
                lcsTable[i][j] = lcsTable[i-1][j-1] + 1
                if debug:
                    print(f"Символы '{StringA[i-1]}' и '{StringB[j-1]}' совпадают: lcsTable[{i}][{j}] = {lcsTable[i][j]}")
            else:
                lcsTable[i][j] = max(lcsTable[i-1][j], lcsTable[i][j-1])
                if debug:
                    print(f"Символы '{StringA[i-1]}' и '{StringB[j-1]}' не совпадают:")
                    print(f"  Макс. из: lcsTable[{i-1}][{j}]={lcsTable[i-1][j]} и lcsTable[{i}][{j-1}]={lcsTable[i][j-1]}")
                    print(f"  Результат: lcsTable[{i}][{j}] = {lcsTable[i][j]}")
    
    if debug:

        i, j = m, n
        lcs = []
        
        print("\n=== ВОССТАНОВЛЕНИЕ НОП ===")
        while i > 0 and j > 0:
            if StringA[i-1] == StringB[j-1]:
                lcs.append(StringA[i-1])
                print(f"Символы совпадают: '{StringA[i-1]}' добавляем в НОП")
                i -= 1
                j -= 1
            elif lcsTable[i-1][j] >= lcsTable[i][j-1]:
                print(f"Пропускаем символ '{StringA[i-1]}' в строке A")
                i -= 1
            else:
                print(f"Пропускаем символ '{StringB[j-1]}' в строке B")
                j -= 1
                
        lcs.reverse()
        print(f"\nНайденная НОП: {''.join(lcs)}")
        print(f"Длина НОП: {lcsTable[m][n]}")
    
    return lcsTable[m][n]


def main():
    costs = list(map(int, input().split()))
    replaceCost, insertCost, deleteCost = costs
    
    StringA = input().strip()
    StringB = input().strip()
    
    debug = True 
    
    operations = minCostTransform(StringA, StringB, replaceCost, insertCost, deleteCost, debug)
    
    lcsLength = findLcsLength(StringA, StringB, debug)
    
    print("\n=== ИТОГОВЫЙ РЕЗУЛЬТАТ ===")
    print(operations)
    print(StringA)
    print(StringB)
    print(f"Длина наибольшей общей подпоследовательности: {lcsLength}")


if __name__ == "__main__":
    main()
