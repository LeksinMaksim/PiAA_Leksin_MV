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
            print("\n[i=\(i), P[\(i)]='\(charPi)']")
            print("  Текущее k (длина префикса для P[0...\(i-1)]): \(k)")
        }
        while k > 0 && patternBytes[i] != patternBytes[k] {
            let charPk = charFromByte(patternBytes[k])
            if verbose {
                print("  Несовпадение: P[\(i)]='\(charPi)' != P[\(k)]='\(charPk)'.")
                print("  Отступаем: k = pi[k-1] = pi[\(k-1)] = \(pi[k - 1])")
            }
            k = pi[k - 1]
        }
        let charPk_after_while = charFromByte(patternBytes[k])
        if patternBytes[i] == patternBytes[k] {
            if verbose {
                print("  Совпадение: P[\(i)]='\(charPi)' == P[\(k)]='\(charPk_after_while)'.")
                print("  Увеличиваем k: \(k) -> \(k + 1)")
            }
            k += 1
        } else {
            if verbose && k == 0 {
                print(
                    "  Несовпадение: P[\(i)]='\(charPi)' != P[\(k)]='\(charPk_after_while)'. k остается \(k)."
                )
            }
        }
        pi[i] = k
        if verbose {
            print("  Устанавливаем pi[\(i)] = \(k). Массив pi: \(pi)")
        }
    }
    if verbose {
        print("--- Вычисление префикс-функции завершено ---")
    }
    return pi
}

private func findAllOccurrencesKMP(pattern: String, text: String, verbose: Bool = false) -> [Int] {
    let n_bytes_text = text.utf8.count
    let m_bytes_pattern = pattern.utf8.count

    if verbose {
        print("\n--- Поиск КМП ---")
        print("Текст T: \"\(text)\" (длина \(n_bytes_text) байт)")
        print("Шаблон P: \"\(pattern)\" (длина \(m_bytes_pattern) байт)")
    }
    guard m_bytes_pattern > 0 else {
        if verbose { print("Шаблон пуст, поиск невозможен.") }
        return []
    }
    guard n_bytes_text >= m_bytes_pattern else {
        if verbose { print("Текст короче шаблона, вхождений нет.") }
        return []
    }

    let textBytes = Array(text.utf8)
    let patternBytes = Array(pattern.utf8)
    let pi = computePi(patternBytes: patternBytes, verbose: verbose)

    if verbose {
        print("\n--- Начало основного цикла поиска ---")
        print("Префикс-функция pi: \(pi)")
    }

    var occurrences: [Int] = []
    var j = 0
    for i in 0..<textBytes.count {
        let charTi = charFromByte(textBytes[i])
        if verbose {
            print("\n[i=\(i), T[\(i)]='\(charTi)']")
            print("  Текущий j (индекс в P / длина совпадения): \(j)")
        }
        while j > 0 && textBytes[i] != patternBytes[j] {
            let charPj = charFromByte(patternBytes[j])
            if verbose {
                print("  Несовпадение: T[\(i)]='\(charTi)' != P[\(j)]='\(charPj)'.")
                print("  Используем префикс-функцию: j = pi[j-1] = pi[\(j-1)] = \(pi[j - 1])")
            }
            j = pi[j - 1]
        }
        let charPj_after_while = charFromByte(patternBytes[j])
        if textBytes[i] == patternBytes[j] {
            if verbose {
                print("  Совпадение: T[\(i)]='\(charTi)' == P[\(j)]='\(charPj_after_while)'.")
                print("  Увеличиваем j: \(j) -> \(j + 1)")
            }
            j += 1
        } else {
            if verbose && j == 0 {
                print(
                    "  Несовпадение: T[\(i)]='\(charTi)' != P[\(j)]='\(charPj_after_while)'. j остается \(j)."
                )
            }
        }
        if j == m_bytes_pattern {
            let startIndex = i - m_bytes_pattern + 1
            if verbose {
                print(
                    "  >>> НАЙДЕНО ВХОЖДЕНИЕ (в конкатенированном тексте)! j == m (\(j) == \(m_bytes_pattern)). Индекс начала: \(startIndex) (i - m + 1 = \(i) - \(m_bytes_pattern) + 1)."
                )
            }
            occurrences.append(startIndex)
            if verbose {
                print(
                    "  (КМП) Используем префикс-функцию для сдвига после находки: j = pi[j-1] = pi[\(j-1)] = \(pi[j - 1])"
                )
            }
            j = pi[j - 1]
        }
    }
    if verbose {
        print("\n--- Поиск КМП завершен ---")
    }
    return occurrences
}

func checkCyclicShift(a: String, b: String, verbose: Bool = false) -> Int {
    if verbose {
        print("\n--- Проверка циклического сдвига ---")
        print("Строка A: \"\(a)\"")
        print("Строка B: \"\(b)\"")
    }

    let countA = a.count
    let countB = b.count
    if verbose {
        print("Проверка длин: |A|=\(countA), |B|=\(countB)")
    }
    guard countA == countB else {
        if verbose { print("Длины не равны. Результат: -1") }
        return -1
    }

    let n_bytes = a.utf8.count
    if verbose {
        print("Байтовая длина n = \(n_bytes)")
    }

    guard n_bytes > 0 else {
        if verbose { print("Строки пустые. Результат: 0") }
        return 0
    }

    if verbose {
        print("Проверка на равенство A == B")
    }
    if a == b {
        if verbose { print("Строки равны. Результат: 0") }
        return 0
    }
    if verbose {
        print("Строки не равны.")
    }

    if verbose {
        print("Создание строки T = B + B")
    }
    let concatenatedB = b + b
    if verbose {
        print("T = \"\(concatenatedB)\"")
        print("Запуск поиска КМП: ищем A в T...")
    }

    let occurrences = findAllOccurrencesKMP(pattern: a, text: concatenatedB, verbose: verbose)

    if verbose {
        print("\n--- Обработка результата КМП ---")
        print("Найденные КМП индексы (k) в T: \(occurrences)")
    }

    if let k = occurrences.first {
        if verbose {
            print("Найдено первое вхождение A в T с индексом k = \(k)")
            print("Вычисление результата по формуле: n_bytes - k (где n_bytes=\(n_bytes))")
            print("Результат: \(n_bytes) - \(k) = \(n_bytes - k)")
        }
        return n_bytes - k
    } else {
        if verbose {
            print("Вхождения A в T не найдены.")
            print("Результат: -1")
        }
        return -1
    }
}

print("Введите строку A:")
guard let stringA = readLine() else {
    fatalError("Не удалось прочитать строку A")
}

print("Введите строку B:")
guard let stringB = readLine() else {
    fatalError("Не удалось прочитать строку B")
}

print("Включить подробный вывод? (yes/no):")
let verboseInput = readLine()?.lowercased()
let verboseMode = (verboseInput == "yes" || verboseInput == "y")

let resultIndex = checkCyclicShift(a: stringA, b: stringB, verbose: verboseMode)

print("\n--- Итоговый результат ---")
print("Индекс циклического сдвига: \(resultIndex)")
