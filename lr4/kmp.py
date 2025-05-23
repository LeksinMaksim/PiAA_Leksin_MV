def kmp_matcher(text: str, pattern: str) -> list[int]:
    text_length = len(text)
    pattern_length = len(pattern)
    occurrences = []
    pi = compute_prefix_function(pattern)
    match_len = 0

    for i in range(text_length):
        while match_len > 0 and pattern[match_len] != text[i]:
            match_len = pi[match_len - 1]
        if pattern[match_len] == text[i]:
            match_len += 1
        if match_len == pattern_length:
            occurrences.append(i - pattern_length + 1)
            match_len = pi[pattern_length - 1]
    if not occurrences:
        return [-1]
    return occurrences


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


if __name__ == "__main__":
    pattern = input()
    text = input()
    if len(text) < len(pattern):
        print(-1)
    else:
        print(*kmp_matcher(text, pattern), sep=',')
