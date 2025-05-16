class Node:
    def __init__(self):
        self.sons = {}  # Словарь сыновей
        self.go = {}    # Словарь переходов
        self.parent = None  # Родительский узел
        self.suffLink = None  # Суффиксная ссылка
        self.up = None  # Сжатая суффиксная ссылка
        self.charToParent = None  # Символ, ведущий к родителю
        self.isLeaf = False  # Флаг терминала
        self.leafPatternNumbers = []  # Номера строк и их стартовые позиции
        self.id = None  # Уникальный идентификатор для вывода

def addString(root, s, patternNumber, startPos):
    # Добавляет строку в бор с информацией о стартовой позиции в шаблоне
    print(f"\n---> Добавление подстроки '{s}' (образец #{patternNumber}, поз. {startPos}) в бор:")
    cur = root
    path = "Корень"  # Для вывода пути
    
    for i, c in enumerate(s):
        if c not in cur.sons:
            # Создаем новую вершину
            cur.sons[c] = Node()
            cur.sons[c].parent = cur
            cur.sons[c].charToParent = c
            cur.sons[c].id = f"П{patternNumber}_{startPos}_{s[:i+1]}"  # Используем префикс строки как id
            print(f"  Создана новая вершина: {cur.sons[c].id} (добавлен переход '{c}' из '{path}')")
        else:
            print(f"  Вершина для перехода '{c}' из '{path}' уже существует: {cur.sons[c].id}")
        
        cur = cur.sons[c]
        path = cur.id  # Обновляем путь для вывода
    
    cur.isLeaf = True
    cur.leafPatternNumbers.append((patternNumber, startPos))
    print(f"  Вершина {cur.id} помечена как терминал для подстроки #{patternNumber} с позиции {startPos}")

def getSuffLink(v, root):
    # Вычисляет суффиксную ссылку для вершины v
    if v.suffLink is None:
        # Если суффиксная ссылка еще не вычислена
        if v == root or v.parent == root:
            v.suffLink = root
            if v != root:
                print(f"  Суффиксная ссылка для {v.id}: → Корень (родитель вершины - корень)")
        else:
            v.suffLink = getLink(getSuffLink(v.parent, root), v.charToParent, root)
            print(f"  Суффиксная ссылка для {v.id}: → {v.suffLink.id}")
    return v.suffLink

def getLink(v, c, root):
    # Вычисляет переход из вершины v по символу c
    if c not in v.go:
        # Если переход еще не вычислен
        v_id = "Корень" if v == root else v.id
        
        if c in v.sons:
            v.go[c] = v.sons[c]
            print(f"  Переход из {v_id} по символу '{c}': → {v.sons[c].id} (прямой переход)")
        elif v == root:
            v.go[c] = root
            print(f"  Переход из Корня по символу '{c}': → Корень (нет перехода, остаемся в корне)")
        else:
            v.go[c] = getLink(getSuffLink(v, root), c, root)
            dest_id = "Корень" if v.go[c] == root else v.go[c].id
            print(f"  Переход из {v_id} по символу '{c}': → {dest_id} (через суффиксную ссылку)")
    return v.go[c]

def getUp(v, root):
    # Вычисляет сжатую суффиксную ссылку для вершины v
    if v.up is None:
        v_id = "Корень" if v == root else v.id
        suffLink = getSuffLink(v, root)
        suffLink_id = "Корень" if suffLink == root else suffLink.id
        
        if suffLink.isLeaf:
            v.up = suffLink
            print(f"  Сжатая суфф. ссылка для {v_id}: → {suffLink_id} (терминальная вершина)")
        elif suffLink == root:
            v.up = root
            print(f"  Сжатая суфф. ссылка для {v_id}: → Корень (суфф. ссылка - корень)")
        else:
            v.up = getUp(suffLink, root)
            up_id = "Корень" if v.up == root else v.up.id
            print(f"  Сжатая суфф. ссылка для {v_id}: → {up_id} (через сжатую суфф. ссылку родителя)")
    return v.up

def countVertices(root):
    # Подсчитывает количество вершин в автомате
    if not root:
        return 0
    
    print("\n---> Подсчет вершин в автомате:")
    visited = set()
    queue = [root]
    
    # Обход в ширину для подсчета вершин
    while queue:
        node = queue.pop(0)
        if node in visited:
            continue
        
        visited.add(node)
        node_id = "Корень" if node == root else node.id
        print(f"  Посещена вершина: {node_id}")
        
        for c, child in node.sons.items():
            if child not in visited:
                queue.append(child)
                child_id = "Корень" if child == root else child.id
                print(f"    Добавлен в очередь потомок: {child_id} (по символу '{c}')")
    
    print(f"  Всего вершин: {len(visited)}")
    return len(visited)

