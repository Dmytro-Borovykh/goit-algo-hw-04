"""
Порівняння трьох алгоритмів сортування за часом виконання:
    - сортування вставками (insertion sort)   — O(n^2)
    - сортування злиттям (merge sort)         — O(n log n)
    - Timsort (вбудований sorted())           — O(n log n), O(n) на впорядкованих даних

Заміри виконуються модулем timeit на чотирьох типах наборів даних.

Використання:
    python sorting_benchmark.py
"""

import random
import timeit
import sys
from typing import Callable, List

# Рекурсія merge_sort на великих масивах може впертись у ліміт стека
sys.setrecursionlimit(20000)


# ---------------------------------------------------------------- алгоритми

def insertion_sort(arr: List[int]) -> List[int]:
    """Сортування вставками. Складність: O(n^2) у середньому, O(n) на впорядкованих даних."""
    a = arr[:]                      # працюємо з копією, щоб не псувати вхідні дані
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        # Зсуваємо більші елементи праворуч, поки не знайдемо місце для key
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return a


def merge(left: List[int], right: List[int]) -> List[int]:
    """Зливає два впорядковані списки в один впорядкований."""
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def merge_sort(arr: List[int]) -> List[int]:
    """Сортування злиттям. Складність: O(n log n) у всіх випадках."""
    if len(arr) <= 1:
        return arr[:]
    mid = len(arr) // 2
    return merge(merge_sort(arr[:mid]), merge_sort(arr[mid:]))


def timsort(arr: List[int]) -> List[int]:
    """Вбудований Timsort — гібрид сортування злиттям та вставками (реалізація на C)."""
    return sorted(arr)


# ------------------------------------------------------------ набори даних

def make_random(n: int) -> List[int]:
    """Випадковий масив."""
    return [random.randint(0, n * 10) for _ in range(n)]


def make_sorted(n: int) -> List[int]:
    """Вже впорядкований масив — найкращий випадок."""
    return list(range(n))


def make_reversed(n: int) -> List[int]:
    """Масив у зворотному порядку — найгірший випадок для вставок."""
    return list(range(n, 0, -1))


def make_nearly_sorted(n: int) -> List[int]:
    """Майже впорядкований масив: ~5% елементів переставлено місцями."""
    a = list(range(n))
    for _ in range(max(1, n // 20)):
        i, j = random.randrange(n), random.randrange(n)
        a[i], a[j] = a[j], a[i]
    return a


DATASETS = {
    "випадковий": make_random,
    "впорядкований": make_sorted,
    "зворотний": make_reversed,
    "майже впорядкований": make_nearly_sorted,
}

ALGORITHMS: dict[str, Callable[[List[int]], List[int]]] = {
    "Insertion": insertion_sort,
    "Merge": merge_sort,
    "Timsort": timsort,
}


# --------------------------------------------------------------- вимірювання

def measure(func: Callable, data: List[int], repeats: int = 3) -> float:
    """Повертає найкращий час виконання (у секундах) з кількох запусків."""
    timer = timeit.Timer(lambda: func(data))
    return min(timer.repeat(repeat=repeats, number=1))


def run_benchmark(sizes: List[int], insertion_limit: int = 10_000) -> dict:
    """Проганяє всі алгоритми на всіх наборах даних і повертає результати."""
    results: dict = {}

    for ds_name, generator in DATASETS.items():
        print(f"\n{'=' * 72}")
        print(f"Набір даних: {ds_name}")
        print(f"{'=' * 72}")
        print(f"{'n':>8} | {'Insertion, с':>14} | {'Merge, с':>12} | {'Timsort, с':>12} | {'Merge/Tim':>10}")
        print("-" * 72)

        results[ds_name] = {name: [] for name in ALGORITHMS}

        for n in sizes:
            data = generator(n)
            row = {}
            for name, func in ALGORITHMS.items():
                # Сортування вставками на великих масивах займає надто багато часу
                if name == "Insertion" and n > insertion_limit:
                    row[name] = None
                    results[ds_name][name].append(None)
                    continue
                t = measure(func, data)
                row[name] = t
                results[ds_name][name].append(t)

            fmt = lambda v: f"{v:.6f}" if v is not None else "пропущено"
            ratio = (f"{row['Merge'] / row['Timsort']:.1f}x"
                     if row["Timsort"] and row["Merge"] else "-")
            print(f"{n:>8} | {fmt(row['Insertion']):>14} | {fmt(row['Merge']):>12} | "
                  f"{fmt(row['Timsort']):>12} | {ratio:>10}")

    return results


def verify_correctness() -> None:
    """Перевіряє, що всі реалізації дають однаковий результат."""
    sample = make_random(500)
    reference = sorted(sample)
    for name, func in ALGORITHMS.items():
        assert func(sample) == reference, f"{name} працює некоректно!"
    print("Коректність усіх реалізацій підтверджено.\n")


if __name__ == "__main__":
    random.seed(42)                 # відтворюваність результатів
    verify_correctness()
    SIZES = [100, 500, 1_000, 5_000, 10_000, 50_000, 100_000]
    run_benchmark(SIZES)
