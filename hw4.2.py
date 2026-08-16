"""
Побудова фракталу «сніжинка Коха» з використанням рекурсії та модуля turtle.

Використання:
    python koch_snowflake.py            # рівень рекурсії запитається інтерактивно
    python koch_snowflake.py 4          # рівень рекурсії передано аргументом
"""

import sys
import turtle


def koch_curve(t: turtle.Turtle, order: int, size: float) -> None:
    """
    Рекурсивно малює криву Коха.

    Базовий випадок (order == 0) — просто відрізок прямої.
    Крок рекурсії: відрізок ділиться на 3 частини, середня замінюється
    двома сторонами рівностороннього трикутника (повороти -60° та +120°).
    """
    if order == 0:
        t.forward(size)
        return

    for angle in (60, -120, 60, 0):
        koch_curve(t, order - 1, size / 3)
        t.left(angle)


def draw_snowflake(order: int, size: float = 300) -> None:
    """Малює сніжинку Коха — три криві Коха, з'єднані в рівносторонній трикутник."""
    screen = turtle.Screen()
    screen.title(f"Сніжинка Коха — рівень рекурсії {order}")
    screen.bgcolor("white")

    t = turtle.Turtle()
    t.speed(0)              # максимальна швидкість малювання
    t.color("navy")
    t.hideturtle()

    # Центруємо фігуру на екрані
    t.penup()
    t.goto(-size / 2, size / 3)
    t.pendown()

    # Три сторони трикутника, кожна — крива Коха
    for _ in range(3):
        koch_curve(t, order, size)
        t.right(120)

    screen.exitonclick()    # вікно закривається кліком миші


def get_order() -> int:
    """Отримує рівень рекурсії з аргументів командного рядка або від користувача."""
    if len(sys.argv) > 1:
        raw = sys.argv[1]
    else:
        raw = input("Введіть рівень рекурсії (0-6): ")

    try:
        order = int(raw)
    except ValueError:
        print("Помилка: рівень рекурсії має бути цілим числом.", file=sys.stderr)
        sys.exit(1)

    if order < 0:
        print("Помилка: рівень рекурсії не може бути від'ємним.", file=sys.stderr)
        sys.exit(1)
    if order > 6:
        print("Попередження: рівень > 6 малюється дуже довго. Обмежено до 6.")
        order = 6

    return order


if __name__ == "__main__":
    draw_snowflake(get_order())
