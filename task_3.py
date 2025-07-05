import requests
import timeit
import chardet

# Завантаження файлів з Google Drive
# Функція `download_from_google_drive()` завантажує файл за цим ID та зберігає його локально

def download_from_google_drive(file_id, destination):
    URL = "https://drive.google.com/uc?export=download"
    with requests.Session() as session:
        response = session.get(URL, params={'id': file_id}, stream=True)
        token = get_confirm_token(response)
        if token:
            params = {'id': file_id, 'confirm': token}
            response = session.get(URL, params=params, stream=True)
        save_response_content(response, destination)


def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value
    return None


def save_response_content(response, destination):
    CHUNK_SIZE = 32768
    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk:
                f.write(chunk)


# Автовизначення кодування 
# Функція `detect_encoding()` аналізує байти файлу та повертає кодування
def detect_encoding(filepath):
    with open(filepath, "rb") as f:
        result = chardet.detect(f.read())
        print(f"Виявлено кодування для '{filepath}': {result['encoding']}")
        return result['encoding']


# Реалізація алгоритмів пошуку 

def boyer_moore_search(text, pattern):
    def build_shift_table(pattern):
        table = {}
        plen = len(pattern)
        for i in range(plen - 1):
            table[pattern[i]] = plen - i - 1
        return table

    shift_table = build_shift_table(pattern)
    i = 0
    while i <= len(text) - len(pattern):
        j = len(pattern) - 1
        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1
        if j < 0:
            return i
        i += shift_table.get(text[i + len(pattern) - 1], len(pattern))
    return -1


def kmp_search(text, pattern):
    def compute_lps(pattern):
        lps = [0] * len(pattern)
        length = 0
        i = 1
        while i < len(pattern):
            if pattern[i] == pattern[length]:
                length += 1
                lps[i] = length
                i += 1
            elif length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
        return lps

    lps = compute_lps(pattern)
    i = j = 0
    while i < len(text):
        if pattern[j] == text[i]:
            i += 1
            j += 1
        if j == len(pattern):
            return i - j
        elif i < len(text) and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return -1


def rabin_karp_search(text, pattern, prime=101):
    m, n = len(pattern), len(text)
    hpattern = 0
    htext = 0
    h = 1
    d = 256

    for i in range(m - 1):
        h = (h * d) % prime
    for i in range(m):
        hpattern = (d * hpattern + ord(pattern[i])) % prime
        htext = (d * htext + ord(text[i])) % prime

    for i in range(n - m + 1):
        if hpattern == htext:
            if text[i:i + m] == pattern:
                return i
        if i < n - m:
            htext = (d * (htext - ord(text[i]) * h) + ord(text[i + m])) % prime
            if htext < 0:
                htext += prime
    return -1


# Вимірювання часу

def measure(func, text, pattern):
    timer = timeit.Timer(lambda: func(text, pattern))
    return min(timer.repeat(repeat=3, number=1))  # найшвидший запуск


# Основна логіка

# IDs файлів із Google Drive
file_id1 = "18_R5vEQ3eDuy2VdV3K5Lu-R-B-adxXZh"
file_id2 = "18BfXyQcmuinEI_8KDSnQm4bLx6yIFS_w"

# Завантажуємо файли
download_from_google_drive(file_id1, "article1.txt")
download_from_google_drive(file_id2, "article2.txt")

# Автовизначаємо кодування
encoding1 = detect_encoding("article1.txt")
encoding2 = detect_encoding("article2.txt")

# Читаємо тексти з правильним кодуванням
with open("article1.txt", "r", encoding=encoding1) as f:
    text1 = f.read()

with open("article2.txt", "r", encoding=encoding2) as f:
    text2 = f.read()

# Обираємо підрядки
existing_substring = "algorithm"         # існуючий
fake_substring = "nonexistentpattern"    # вигаданий

# Алгоритми
algorithms = [
    ("Boyer–Moore", boyer_moore_search),
    ("KMP", kmp_search),
    ("Rabin–Karp", rabin_karp_search),
]

# Порівняння
for idx, text in enumerate([text1, text2], start=1):
    print(f"\n === Текст {idx} ===")
    for pattern, desc in [(existing_substring, "існуючий"), (fake_substring, "вигаданий")]:
        print(f"\n Підрядок ({desc}): '{pattern}'")
        for name, func in algorithms:
            t = measure(func, text, pattern)
            print(f"  {name:<15}: {t:.6f} сек")

