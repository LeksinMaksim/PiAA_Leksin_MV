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

def addString(root, s, patternNumber):
    cur = root
    for c in s:
        if c not in cur.sons:
            cur.sons[c] = Node()
            cur.sons[c].parent = cur
            cur.sons[c].charToParent = c
        cur = cur.sons[c]
    cur.isLeaf = True
    cur.leafPatternNumbers.append(patternNumber)


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

def processText(root, text, patterns):
    result = []
    patternOccurrences = {}  
    cur = root
    for i, c in enumerate(text):
        cur = getLink(cur, c, root)
        
        if cur.isLeaf:
            for patternNumber in cur.leafPatternNumbers:
                pattern = patterns[patternNumber-1]
                pos = i - len(pattern) + 2  
                result.append((pos, patternNumber))
                
                if patternNumber not in patternOccurrences:
                    patternOccurrences[patternNumber] = []
                patternOccurrences[patternNumber].append(pos)
        
        node = getUp(cur, root)
        while node != root:
            if node.isLeaf:
                for patternNumber in node.leafPatternNumbers:
                    pattern = patterns[patternNumber-1]
                    pos = i - len(pattern) + 2
                    result.append((pos, patternNumber))
                    
                    if patternNumber not in patternOccurrences:
                        patternOccurrences[patternNumber] = []
                    patternOccurrences[patternNumber].append(pos)
            node = getUp(node, root)
    
    intersectingPatterns = findIntersectingPatterns(patternOccurrences, patterns)
    return result, intersectingPatterns

def findIntersectingPatterns(patternOccurences, patterns):
    intersectingPatterns = set()
    intervals = []
    for patternNumber, positions in patternOccurences.items():
        patternLength = len(patterns[patternNumber-1])
        for pos in positions:
            intervals.append((pos, pos + patternLength - 1, patternNumber))
    intervals.sort()
    for i in range(len(intervals)):
        start1, end1, pattern1 = intervals[i]
        for j in range(i+1, len(intervals)):
            start2, end2, pattern2 = intervals[j]
            if start2 > end1:
                break
            if pattern1 != pattern2:
                intersectingPatterns.add(pattern1)
                intersectingPatterns.add(pattern2)
    return sorted(list(intersectingPatterns))

def ahoCorasick(text, patterns):
    root = Node()
    for i, pattern in enumerate(patterns):
        addString(root, pattern, i+1)
    verticesCount = countVertices(root)
    result, intersectingPatterns = processText(root, text, patterns)
    result.sort()
    return result, verticesCount, intersectingPatterns

text = input().strip()
n = int(input().strip())
patterns = []
for _ in range(n):
    patterns.append(input().strip())
result, verticesCount, intersectingPatterns = ahoCorasick(text, patterns)
for pos, patternNumber in result:
    print(pos, patternNumber)
