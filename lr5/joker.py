class Node:
    def __init__(self):
        self.sons = {}
        self.go = {}
        self.parent = None
        self.suffLink = None
        self.up = None
        self.charToParent = None
        self.isLeaf = False
        self.leafPatternNumbers = []

def addString(root, s, patternNumber, startPos):
    cur = root
    for c in s:
        if c not in cur.sons:
            cur.sons[c] = Node()
            cur.sons[c].parent = cur
            cur.sons[c].charToParent = c
        cur = cur.sons[c]
    cur.isLeaf = True
    cur.leafPatternNumbers.append((patternNumber, startPos))

def getSuffLink(v, root):
    if v.suffLink is None:
        if v == root or v.parent == root:
            v.suffLink = root
        else:
            v.suffLink = getLink(getSuffLink(v.parent, root), v.charToParent, root)
    return v.suffLink

def getLink(v, c, root):
    if c not in v.go:
        if c in v.sons:
            v.go[c] = v.sons[c]
        elif v == root:
            v.go[c] = root
        else:
            v.go[c] = getLink(getSuffLink(v, root), c, root)
    return v.go[c]

def getUp(v, root):
    if v.up is None:
        suffLink = getSuffLink(v, root)
        if suffLink.isLeaf:
            v.up = suffLink
        elif suffLink == root:
            v.up = root
        else:
            v.up = getUp(suffLink, root)
    return v.up

def countVertices(root):
    if not root:
        return 0
    
    visited = set()
    queue = [root]
    while queue:
        node = queue.pop(0)
        if node in visited:
            continue

        visited.add(node)
        for child in node.sons.values():
            if child not in visited:
                queue.append(child)
    return len(visited)

def findPatternWithJoker(text, pattern, joker):
    substrings = []
    currentSubstring = ""
    currentStart = 0
    for i, c in enumerate(pattern):
        if c == joker:
            if currentSubstring:
                substrings.append((currentSubstring, currentStart))
                currentSubstring = ""
            currentStart = i + 1
        else:
            if not currentSubstring:
                currentStart = i
            currentSubstring += c
    if currentSubstring:
        substrings.append((currentSubstring, currentStart))
    if not substrings:
        return [], 0, []
    root = Node()
    for i, (substring, pos) in enumerate(substrings):
        addString(root, substring, i, pos)
    verticesCount = countVertices(root)
    occurences = processText(root, text, substrings)
    result = []
    patternOccurences = {}
    for i in range(len(text) - len(pattern) + 1):
        if len(occurences[i]) == len(substrings):
            foundSubstrings = set(occurences[i])
            if len(foundSubstrings) == len(substrings):
                match = True
                for j in range(len(pattern)):
                    if i + j >= len(text):
                        match = False
                        break
                    if pattern[j] != joker and pattern[j] != text[i+j]:
                        match = False
                        break
                if match:
                    pos = i + 1
                    result.append(pos)
                    patternOccurences[1] = patternOccurences.get(1, []) + [pos]
    interspectingPatterns = findIntersectingPatterns(patternOccurences, [pattern])
    return result, verticesCount, interspectingPatterns

def processText(root, text, substrings):
    occurrences = [[] for _ in range(len(text) + 1)]
    cur = root
    for i, c in enumerate(text):
        cur = getLink(cur, c, root)
        
        if cur.isLeaf:
            for substringIdx, startInPattern in cur.leafPatternNumbers:
                substring, _ = substrings[substringIdx]
                substringStart = i - len(substring) + 1
                patternStart = substringStart - startInPattern
                if patternStart >= 0:
                    occurrences[patternStart].append(substringIdx)
        
        node = getUp(cur, root)
        while node != root:
            if node.isLeaf:
                for substringIdx, startInPattern in node.leafPatternNumbers:
                    substring, _ = substrings[substringIdx]
                    substringStart = i - len(substring) + 1
                    patternStart = substringStart - startInPattern
                    if patternStart >= 0:
                        occurrences[patternStart].append(substringIdx)
            node = getUp(node, root)
    return occurrences

def findIntersectingPatterns(patternOccurrences, patterns):
    intersectingPatterns = set()
    
    if len(patternOccurrences) == 1:
        patternNumber = list(patternOccurrences.keys())[0]
        positions = patternOccurrences[patternNumber]
        patternLength = len(patterns[patternNumber-1])
        
        intervals = [(pos, pos + patternLength - 1) for pos in positions]        
        intervals.sort()        
        for i in range(len(intervals) - 1):
            _, end1 = intervals[i]
            start2, _ = intervals[i+1]
            
            if start2 <= end1:
                intersectingPatterns.add(patternNumber)
                break   
    return sorted(list(intersectingPatterns))

text = input().strip()
pattern = input().strip()
joker = input().strip()
result, verticesCount, intersectingPatterns = findPatternWithJoker(text, pattern, joker)
for pos in result:
    print(pos)
