"""
Мини-проект: скрипт-обработчик логов.

Формат строки лога:
2026-09-20 10:01:15 INFO 192.168.1.10 GET /api/users 200

Задача: для каждого IP-адреса посчитать, сколько раз он встречается
в логе с уровнем ERROR.

Ниже — две версии решения одной и той же задачи:
  1. naive_version()      -- вложенные циклы, O(n * m)
  2. optimized_version()  -- один проход, O(n)

Это сделано специально, чтобы наглядно увидеть разницу в подходе
и в производительности на больших файлах.
"""

import time
from collections import defaultdict


def read_log_lines(path: str) -> list[str]:
    """Читает файл и возвращает список строк без пустых и лишних пробелов."""
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def naive_version(lines: list[str]) -> dict[str, int]:
    """
    ПЛОХОЙ (но частый у новичков) способ.

    Идея: сначала собрать список всех IP из ERROR-строк,
    а потом для каждого уникального IP заново пробежаться по всему
    списку и посчитать вхождения через .count().

    Проблема: list.count() сам по себе проходит по всему списку.
    Если снаружи ещё один цикл по уникальным IP -- получаем
    вложенные циклы -> O(n * m), где n -- строки, m -- уникальные IP.
    На большом логе (миллионы строк) это будет ОЧЕНЬ медленно.
    """
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


def optimized_version(lines: list[str]) -> dict[str, int]:
    """
    Оптимизированная версия. Один проход по строкам, O(n).

    Ключевая идея: используем defaultdict(int) -- словарь,
    который сам создаёт значение 0 при первом обращении к новому ключу.
    Это убирает необходимость отдельно искать "уникальные" элементы
    и отдельно их считать -- всё происходит за один проход.
    """
    counts: dict[str, int] = defaultdict(int)
    for line in lines:
        parts = line.split()
        level, ip = parts[2], parts[3]
        if level == "ERROR":
            counts[ip] += 1
    return dict(counts)


def benchmark(lines: list[str]) -> None:
    """Сравнивает время работы обеих версий на одинаковых данных."""
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


def generate_big_log(base_lines: list[str], repeats: int) -> list[str]:
    """
    Генерирует большой лог с БОЛЬШИМ количеством уникальных IP.

    Это важно для демонстрации: если уникальных IP мало (как в
    sample.log -- их всего 4), разница между наивной и оптимизированной
    версией почти не видна, потому что внутренний цикл наивной версии
    короткий. Реальная разница проявляется, когда уникальных IP много
    -- именно так выглядят настоящие логи веб-сервера.
    """
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
    log_lines = read_log_lines("sample.log")

    # Имитация большого лога с большим числом уникальных IP-адресов
    big_log = generate_big_log(log_lines, repeats=300)
    print(f"Строк в логе: {len(big_log)}")

    benchmark(big_log)
