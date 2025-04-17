import Foundation

private func computePi(patternBytes: [UInt8]) -> [Int] {
    let m = patternBytes.count
    guard m > 0 else { return [] }
    var pi = [Int](repeating: 0, count: m)
    var k = 0
    for i in 1..<m {
        while k > 0 && patternBytes[i] != patternBytes[k] {
            k = pi[k - 1]
        }
        if patternBytes[i] == patternBytes[k] {
            k += 1
        }
        pi[i] = k
    }
    return pi
}

private func findAllOccurrencesKMP(pattern: String, text: String) -> [Int] {
    let n_bytes_text = text.utf8.count
    let m_bytes_pattern = pattern.utf8.count

    guard m_bytes_pattern > 0 else { return [] }
    guard n_bytes_text >= m_bytes_pattern else { return [] }

    let textBytes = Array(text.utf8)
    let patternBytes = Array(pattern.utf8)

    let pi = computePi(patternBytes: patternBytes)

    var occurrences: [Int] = []
    var j = 0

    for i in 0..<textBytes.count {
        while j > 0 && textBytes[i] != patternBytes[j] {
            j = pi[j - 1]
        }
        if textBytes[i] == patternBytes[j] {
            j += 1
        }
        if j == m_bytes_pattern {
            let startIndex = i - m_bytes_pattern + 1
            occurrences.append(startIndex)
            j = pi[j - 1]
        }
    }
    return occurrences
}

func checkCyclicShift(a: String, b: String) -> Int {
    guard a.count == b.count else {
        return -1
    }

    let n_bytes = a.utf8.count

    guard n_bytes > 0 else {
        return 0
    }

    if a == b {
        return 0
    }

    let concatenatedB = b + b
    let occurrences = findAllOccurrencesKMP(pattern: a, text: concatenatedB)

    if let k = occurrences.first {
        return n_bytes - k
    } else {
        return -1
    }
}

guard let stringA = readLine() else {
    fatalError("Не удалось прочитать строку A")
}

guard let stringB = readLine() else {
    fatalError("Не удалось прочитать строку B")
}

let resultIndex = checkCyclicShift(a: stringA, b: stringB)
print(resultIndex)