def findPatternWithJoker(text, pattern, joker):
    # Находит все вхождения шаблона с джокером в текст
    print("\n=== АЛГОРИТМ ПОИСКА ОБРАЗЦА С ДЖОКЕРОМ ===")
    print(f"Текст: '{text}'")
    print(f"Шаблон: '{pattern}'")
    print(f"Джокер: '{joker}'")
    
    # Разбиваем шаблон на подстроки без джокеров
    print("\n--- Шаг 1: Разбиение шаблона на подстроки без джокеров ---")
    substrings = []
    currentSubstring = ""
    currentStart = 0
    
    for i, c in enumerate(pattern):
        if c == joker:
            if currentSubstring:
                substrings.append((currentSubstring, currentStart))
                print(f"  Найдена подстрока: '{currentSubstring}' (начинается с позиции {currentStart})")
                currentSubstring = ""
            currentStart = i + 1
            print(f"  Встречен джокер на позиции {i}, следующая подстрока начнется с позиции {currentStart}")
        else:
            if not currentSubstring:
                currentStart = i
                print(f"  Начинаем собирать новую подстроку с позиции {i}")
            currentSubstring += c
    
    if currentSubstring:
        substrings.append((currentSubstring, currentStart))
        print(f"  Найдена подстрока: '{currentSubstring}' (начинается с позиции {currentStart})")
    
    # Если нет подстрок (только джокеры), завершаем работу
    if not substrings:
        print("  Шаблон состоит только из джокеров, поиск невозможен")
        return [], 0, []
    
    print(f"  Итого подстрок без джокеров: {len(substrings)}")
    
    # Строим автомат Ахо-Корасик для подстрок
    print("\n--- Шаг 2: Построение бора для подстрок ---")
    root = Node()
    root.id = "Корень"
    for i, (substring, pos) in enumerate(substrings):
        addString(root, substring, i, pos)
    
    print("\n--- Шаг 3: Построение суффиксных ссылок ---")
    # Вычисляем суффиксные ссылки для всех вершин
    queue = [root]
    visited = set([root])
    
    while queue:
        node = queue.pop(0)
        # Вычисляем суффиксную ссылку для текущей вершины
        if node != root:
            getSuffLink(node, root)
        
        # Добавляем потомков в очередь
        for child in node.sons.values():
            if child not in visited:
                queue.append(child)
                visited.add(child)
    
    print("\n--- Шаг 4: Построение сжатых суффиксных ссылок ---")
    # Вычисляем сжатые суффиксные ссылки для всех вершин
    queue = [root]
    visited = set([root])
    
    while queue:
        node = queue.pop(0)
        # Вычисляем сжатую суффиксную ссылку для текущей вершины
        if node != root:
            getUp(node, root)
        
        # Добавляем потомков в очередь
        for child in node.sons.values():
            if child not in visited:
                queue.append(child)
                visited.add(child)
    
    # Подсчет количества вершин в автомате
    verticesCount = countVertices(root)
    
    print("\n--- Шаг 5: Поиск подстрок в тексте ---")
    # Обрабатываем текст
    occurrences = processText(root, text, substrings)
    
    print("\n--- Шаг 6: Проверка полных совпадений шаблона ---")
    # Находим позиции, где все подстроки найдены
    result = []
    patternOccurrences = {}  # Для хранения информации о пересечениях
    
    for i in range(len(text) - len(pattern) + 1):
        # Проверяем, найдены ли все подстроки на данной позиции
        found_count = len(occurrences[i]) if i < len(occurrences) else 0
        
        if found_count == len(substrings):
            print(f"  Позиция {i}: найдены все {len(substrings)} подстроки")
            
            # Проверяем, найдены ли все уникальные подстроки
            foundSubstrings = set(occurrences[i])
            if len(foundSubstrings) == len(substrings):
                print(f"    Все уникальные подстроки найдены")
                
                # Проверяем точное соответствие шаблону (с учетом джокеров)
                match = True
                for j in range(len(pattern)):
                    if i + j >= len(text):
                        match = False
                        print(f"    Выход за пределы текста на позиции {i+j}")
                        break
                    if pattern[j] != joker and pattern[j] != text[i + j]:
                        match = False
                        print(f"    Несовпадение на позиции {i+j}: шаблон '{pattern[j]}', текст '{text[i+j]}'")
                        break
                
                if match:
                    pos = i + 1  # +1 для нумерации с 1
                    print(f"    ПОЛНОЕ СОВПАДЕНИЕ: шаблон найден на позиции {pos}")
                    result.append(pos)
                    
                    # Сохраняем информацию о вхождениях для поиска пересечений
                    patternOccurrences[1] = patternOccurrences.get(1, []) + [pos]
        elif i < len(occurrences) and occurrences[i]:
            print(f"  Позиция {i}: найдено {len(occurrences[i])} подстрок из {len(substrings)}")
    
    # Поскольку у нас только один шаблон, пересечения возможны только между его вхождениями
    print("\n--- Шаг 7: Поиск пересечений шаблонов ---")
    intersectingPatterns = findIntersectingPatterns(patternOccurrences, [pattern])
    
    return result, verticesCount, intersectingPatterns

