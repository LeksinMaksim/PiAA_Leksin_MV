import Foundation

private func computePi(patternBytes: [UInt8]) -> [Int] {
    let m = patternBytes.count
    guard m > 0 else { return [] }

    var pi = [Int](repeating: 0, count: m)
    var k = 0

    for i in 1..<m {
        while k > 0 && patternBytes[i] != patternBytes[k] {
            k = pi[k-1]
        }

        if patternBytes[i] == patternBytes[k] {
            k += 1
        }

        pi[i] = k
    }
    return pi
}

func findAllOccurencesKMP(pattern: String, text: String) -> [Int] {
    let n = text.count
    let m = pattern.count
    guard m > 0 else {
        print("Warning: Pattern is empty.")
        return []
    }
    guard n >= m else { return [] }

    let textBytes = Array(text.utf8)
    let patternBytes = Array(pattern.utf8)

    let pi = computePi(patternBytes: patternBytes)

    var occurences: [Int] = []
    var j = 0

    for i in 0..<textBytes.count {
        while j > 0 && textBytes[i] != patternBytes[j] {
            j = pi[j-1]
        }
        if textBytes[i] == patternBytes[j] {
            j += 1
        }

        if j == m {
            let startIndex = i - m + 1
            occurences.append(startIndex)
            j = pi[j-1]
        }
    }
    return occurences
}

guard let pattern = readLine() else {
    fatalError("Не удалось прочитать строку шаблона P")
}

guard let text = readLine() else {
    fatalError("Не удалось прочитать строку текста T")
}

guard pattern.count <= 25000 else {
    fatalError("Длинна шаблона P превышает ограничение в 25000 символов")
}

let resultIndices = findAllOccurencesKMP(pattern: pattern, text: text)

if resultIndices.isEmpty {
    print("-1")
} else {
    let resultString = resultIndices.map { String($0) }.joined(separator: ",")
    print(resultString)
}
