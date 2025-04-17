import Foundation

private func charFromByte(_ byte: UInt8?) -> String {
    guard let byte = byte else { return "nil" }
    return String(bytes: [byte], encoding: .utf8) ?? "\(byte)"
}

private func computePi(patternBytes: [UInt8], verbose: Bool = false) -> [Int] {
    let m = patternBytes.count
    guard m > 0 else { return [] }

    var pi = [Int](repeating: 0, count: m)
    var k = 0

    if verbose {
        let patternStr = String(decoding: patternBytes, as: UTF8.self)
        print("\n--- Вычисление префикс-функции для шаблона: \"\(patternStr)\" ---")
        print("Инициализация: pi = \(pi), k = \(k)")
    }

    for i in 1..<m {
        let charPi = charFromByte(patternBytes[i])
        if verbose {
            print("\n[i=\(i), P[\(i)] = '\(charPi)']")
            print("   Текущее k (длина префикса для P[0...\(i-1)]): \(k)")
        }

        while k > 0 && patternBytes[i] != patternBytes[k] {
            let charPk = charFromByte(patternBytes[k])
            if verbose {
                print("   Несовпадение: P[\(i)]='\(charPi)' != P[\(k)]='\(charPk)'.")
                print("   Отступаем: k = pi[k-1] = pi[\(k-1)] = \(pi[k-1])")
            }
            k = pi[k - 1]
        }

        let charPk_after_while = charFromByte(patternBytes[k])
        if patternBytes[i] == patternBytes[k] {
            if verbose {
                print("   Совпадение: P[\(i)]='\(charPi)' == P[\(k)]='\(charPk_after_while)'.")
                print("   Увеличиваем k: \(k) -> \(k + 1)")
            }
            k += 1
        } else {
            if verbose && k == 0 {
                print(
                    "   Несовпадение: P[\(i)]='\(charPi)' != P[\(k)]='\(charPk_after_while)'. k остается \(k)."
                )
            }
        }

        pi[i] = k
        if verbose {
            print("   Устанавливаем pi[\(i)] = \(k). Массив pi: \(pi)")
        }
    }
    if verbose {
        print("--- Вычисление префикс-функции завершено ---")
    }
    return pi
}

func findAllOccurencesKMP(pattern: String, text: String, verbose: Bool = false) -> [Int] {
    let n_bytes_text = text.utf8.count
    let m_bytes_pattern = pattern.utf8.count

    if verbose {
        print("\n--- Поиск КМП ---")
        print("Текст T: \"\(text)\" (длина \(n_bytes_text) байт)")
        print("Шаблон P: \"\(pattern)\" (длина \(m_bytes_pattern) байт)")
    }
    guard m_bytes_pattern > 0 else {
        print("Шаблон пуст, поиск невозможен.")
        return []
    }
    guard n_bytes_text >= m_bytes_pattern else {
        print("Текст короче шаблона, вхождений нет.")
        return []
    }

    let textBytes = Array(text.utf8)
    let patternBytes = Array(pattern.utf8)

    let pi = computePi(patternBytes: patternBytes, verbose: verbose)

    if verbose {
        print("\n--- Начало основного цикла поиска ---")
        print("Префикс-функция pi: \(pi)")
    }

    var occurences: [Int] = []
    var j = 0

    for i in 0..<textBytes.count {
        let charTi = charFromByte(textBytes[i])
        if verbose {
            print("\n[i=\(i), T[\(i)]='\(charTi)']")
            print("   Текущий j (индекс в P / длина совпадения): \(j)")
        }

        while j > 0 && textBytes[i] != patternBytes[j] {
            let charPj = charFromByte(patternBytes[j])
            if verbose {
                print("   Несовпадение: T[\(i)]='\(charTi)' != P[\(j)]='\(charPj)'.")
                print("   Используем префикс-функцию: j = pi[j-1] = \(pi[j-1])")
            }
            j = pi[j - 1]
        }
        let charPj_after_while = charFromByte(patternBytes[j])
        if textBytes[i] == patternBytes[j] {
            if verbose {
                print("   Совпадение: T[\(i)]='\(charTi)' == P[\(j)]='\(charPj_after_while)'.")
                print("   Увеличиваем j: \(j) -> \(j + 1)")
            }
            j += 1
        } else {
            if verbose && j == 0 {
                print(
                    "   Несовпадение: T[\(i)]='\(charTi)' != P[\(j)]='\(charPj_after_while)'. j остается \(j)."
                )
            }
        }

        if j == m_bytes_pattern {
            let startIndex = i - m_bytes_pattern + 1
            if verbose {
                print(
                    "   >>> НАЙДЕНО ВХОЖДЕНИЕ! j == m (\(j) == \(m_bytes_pattern)). Индекс начала: \(startIndex) (i - m + 1 = \(i) - \(m_bytes_pattern) + 1)."
                )
            }
            occurences.append(startIndex)
            if verbose {
                print(
                    "   Используем префикс-функцию для сдвига после находки: j = pi[j-1] = [pi[\(j-1)] = \(pi[j-1])"
                )
            }
            j = pi[j - 1]
        }
    }
    if verbose {
        print("\n--- Поиск КМП завершен ---")
    }
    return occurences
}

print("Введите шаблон P:")
guard let pattern = readLine() else {
    fatalError("Не удалось прочитать строку шаблона P")
}

print("Введите текст T:")
guard let text = readLine() else {
    fatalError("Не удалось прочитать строку текста T")
}

guard pattern.count <= 25000 else {
    fatalError("Длинна шаблона P превышает ограничение в 25000 символов")
}

print("Включить подробный вывод? (yes/no):")
let verboseInput = readLine()?.lowercased()
let verboseMode = (verboseInput == "yes" || verboseInput == "y")

let resultIndices = findAllOccurencesKMP(pattern: pattern, text: text, verbose: verboseMode)

print("\n--- Результат ---")
if resultIndices.isEmpty {
    print("Индекс(ы) вхождения: -1")
} else {
    let resultString = resultIndices.map { String($0) }.joined(separator: ",")
    print("Индекс(ы) вхождения: \(resultString)")
}
