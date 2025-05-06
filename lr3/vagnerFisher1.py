def minCostTransform(stringA, stringB, replaceCost, insertCost, deleteCost):
    m, n = len(stringA), len(stringB)
    dpTable = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        dpTable[i][0] = dpTable[i-1][0] + deleteCost

    for j in range(1, n + 1):
        dpTable[0][j] = dpTable[0][j-1] + insertCost

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if stringA[i-1] == stringB[j-1]:
                dpTable[i][j] = dpTable[i-1][j-1]
            else:
                replaceOption = dpTable[i-1][j-1] + replaceCost
                deleteOption = dpTable[i-1][j] + deleteCost
                insertOption = dpTable[i][j-1] + insertCost

                dpTable[i][j] = min(replaceOption, deleteOption, insertOption)
    
    return dpTable[m][n]


def findLcsLength(stringA, stringB):
    m, n = len(stringA), len(stringB) 
    lcsTable = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if stringA[i-1] == stringB[j-1]:
                lcsTable[i][j] = lcsTable[i-1][j-1] + 1
            else:
                lcsTable[i][j] = max(lcsTable[i-1][j], lcsTable[i][j-1])
    
    return lcsTable[m][n]

def main():
    costs = list(map(int, input().split()))
    replaceCost, insertCost, deleteCost = costs

    stringA = input().strip()
    stringB = input().strip()

    result = minCostTransform(stringA, stringB, replaceCost, insertCost, deleteCost)

    lcsLength = findLcsLength(stringA, stringB)

    print(result)

    print(f"Длина наибольшей общей подпоследовательности: {lcsLength}")

if __name__ == "__main__":
    main()
