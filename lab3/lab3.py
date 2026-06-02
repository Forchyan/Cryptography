import os
import numpy as np


def gen_key_file(fname, size):
    data = np.random.randint(0, 256, size, dtype=np.uint8)
    with open(fname, "wb") as f:
        f.write(data.tobytes())
    print(f"Создан ключевой файл {fname} ({size} байт)")

def vernam(in_fname, key_fname, out_fname):
    """XOR входного файла с ключевым файлом"""
    if not os.path.exists(in_fname):
        print(f"Файл {in_fname} не найден, сорян")
        return
    if not os.path.exists(key_fname):
        print(f"Ключевой файл {key_fname} не найден")
        return

    size_in = os.path.getsize(in_fname)
    size_key = os.path.getsize(key_fname)
    if size_key < size_in:
        print(f"Ключ ({size_key} байт) короче файла ({size_in} байт). Берём только первые {size_key} байт файла.")
        return

    with open(in_fname, "rb") as f_in, open(key_fname, "rb") as f_key, open(out_fname, "wb") as f_out:
        while True:
            block = f_in.read(4096)
            key_block = f_key.read(len(block))
            if not block:
                break
            xor_block = bytes(a ^ b for a, b in zip(block, key_block))
            f_out.write(xor_block)
    print(f"Обработано: {in_fname} -> {out_fname} (Вернам)")

class RC4:
    def __init__(self, key):
        self.S = list(range(256))
        j = 0
        for i in range(256):
            j = (j + self.S[i] + key[i % len(key)]) % 256
            self.S[i], self.S[j] = self.S[j], self.S[i]
        self.i = 0
        self.j = 0

    def keystream(self):
        while True:
            self.i = (self.i + 1) % 256
            self.j = (self.j + self.S[self.i]) % 256
            self.S[self.i], self.S[self.j] = self.S[self.j], self.S[self.i]
            yield self.S[(self.S[self.i] + self.S[self.j]) % 256]

def rc4_file(in_fname, out_fname, key_bytes):
    if not os.path.exists(in_fname):
        print(f"Файл {in_fname} не найден")
        return
    rc4 = RC4(key_bytes)
    with open(in_fname, "rb") as f_in, open(out_fname, "wb") as f_out:
        for byte in iter(lambda: f_in.read(1), b''):
            k = next(rc4.keystream())
            f_out.write(bytes([byte[0] ^ k]))
    print(f"Обработано: {in_fname} -> {out_fname} (RC4)")

def main():
    while True:
        print("\n" + "="*50)
        print("1 - Сгенерировать ключевой файл")
        print("2 - Шифр Вернама (XOR) - зашифровать/расшифровать")
        print("3 - Поточный шифр RC4 - зашифровать/расшифровать")
        print("0 - Выйти")
        choice = input("Твой выбор: ").strip()

        if choice == '1':
            name = input("Имя файла-ключа: ").strip()
            try:
                size = int(input("Размер в байтах: "))
            except:
                print("Надо число")
                continue
            if size > 0:
                gen_key_file(name, size)
            else:
                print("Размер должен быть положительным")

        elif choice == '2':
            inp = input("Входной файл: ").strip()
            key = input("Ключевой файл: ").strip()
            out = input("Выходной файл: ").strip()
            vernam(inp, key, out)

        elif choice == '3':
            inp = input("Входной файл: ").strip()
            out = input("Выходной файл: ").strip()
            key_str = input("Ключ (строка): ").strip().encode()
            if not key_str:
                print("Ключ не может быть пустым")
                continue
            rc4_file(inp, out, key_str)

        elif choice == '0':
            print("Пока")
            break
        else:
            print("Не понял, введи 1,2,3 или 0")

if __name__ == "__main__":
    main()