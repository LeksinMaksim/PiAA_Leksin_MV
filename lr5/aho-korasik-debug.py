class Node:
    def __init__(self):
        self.sons = {}  # Словарь сыновей (символ -> узел)
        self.go = {}    # Словарь переходов (символ -> узел) для ленивой рекурсии
        self.parent = None  # Родительский узел
        self.suffLink = None  # Суффиксная ссылка
        self.up = None  # Сжатая суффиксная ссылка
        self.charToParent = None  # Символ, ведущий к родителю
        self.isLeaf = False  # Флаг терминала
        self.leafPatternNumbers = [] # Номера строк, за которые отвечает терминал
        self.id = None  # Идентификатор для вывода

def addString(root, s, patternNumber):
    # Добавляет строку в бор
    print(f"\n---> Добавление строки '{s}' (образец #{patternNumber}) в бор:")
    cur = root
    path = "Корень"  # Для вывода пути
    
    for i, c in enumerate(s):
        if c not in cur.sons:
            # Создаем новую вершину
            cur.sons[c] = Node()
            cur.sons[c].parent = cur
            cur.sons[c].charToParent = c
            cur.sons[c].id = f"{s[:i+1]}"  # Используем префикс строки как id
            print(f"  Создана новая вершина: {cur.sons[c].id} (добавлен переход '{c}' из '{path}')")
        else:
            print(f"  Вершина для перехода '{c}' из '{path}' уже существует: {cur.sons[c].id}")
        
        cur = cur.sons[c]
        path = cur.id  # Обновляем путь для вывода
    
    cur.isLeaf = True
    cur.leafPatternNumbers.append(patternNumber)
    print(f"  Вершина {cur.id} помечена как терминал для образца #{patternNumber}")

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

def processText(root, text, patterns):
    # Обрабатывает текст и находит все вхождения образцов
    print("\n---> Обработка текста:")
    result = []
    patternOccurrences = {}  # Словарь для хранения вхождений образцов
    
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
            for patternNumber in cur.leafPatternNumbers:
                pattern = patterns[patternNumber-1]
                pos = i - len(pattern) + 2  
                print(f"      Найден образец #{patternNumber} '{pattern}' на позиции {pos}")
                result.append((pos, patternNumber))
                
                # Сохраняем информацию о вхождении для поиска пересечений
                if patternNumber not in patternOccurrences:
                    patternOccurrences[patternNumber] = []
                patternOccurrences[patternNumber].append(pos)
        
        # Проходим по сжатым суффиксным ссылкам
        node = getUp(cur, root)
        up_followed = False
        while node != root:
            up_followed = True
            node_state = "Корень" if node == root else node.id
            print(f"    Переход по сжатой суфф. ссылке: {cur_state} → {node_state}")
            
            if node.isLeaf:
                print(f"      Вершина {node_state} является терминалом:")
                for patternNumber in node.leafPatternNumbers:
                    pattern = patterns[patternNumber-1]
                    pos = i - len(pattern) + 2
                    print(f"        Найден образец #{patternNumber} '{pattern}' на позиции {pos}")
                    result.append((pos, patternNumber))
                    
                    if patternNumber not in patternOccurrences:
                        patternOccurrences[patternNumber] = []
                    patternOccurrences[patternNumber].append(pos)
            
            node = getUp(node, root)
        
        if not up_followed:
            print(f"    Нет переходов по сжатым суфф. ссылкам или переход ведет в корень")
    
    # Находим образцы с пересечениями
    intersectingPatterns = findIntersectingPatterns(patternOccurrences, patterns)
    
    return result, intersectingPatterns

def findIntersectingPatterns(patternOccurrences, patterns):
    # Находит образцы, имеющие пересечения с другими образцами в строке поиска
    print("\n---> Поиск образцов с пересечениями:")
    intersectingPatterns = set()
    
    # Создаем интервалы для каждого вхождения образца
    intervals = []
    for patternNumber, positions in patternOccurrences.items():
        patternLength = len(patterns[patternNumber-1])
        for pos in positions:
            intervals.append((pos, pos + patternLength - 1, patternNumber))
    
    # Сортируем интервалы по начальной позиции
    intervals.sort()
    print(f"  Созданы интервалы вхождений образцов: {intervals}")
    
    # Проверяем пересечения
    for i in range(len(intervals)):
        start1, end1, pattern1 = intervals[i]
        for j in range(i+1, len(intervals)):
            start2, end2, pattern2 = intervals[j]
            
            # Если начало второго интервала за концом первого, то пересечений нет
            if start2 > end1:
                break
                
            # Если есть пересечение и это разные образцы
            if pattern1 != pattern2:
                print(f"  Найдено пересечение образцов #{pattern1} и #{pattern2}:")
                print(f"    Образец #{pattern1}: позиции {start1}-{end1}")
                print(f"    Образец #{pattern2}: позиции {start2}-{end2}")
                intersectingPatterns.add(pattern1)
                intersectingPatterns.add(pattern2)
    
    if not intersectingPatterns:
        print("  Не найдено образцов с пересечениями")
    else:
        print(f"  Образцы с пересечениями: {sorted(list(intersectingPatterns))}")
    
    return sorted(list(intersectingPatterns))

def ahoCorasick(text, patterns):
    # Основная функция алгоритма Ахо-Корасик
    print("\n=== АЛГОРИТМ АХО-КОРАСИК ===")
    print(f"Текст: '{text}'")
    print(f"Образцы: {patterns}")
    
    # Инициализация корня бора
    root = Node()
    root.id = "Корень"
    print("\n--- Шаг 1: Построение бора ---")
    
    # Построение бора
    for i, pattern in enumerate(patterns):
        addString(root, pattern, i+1)
    
    print("\n--- Шаг 2: Построение суффиксных ссылок ---")
    # Вычисляем суффиксные ссылки для всех вершин
    # Выполним обход бора в ширину для построения всех суффиксных ссылок
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
    
    print("\n--- Шаг 3: Построение сжатых суффиксных ссылок ---")
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
    
    print("\n--- Шаг 4: Поиск образцов в тексте ---")
    result, intersectingPatterns = processText(root, text, patterns)
    
    # Сортировка результатов
    result.sort()
    print(f"\nНайденные вхождения (всего {len(result)}): {result}")
    
    return result, verticesCount, intersectingPatterns

text = input().strip()
n = int(input().strip())
patterns = []
for _ in range(n):
    patterns.append(input().strip())

result, verticesCount, intersectingPatterns = ahoCorasick(text, patterns)
print("\n=== РЕЗУЛЬТАТЫ ===")
for pos, patternNumber in result:
    print(pos, patternNumber)

print(f"Количество вершин в автомате: {verticesCount}")
print(f"Образцы с пересечениями: {intersectingPatterns}")