def processText(root, text, substrings):
    # Обрабатывает текст и находит вхождения подстрок
    # Создаем список словарей для каждой позиции в тексте
    # В списке будем хранить найденные подстроки
    occurrences = [[] for _ in range(len(text) + 1)]
    
    cur = root
    print(f"  Начинаем с корня бора")
    
    for i, c in enumerate(text):
        # Переход по символу текста
        prev_state = "Корень" if cur == root else cur.id
        cur = getLink(cur, c, root)
        cur_state = "Корень" if cur == root else cur.id
        print(f"  Символ текста[{i}] = '{c}': {prev_state} → {cur_state}")
        
        # Проверяем текущий узел на наличие терминалов
        if cur.isLeaf:
            print(f"    Вершина {cur_state} является терминалом:")
            for substringIdx, startInPattern in cur.leafPatternNumbers:
                substring, _ = substrings[substringIdx]
                # Вычисляем позицию начала подстроки в тексте
                substringStart = i - len(substring) + 1
                # Вычисляем позицию начала шаблона
                patternStart = substringStart - startInPattern
                if patternStart >= 0:
                    print(f"      Найдена подстрока #{substringIdx} '{substring}' с началом шаблона на позиции {patternStart}")
                    occurrences[patternStart].append(substringIdx)
        
        # Проходим по сжатым суффиксным ссылкам
        node = getUp(cur, root)
        up_followed = False
        while node != root:
            up_followed = True
            node_state = "Корень" if node == root else node.id
            print(f"    Переход по сжатой суфф. ссылке: {cur_state} → {node_state}")
            
            if node.isLeaf:
                print(f"      Вершина {node_state} является терминалом:")
                for substringIdx, startInPattern in node.leafPatternNumbers:
                    substring, _ = substrings[substringIdx]
                    substringStart = i - len(substring) + 1
                    patternStart = substringStart - startInPattern
                    if patternStart >= 0:
                        print(f"        Найдена подстрока #{substringIdx} '{substring}' с началом шаблона на позиции {patternStart}")
                        occurrences[patternStart].append(substringIdx)
            
            node = getUp(node, root)
        
        if not up_followed:
            print(f"    Нет переходов по сжатым суфф. ссылкам или переход ведет в корень")
    
    return occurrences

def findIntersectingPatterns(patternOccurrences, patterns):
    # Находит образцы, имеющие пересечения с другими образцами в строке поиска
    print("\n---> Поиск образцов с пересечениями:")
    intersectingPatterns = set()
    
    # Если только один шаблон, проверяем пересечения между его вхождениями
    if len(patternOccurrences) == 1:
        patternNumber = list(patternOccurrences.keys())[0]
        positions = patternOccurrences[patternNumber]
        patternLength = len(patterns[patternNumber-1])
        
        # Создаем интервалы для вхождений
        intervals = [(pos, pos + patternLength - 1) for pos in positions]
        print(f"  Интервалы вхождений шаблона: {intervals}")
        
        # Сортируем интервалы
        intervals.sort()
        
        # Проверяем пересечения
        for i in range(len(intervals) - 1):
            _, end1 = intervals[i]
            start2, _ = intervals[i+1]
            
            if start2 <= end1:
                # Есть пересечение
                print(f"  Найдено пересечение между вхождениями шаблона:")
                print(f"    Вхождение на позиции {intervals[i][0]}: до позиции {end1}")
                print(f"    Вхождение на позиции {start2}: начинается до окончания предыдущего")
                intersectingPatterns.add(patternNumber)
                break
    
    if not intersectingPatterns:
        print("  Не найдено образцов с пересечениями")
    else:
        print(f"  Образцы с пересечениями: {sorted(list(intersectingPatterns))}")
    
    return sorted(list(intersectingPatterns))

text = input().strip()
pattern = input().strip()
joker = input().strip()

result, verticesCount, intersectingPatterns = findPatternWithJoker(text, pattern, joker)
print("\n=== РЕЗУЛЬТАТЫ ===")
for pos in result:
    print(pos)

print(f"Количество вершин в автомате: {verticesCount}")
print(f"Образцы с пересечениями: {intersectingPatterns}")
