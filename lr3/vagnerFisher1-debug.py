def minCostTransform(stringA, stringB, replaceCost, insertCost, deleteCost, debug=False):
    m, n = len(stringA), len(stringB)
    dpTable = [[0] * (n + 1) for _ in range(m + 1)]
    
    if debug:
        print("\n=== ИНИЦИАЛИЗАЦИЯ ТАБЛИЦЫ DP ===")
        print("Строка A:", stringA)
        print("Строка B:", stringB)
        print("Стоимость операций: Замена={}, Вставка={}, Удаление={}".format(
            replaceCost, insertCost, deleteCost))
    
    for i in range(1, m + 1):
        dpTable[i][0] = dpTable[i-1][0] + deleteCost
        if debug:
            print(f"Инициализация: dpTable[{i}][0] = {dpTable[i][0]} (удаление символа '{stringA[i-1]}')")
    
    for j in range(1, n + 1):
        dpTable[0][j] = dpTable[0][j-1] + insertCost
        if debug:
            print(f"Инициализация: dpTable[0][{j}] = {dpTable[0][j]} (вставка символа '{stringB[j-1]}')")
    
    if debug:
        print("\n=== ЗАПОЛНЕНИЕ ТАБЛИЦЫ DP ===")
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if stringA[i-1] == stringB[j-1]:
                dpTable[i][j] = dpTable[i-1][j-1]
                if debug:
                    print(f"Символы '{stringA[i-1]}' и '{stringB[j-1]}' совпадают: dpTable[{i}][{j}] = {dpTable[i][j]}")
            else:
                replaceOption = dpTable[i-1][j-1] + replaceCost
                deleteOption = dpTable[i-1][j] + deleteCost
                insertOption = dpTable[i][j-1] + insertCost
                
                dpTable[i][j] = min(replaceOption, deleteOption, insertOption)
                
                if debug:
                    print(f"Символы '{stringA[i-1]}' и '{stringB[j-1]}' не совпадают:")
                    print(f"  Вариант замены: {dpTable[i-1][j-1]} + {replaceCost} = {replaceOption}")
                    print(f"  Вариант удаления: {dpTable[i-1][j]} + {deleteCost} = {deleteOption}")
                    print(f"  Вариант вставки: {dpTable[i][j-1]} + {insertCost} = {insertOption}")
                    print(f"  Выбран минимальный вариант: dpTable[{i}][{j}] = {dpTable[i][j]}")
    
    if debug:
        print(f"\nМинимальная стоимость преобразования: {dpTable[m][n]}")
    
    return dpTable[m][n]


def findLcsLength(stringA, stringB, debug=False):
    """Функция для нахождения длины наибольшей общей подпоследовательности"""
    m, n = len(stringA), len(stringB)
    lcsTable = [[0] * (n + 1) for _ in range(m + 1)]
    
    if debug:
        print("\n=== АЛГОРИТМ НАХОЖДЕНИЯ НАИБОЛЬШЕЙ ОБЩЕЙ ПОДПОСЛЕДОВАТЕЛЬНОСТИ ===")
        print("Строка A:", stringA)
        print("Строка B:", stringB)
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if stringA[i-1] == stringB[j-1]:
                lcsTable[i][j] = lcsTable[i-1][j-1] + 1
                if debug:
                    print(f"Символы '{stringA[i-1]}' и '{stringB[j-1]}' совпадают: lcsTable[{i}][{j}] = {lcsTable[i][j]}")
            else:
                lcsTable[i][j] = max(lcsTable[i-1][j], lcsTable[i][j-1])
                if debug:
                    print(f"Символы '{stringA[i-1]}' и '{stringB[j-1]}' не совпадают:")
                    print(f"  Макс. из: lcsTable[{i-1}][{j}]={lcsTable[i-1][j]} и lcsTable[{i}][{j-1}]={lcsTable[i][j-1]}")
                    print(f"  Результат: lcsTable[{i}][{j}] = {lcsTable[i][j]}")
    
    if debug:
        
        i, j = m, n
        lcs = []
        
        print("\n=== ВОССТАНОВЛЕНИЕ НОП ===")
        while i > 0 and j > 0:
            if stringA[i-1] == stringB[j-1]:
                lcs.append(stringA[i-1])
                print(f"Символы совпадают: '{stringA[i-1]}' добавляем в НОП")
                i -= 1
                j -= 1
            elif lcsTable[i-1][j] >= lcsTable[i][j-1]:
                print(f"Пропускаем символ '{stringA[i-1]}' в строке A")
                i -= 1
            else:
                print(f"Пропускаем символ '{stringB[j-1]}' в строке B")
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
    
    result = minCostTransform(StringA, StringB, replaceCost, insertCost, deleteCost, debug)
    
    lcsLength = findLcsLength(StringA, StringB, debug)
    
    print("\n=== ИТОГОВЫЙ РЕЗУЛЬТАТ ===")
    print(result)
    print(f"Длина наибольшей общей подпоследовательности: {lcsLength}")


if __name__ == "__main__":
    main()
