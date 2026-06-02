import math
import random
import os
from collections import Counter

def guide():
    print("\n" + "=" * 50)
    print("1 - Посчитать частоты и энтропию для любого файла")
    print("2 - Создать тестовые файлы")
    print("3 - Проанализировать все тестовые файлы")
    print("0 - Выйти")

def calculate_entropy(counter, total):
    entropy = 0.0
    for count in counter.values():
        p = count / total
        entropy -= p * math.log2(p)
    return entropy

def analyze_file(filename):
    try:
        with open(filename, 'rb') as f:
            data = f.read()
    except FileNotFoundError:
        print(f"Файл {filename} не найден, проверь имя")
        return
    except Exception as e:
        print(f"Ошибка при чтении: {e}")
        return

    total = len(data)
    if total == 0:
        print("Файл пустой")
        return

    counter = Counter(data)
    ent = calculate_entropy(counter, total)

    print(f"\nАнализируем {filename}")
    print(f"Размер файла: {total} байт")
    print(f"Энтропия: {ent:.6f} бит")
    print("\nЧастоты байтов (байт -> сколько раз):")
    for byte_val in sorted(counter.keys()):
        print(f"  {byte_val:3d} (0x{byte_val:02X}) : {counter[byte_val]:6d}  ({counter[byte_val]/total:.2%})")
    print("-" * 50)

def generate_test_files():
    print("\nГенерирую тестовые файлы...")

    with open("test_same.bin", "wb") as f:
        f.write(b'A' * 1000)
    print("Создал test_same.bin (1000 букв A)")

    data_01 = bytes(random.choice([0, 1]) for _ in range(1000))
    with open("test_01.bin", "wb") as f:
        f.write(data_01)
    print("Создал test_01.bin (1000 случайных 0 и 1)")

    data_random = bytes(random.randint(0, 255) for _ in range(10000))
    with open("test_random.bin", "wb") as f:
        f.write(data_random)
    print("Создал test_random.bin (10000 случайных байт)")

    data_balanced = bytes([b for b in range(256) for _ in range(100)])
    with open("test_balanced.bin", "wb") as f:
        f.write(data_balanced)
    print("Создал test_balanced.bin (каждый байт от 0 до 255 по 100 раз)")

    print("Готово\n")

def analyze_all_tests():
    test_files = ["test_same.bin", "test_01.bin", "test_random.bin", "test_balanced.bin"]
    print("\n--- Смотрю тестовые файлы ---")
    for fname in test_files:
        if os.path.exists(fname):
            analyze_file(fname)
        else:
            print(f"Файл {fname} нет. Сначала сгенерируй (пункт 2)")
    print("--- Закончил ---\n")

def main():
    while True:
        guide()
        choice = input("Твой выбор: ").strip()

        if choice == '1':
            fname = input("Введи имя файла: ").strip()
            analyze_file(fname)
        elif choice == '2':
            generate_test_files()
        elif choice == '3':
            analyze_all_tests()
        elif choice == '0':
            print("Пока")
            break
        else:
            print("Не понял, введи 1, 2, 3 или 0")

if __name__ == "__main__":
    main()