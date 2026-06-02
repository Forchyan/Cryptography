import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes



def get_key(password: str, salt: bytes, length=32):
    """получаем ключ из пароля методом PBKDF2"""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=length,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

# Шифрование файла (AES-CBC)
def encrypt_file(in_file, out_file, password):
    if not os.path.exists(in_file):
        print(f"Файл {in_file} не найден")
        return

    # соль (8 байт) и вектор инициализации (16 байт) – случайные
    salt = os.urandom(8)
    iv = os.urandom(16)
    key = get_key(password, salt)

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    with open(in_file, "rb") as f_in, open(out_file, "wb") as f_out:
        # сначала пишем соль и iv
        f_out.write(salt)
        f_out.write(iv)

        # шифруем блоками по 16 байт (дополнение PKCS7)
        while True:
            data = f_in.read(16)
            if not data:
                break
            if len(data) < 16:
                # добавляем паддинг
                pad_len = 16 - len(data)
                data += bytes([pad_len] * pad_len)
            encrypted = encryptor.update(data)
            f_out.write(encrypted)
        # финализируем (в нашем случае пусто)
        f_out.write(encryptor.finalize())

    print(f"Зашифровано: {in_file} -> {out_file} (AES-CBC)")

# Расшифрование файла (AES-CBC)
def decrypt_file(in_file, out_file, password):
    if not os.path.exists(in_file):
        print(f"Файл {in_file} не найден")
        return

    with open(in_file, "rb") as f_in:
        salt = f_in.read(8)
        iv = f_in.read(16)
        if len(salt) != 8 or len(iv) != 16:
            print("Неверный формат зашифрованного файла")
            return

        key = get_key(password, salt)

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()

        decrypted_data = bytearray()
        while True:
            data = f_in.read(16)
            if not data:
                break
            decrypted = decryptor.update(data)
            decrypted_data.extend(decrypted)

        # последний блок – паддинг
        last_byte = decrypted_data[-1]
        if last_byte < 1 or last_byte > 16:
            print("Ошибка расшифровки (паддинг)")
            return
        decrypted_data = decrypted_data[:-last_byte]

        with open(out_file, "wb") as f_out:
            f_out.write(decrypted_data)

    print(f"Расшифровано: {in_file} -> {out_file} (AES-CBC)")

def main():
    while True:
        print("\n" + "="*50)
        print("1 - Зашифровать файл (блочный шифр AES-CBC)")
        print("2 - Расшифровать файл")
        print("0 - Выйти")
        choice = input("Твой выбор: ").strip()

        if choice == '1':
            inp = input("Входной файл: ").strip()
            out = input("Выходной файл: ").strip()
            pwd = input("Пароль: ").strip()
            if inp and out and pwd:
                encrypt_file(inp, out, pwd)
            else:
                print("Не все данные введены")

        elif choice == '2':
            inp = input("Зашифрованный файл: ").strip()
            out = input("Расшифрованный файл: ").strip()
            pwd = input("Пароль: ").strip()
            if inp and out and pwd:
                decrypt_file(inp, out, pwd)
            else:
                print("Не все данные введены")

        elif choice == '0':
            print("Пока")
            break
        else:
            print("Не понял, введи 1, 2 или 0")

if __name__ == "__main__":
    main()