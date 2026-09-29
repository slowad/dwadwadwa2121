
import os
import time
from collections import defaultdict


def read_log_lines(path):
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def naive_version(lines):

    error_ips = []
    for line in lines:                  # цикл №1: n строк
        parts = line.split()
        level = parts[2]
        ip = parts[3]
        if level == "ERROR":
            error_ips.append(ip)

    unique_ips = []
    for ip in error_ips:                # цикл №2: n элементов
        if ip not in unique_ips:        # in по списку -- ещё один проход!
            unique_ips.append(ip)

    result = {}
    for ip in unique_ips:               # цикл №3: m уникальных IP
        result[ip] = error_ips.count(ip)  # .count() -- проход по всем n
    return result


def optimized_version(lines):
    counts: dict[str, int] = defaultdict(int)
    for line in lines:
        parts = line.split()
        level, ip = parts[2], parts[3]
        if level == "ERROR":
            counts[ip] += 1
    return dict(counts)


def benchmark(lines):
    start = time.perf_counter()
    naive_result = naive_version(lines)
    naive_time = time.perf_counter() - start

    start = time.perf_counter()
    fast_result = optimized_version(lines)
    fast_time = time.perf_counter() - start

    assert naive_result == fast_result, "Результаты должны совпадать!"

    print(f"Наивная версия:       {naive_time:.6f} сек")
    print(f"Оптимизированная:     {fast_time:.6f} сек")
    print(f"Результат (ERROR по IP): {fast_result}")


def generate_big_log(base_lines, repeats):

    big = []
    for i in range(repeats):
        for line in base_lines:
            parts = line.split()
            # подменяем последний октет IP, чтобы получить много уникальных адресов
            ip_parts = parts[3].split(".")
            ip_parts[-1] = str(i % 250)
            parts[3] = ".".join(ip_parts)
            big.append(" ".join(parts))
    return big


if __name__ == "__main__":
    # Автоматически определяем папку, в которой лежит сам скрипт log_analyzer.py
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Соединяем путь к папке и имя файла (у вас на скриншоте файл называется просто sample без .log)
    log_path = os.path.join(current_dir, "sample.log")

    log_lines = read_log_lines(log_path)

    # Имитация большого лога с большим числом уникальных IP-адресов
    big_log = generate_big_log(log_lines, repeats=300)
    print(f"Строк в логе: {len(big_log)}")

    benchmark(big_log)
