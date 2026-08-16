"""
Рекурсивне копіювання файлів із вихідної директорії до директорії призначення
з сортуванням у піддиректорії за розширенням файлів.

Використання:
    python sort_files.py <шлях_до_вихідної_директорії> [шлях_до_директорії_призначення]

Якщо другий аргумент не передано, використовується директорія 'dist'.
"""

import argparse
import shutil
import sys
from pathlib import Path


def parse_arguments() -> argparse.Namespace:
    """Парсинг аргументів командного рядка."""
    parser = argparse.ArgumentParser(
        description="Рекурсивно копіює файли та сортує їх у піддиректорії за розширенням."
    )
    parser.add_argument(
        "source",
        type=Path,
        help="Шлях до вихідної директорії",
    )
    parser.add_argument(
        "destination",
        type=Path,
        nargs="?",
        default=Path("dist"),
        help="Шлях до директорії призначення (за замовчуванням: dist)",
    )
    return parser.parse_args()


def copy_file(file_path: Path, destination: Path) -> None:
    """Копіює один файл у піддиректорію, назва якої відповідає його розширенню."""
    # Розширення без крапки та в нижньому регістрі; якщо його немає — тека 'no_extension'
    extension = file_path.suffix.lower().lstrip(".") or "no_extension"
    target_dir = destination / extension

    try:
        target_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(file_path, target_dir / file_path.name)
        print(f"[✓] {file_path} -> {target_dir / file_path.name}")
    except PermissionError:
        print(f"[!] Немає прав доступу до файлу: {file_path}", file=sys.stderr)
    except OSError as e:
        print(f"[!] Помилка копіювання {file_path}: {e}", file=sys.stderr)


def process_directory(source: Path, destination: Path) -> None:
    """Рекурсивно перебирає елементи директорії: теки обходить рекурсивно, файли копіює."""
    try:
        entries = list(source.iterdir())
    except PermissionError:
        print(f"[!] Немає прав доступу до директорії: {source}", file=sys.stderr)
        return
    except OSError as e:
        print(f"[!] Помилка читання директорії {source}: {e}", file=sys.stderr)
        return

    for entry in entries:
        try:
            if entry.is_dir():
                # Пропускаємо теку призначення, якщо вона всередині вихідної —
                # інакше отримаємо нескінченну рекурсію
                if entry.resolve() == destination.resolve():
                    continue
                process_directory(entry, destination)
            elif entry.is_file():
                copy_file(entry, destination)
        except OSError as e:
            print(f"[!] Помилка обробки {entry}: {e}", file=sys.stderr)


def main() -> int:
    args = parse_arguments()
    source: Path = args.source
    destination: Path = args.destination

    if not source.exists():
        print(f"[!] Вихідна директорія не існує: {source}", file=sys.stderr)
        return 1
    if not source.is_dir():
        print(f"[!] Вказаний шлях не є директорією: {source}", file=sys.stderr)
        return 1

    try:
        destination.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        print(f"[!] Не вдалося створити директорію призначення {destination}: {e}", file=sys.stderr)
        return 1

    print(f"Копіювання з '{source}' до '{destination}'...\n")
    process_directory(source, destination)
    print("\nГотово. Усі доступні файли скопійовано та розсортовано за розширенням.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
