def kmp_matcher(text: str, pattern: str) -> int:
    text_length = len(text)
    pattern_length = len(pattern)
    pi = compute_prefix_function(pattern)
    match_len = 0
    
    for i in range(text_length):
        while match_len > 0 and pattern[match_len] != text[i]:
            match_len = pi[match_len - 1]
        if pattern[match_len] == text[i]:
            match_len += 1
        if match_len == pattern_length:
            return i - pattern_length + 1
    return -1


def compute_prefix_function(pattern: str) -> list[int]:
    pattern_length = len(pattern)
    pi = [0 for _ in range(pattern_length)]
    border_len = 0
    for i in range(1, pattern_length):
        while border_len > 0 and pattern[border_len] != pattern[i]:
            border_len = pi[border_len - 1]
        if pattern[border_len] == pattern[i]:
            border_len += 1
        pi[i] = border_len
    return pi


def check_cyclic_shift(str1: str, str2: str) -> int:
    if len(str1) != len(str2):
        return -1
    if str1 == str2:
        return 0

    doubled_str1 = str1 + str1
    
    return kmp_matcher(doubled_str1, str2)


if __name__ == "__main__":
    str2 = input()
    str1 = input()
    
    print(check_cyclic_shift(str2, str1))
